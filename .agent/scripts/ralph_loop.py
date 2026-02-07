#!/usr/bin/env python3
import os
import sys
import time
from pathlib import Path
from typing import Optional

# Dependências Externas (Instalar via uv/pip)
import json
import requests
from dotenv import load_dotenv
from smolagents import CodeAgent, LiteLLMModel, Tool, DuckDuckGoSearchTool
from smolagents.tools import tool
from memory_manager import MemoryManager # SUMA

# Carrega variáveis de ambiente do .env na raiz
load_dotenv()

class TavilySearchTool(Tool):
    name = "web_search"
    description = "Searches the web for a given query using Tavily API."
    inputs = {
        "query": {
            "type": "string",
            "description": "The search query to look up on the web.",
        }
    }
    output_type = "string"

    def __init__(self, api_key=None):
        super().__init__()
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")

    def forward(self, query: str) -> str:
        if not self.api_key:
            return "Error: TAVILY_API_KEY not found."
            
        try:
            response = requests.post(
                "https://api.tavily.com/search",
                json={"query": query, "api_key": self.api_key},
                timeout=10
            )
            data = response.json()
            results = data.get("results", [])
            return "\n".join([f"- {r['title']}: {r['url']}\n  {r['content']}" for r in results[:3]])
        except Exception as e:
            return f"Error searching with Tavily: {str(e)}"

# --- CONFIGURAÇÃO DE HARDWARE AGNÓSTICO (SODA v1.8) ---
# Define quem é o "Big Brain".
# Opções: "gemini" (Cloud), "ollama" (Local GPU), "vertex" (Enterprise)
LLM_PROVIDER = os.getenv("SODA_LLM_PROVIDER", "gemini").lower()
RAW_MODEL_STRING = os.getenv("SODA_LLM_MODEL", "flash").lower()

import subprocess

def get_ollama_url():
    """
    Tenta descobrir a URL do Ollama automaticamente.
    Prioridade:
    1. ENV VAR (Se definida explicitamente)
    2. Localhost (Linux Nativo)
    3. WSL Gateway (Windows Host via WSL)
    """
    env_url = os.getenv("OLLAMA_BASE_URL")
    if env_url and "localhost" not in env_url:
        return env_url
        
    candidates = ["http://localhost:11434"]
    
    # Tentativa de descobrir IP do Host WSL
    try:
        result = subprocess.run(
            "ip route show | grep default | awk '{print $3}'", 
            shell=True, capture_output=True, text=True
        )
        gateway_ip = result.stdout.strip()
        if gateway_ip:
            candidates.append(f"http://{gateway_ip}:11434")
    except:
        pass
        
    # Testar conectividade
    print("🔌 SODA Kernel: Buscando servidor Ollama...")
    for url in candidates:
        try:
            resp = requests.get(f"{url}/api/tags", timeout=1)
            if resp.status_code == 200:
                print(f"✅ Ollama encontrado em: {url}")
                return url
        except:
            continue
            
    print("⚠️ Ollama não encontrado. Usando default (localhost).")
    return "http://localhost:11434"

def get_model():
    """
    Fábrica de Modelos Agnóstica de Hardware.
    Decide qual cérebro usar baseado na configuração do .env.
    """
    print(f"🔌 SODA Kernel: Inicializando provedor '{LLM_PROVIDER}'...")

    if LLM_PROVIDER == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("🚨 ERRO: 'GEMINI_API_KEY' não encontrada no .env.")
            sys.exit(1)
            
        # Agnostic Model Selection (Always Latest)
        if "pro" in RAW_MODEL_STRING:
             model_id = "gemini/gemini-pro-latest"
             print("✨ Selecionado: Gemini Pro (Latest)")
        else:
             model_id = "gemini/gemini-flash-latest"
             print("⚡ Selecionado: Gemini Flash (Latest)")
             
        return LiteLLMModel(model_id=model_id, api_key=api_key)

    elif LLM_PROVIDER == "ollama":
        base_url = get_ollama_url()
        print(f"⚠️ MODO LOCAL (GPU/CPU): Conectando em {base_url}")
        
        # Smart Local Mapping (Baseado nos testes do usuário)
        # raw string -> ollama tag
        local_map = {
            "qwen": "qwen2.5:3b",    # Assumindo 3b/4b como default leve
            "qwen3": "qwen3:4b",     # Requested by User
            "phi": "phi4-mini",      # Microsoft Phi-4 Mini
            "reasoning": "phi4-mini-reasoning"
        }
        
        # Tenta encontrar match ou usa string crua
        tag = local_map.get(RAW_MODEL_STRING, RAW_MODEL_STRING)
        # Se usuário digitou algo específico que contenha a chave (ex: "qwen-coder")
        for key, val in local_map.items():
            if key in RAW_MODEL_STRING:
                tag = val
                break
        
        print(f"🦙 Selecionado Local: {tag}")
        
        return LiteLLMModel(
            model_id=f"ollama/{tag}", 
            api_base=base_url,
            api_key="ollama" 
        )
    
    else:
        print(f"❌ Provedor '{LLM_PROVIDER}' não suportado neste script.")
        sys.exit(1)

# ... (Ferramentas de Arquivo mantidas) ...

# --- MOTOR RALPH (A Lógica de Loop) ---

class RalphLoop:
    def __init__(self):
        self.model = get_model()
        
        # Tools: Filesystem + Web Search (Os Olhos)
        # Prioridade: Tavily (API) > DuckDuckGo (Free)
        tools_list = [read_file, write_file, list_files]
        
        tavily_key = os.getenv("TAVILY_API_KEY")
        if tavily_key:
            print("🦅 Search: Tavily Activated")
            tools_list.append(TavilySearchTool(api_key=tavily_key))
        else:
            print("🦆 Search: DuckDuckGo Activated (Fallback)")
            tools_list.append(DuckDuckGoSearchTool())
        
        # --- MCP GATEWAY INTEGRATION (VII-G) ---
        try:
            # Add local scripts path to sys.path to ensure import works if running from root
            sys.path.append(str(Path(__file__).parent))
            from mcp_manager import McpManager
            
            mcp_profile = os.getenv("SODA_PROFILE", "dev") # Default to dev for testing
            print(f"🔌 MCP Gateway: Loading profile '{mcp_profile}'...")
            
            mcp_mgr = McpManager(mcp_profile)
            # Health check quick scan (optional, maybe too slow for every boot? Skipping for speed)
            # mcp_health = mcp_mgr.health_check()
            
            mcp_tools = mcp_mgr.get_tools_for_profile()
            if mcp_tools:
                tool_names = [t.name for t in mcp_tools]
                print(f"🛠️  MCP Tools Inject: {tool_names}")
                tools_list.extend(mcp_tools)
            else:
                print(f"ℹ️  MCP Gateway: No tools for profile '{mcp_profile}'")
                
        except Exception as e:
            print(f"⚠️ MCP Gateway Warning: Required dependencies missing or Docker down. ({e})")
            # Non-blocking failure
            pass
        self.agent = CodeAgent(
            tools=tools_list,
            model=self.model,
            max_steps=20, 
            verbosity_level=1
        )
        
        # Caminhos da Memória Quente (Delegado ao MemoryManager)
        self.memory = MemoryManager() # SUMA Engine
        self.mem_path = self.memory.hot_mem
        self.paths = {
            "plan": self.mem_path / "task_plan.md",
            "progress": self.mem_path / "progress.md",
            "findings": self.mem_path / "findings.md"
        }

    def _ensure_memory(self):
        """Garante que a estrutura de memória existe."""
        self.mem_path.mkdir(parents=True, exist_ok=True)
        for p in self.paths.values():
            if not p.exists():
                p.touch()

    def load_context(self) -> str:
        """Carrega o estado atual do projeto."""
        self._ensure_memory()
        
        context = "CONTEXTO SODA v1.8:\n"
        
        # 1. Lê o Plano Tático
        plan_content = self.paths["plan"].read_text(encoding='utf-8').strip()
        if not plan_content:
            return "ALERTA: 'task_plan.md' está vazio. Execute /sharding primeiro."
        context += f"\n--- PLANO TÁTICO (O QUE FAZER) ---\n{plan_content}\n"

        # 2. Lê Descobertas (se houver)
        findings = self.paths["findings"].read_text(encoding='utf-8').strip()
        if findings:
            context += f"\n--- CONHECIMENTO ADQUIRIDO ---\n{findings}\n"
        
        return context

    def log_progress(self, message: str, type="INFO"):
        """Persiste logs no arquivo imutável."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n[{timestamp}] [{type}] RALPH: {message}"
        
        # Feedback visual no terminal
        color = "\033[92m" if type == "SUCCESS" else "\033[91m" if type == "ERROR" else "\033[0m"
        print(f"{color}{entry}\033[0m")
        
        with open(self.paths["progress"], "a", encoding="utf-8") as f:
            f.write(entry)

    def run(self, task_instruction: str):
        """Executa o ciclo OODA para uma tarefa."""
        print(f"🥤 RALPH ENGINE v1.8 INICIADO")
        print(f"🎯 Alvo: {task_instruction}")
        
        self.log_progress(f"Iniciando run: {task_instruction}")
        context = self.load_context()

        # O Prompt System é injetado dinamicamente
        prompt = f"""
        {context}
        
        --- MISSÃO IMEDIATA ---
        {task_instruction}
        
        --- REGRAS DE EXECUÇÃO (SODA v1.8) ---
        1. Você é um CodeAgent. Use Python para manipular arquivos e lógica.
        2. NÃO assuma que arquivos existem; use `list_files` ou `read_file` para verificar.
        3. Se for criar código, escreva o arquivo completo.
        4. Se precisar de bibliotecas externas, avise no final (não instale sem permissão).
        5. PROTEÇÃO DE HARDWARE: Não tente rodar modelos pesados locais. Use sua inteligência Python (CPU).
        
        Retorne um resumo curto do que foi realizado.
        """

        try:
            # A mágica do Smolagents acontece aqui
            result = self.agent.run(prompt)
            
            self.log_progress(f"Concluído: {result}", type="SUCCESS")
            
            # --- SUMA LEARNING LOOP ---
            self.memory.reflect_and_learn(result)
            self.memory.log_progress(f"Ação executada: {task_instruction}")
            
        except Exception as e:
            error_msg = f"Falha na execução: {str(e)}"
            self.log_progress(error_msg, type="ERROR")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python ralph_loop.py '<tarefa>'")
        print("Ex: python ralph_loop.py 'Criar estrutura inicial do src conforme task_plan'")
        sys.exit(1)
        
    task = sys.argv[1]
    ralph = RalphLoop()
    ralph.run(task)