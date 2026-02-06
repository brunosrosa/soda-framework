#!/usr/bin/env python3
import os
import sys
import time
from pathlib import Path
from typing import Optional

# Dependências Externas (Instalar via uv/pip)
from dotenv import load_dotenv
from smolagents import CodeAgent, LiteLLMModel, Tool
from smolagents.tools import tool

# Carrega variáveis de ambiente do .env na raiz
load_dotenv()

# --- CONFIGURAÇÃO DE HARDWARE AGNÓSTICO (SODA v1.8) ---
# Define quem é o "Big Brain".
# Opções: "gemini" (Cloud - Default), "ollama" (Local GPU - Futuro), "vertex" (Enterprise)
LLM_PROVIDER = os.getenv("SODA_LLM_PROVIDER", "gemini").lower()
MODEL_ID = os.getenv("SODA_LLM_MODEL", "gemini/gemini-3-pro-latest")

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
            print("Para modo Cloud-First, gere uma chave no Google AI Studio.")
            sys.exit(1)
        return LiteLLMModel(model_id=MODEL_ID, api_key=api_key)

    elif LLM_PROVIDER == "ollama":
        # PREPARADO PARA O FUTURO (Quando a ventoinha voltar)
        # Requer: ollama serve rodando
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        print(f"⚠️ MODO LOCAL (GPU/CPU): Conectando em {base_url}")
        return LiteLLMModel(
            model_id=f"ollama/{MODEL_ID}", # ex: ollama/qwen2.5-coder
            api_base=base_url,
            api_key="ollama" # Dummy key
        )
    
    elif LLM_PROVIDER == "anthropic":
        return LiteLLMModel(model_id=MODEL_ID, api_key=os.getenv("ANTHROPIC_API_KEY"))

    else:
        print(f"❌ Provedor '{LLM_PROVIDER}' não suportado neste script.")
        sys.exit(1)

# --- FERRAMENTAS DO SISTEMA (Sovereign File System) ---
# Estas ferramentas dão ao Agente "Mãos" para manipular o projeto.

@tool
def read_file(file_path: str) -> str:
    """
    Lê o conteúdo de um arquivo do projeto com segurança.
    Args:
        file_path: Caminho relativo do arquivo a partir da raiz.
    """
    try:
        # Segurança básica: impedir Path Traversal
        if ".." in file_path:
            return "ERRO DE SEGURANÇA: Acesso a diretórios pai (..) bloqueado pelo SODA."
        
        target = Path(file_path)
        if not target.exists():
            return f"ERRO: Arquivo '{file_path}' não encontrado."

        with open(target, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Erro de I/O ao ler arquivo: {str(e)}"

@tool
def write_file(file_path: str, content: str) -> str:
    """
    Escreve conteúdo em um arquivo. Cria diretórios automaticamente se não existirem.
    Args:
        file_path: Caminho relativo do arquivo.
        content: Conteúdo de texto a ser escrito.
    """
    try:
        if ".." in file_path:
            return "ERRO DE SEGURANÇA: Acesso a diretórios pai (..) bloqueado."

        target = Path(file_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        
        with open(target, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"SUCESSO: Arquivo '{file_path}' escrito/atualizado."
    except Exception as e:
        return f"Erro de I/O ao escrever: {str(e)}"

@tool
def list_files(directory: str = ".") -> str:
    """
    Lista arquivos em um diretório, ignorando artefatos ocultos e venv.
    Args:
        directory: Diretório a listar.
    """
    try:
        if ".." in directory: return "ERRO: Acesso negado."
        
        ignored = {'.git', '__pycache__', 'node_modules', 'venv', '.env', '.DS_Store'}
        items = []
        for item in os.listdir(directory):
            if item not in ignored and not item.startswith('.'):
                items.append(item)
                
        return "\n".join(sorted(items))
    except Exception as e:
        return f"Erro ao listar: {str(e)}"

# --- MOTOR RALPH (A Lógica de Loop) ---

class RalphLoop:
    def __init__(self):
        self.model = get_model()
        
        # CodeAgent: O agente que escreve Python para resolver problemas (roda na CPU local)
        # Ele usa o modelo (Cloud) apenas para raciocinar sobre QUAL código escrever.
        self.agent = CodeAgent(
            tools=[read_file, write_file, list_files],
            model=self.model,
            max_steps=20, # Circuit Breaker para evitar loop infinito
            verbosity_level=1
        )
        
        # Caminhos da Memória Quente
        self.mem_path = Path(".agent/memory/hot")
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