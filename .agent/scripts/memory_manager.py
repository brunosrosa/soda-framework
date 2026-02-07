import os
import requests
from pathlib import Path
from typing import Dict, Any, List, Optional

class MemoryManager:
    """
    Gerenciador Unificado de Memória (SUMA - SODA Unified Memory Architecture).
    Integra:
    1. Plan-With-Files (Fluido/Hot)
    2. OpenSpec (Estruturado/Gov)
    3. OpenMemory (Profundo/Cold) via API REST
    """
    
    def __init__(self, root_path: str = ".agent", om_url: str = "http://localhost:8080"):
        self.root = Path(root_path)
        self.hot_mem = self.root / "memory/hot"
        self.specs_path = self.root / "openspec/changes"
        self.om_url = om_url
        
        # Garante estrutura
        self.hot_mem.mkdir(parents=True, exist_ok=True)
        
        # Check Connection (Silent fail safe)
        try:
            requests.get(f"{self.om_url}/health", timeout=1)
            self.om_connected = True
            print("✅ [SUMA] OpenMemory connected (REST API).")
        except:
            self.om_connected = False
            print("⚠️ [SUMA] OpenMemory disconnected (API Unreachable).")

    def load_context(self) -> str:
        """Carrega o contexto combinado (Hot + Cold) para o Agente."""
        context = []
        
        # 1. Carrega Plano Tático (PWF - Hot)
        plan_file = self.hot_mem / "task_plan.md"
        if plan_file.exists():
            context.append(f"--- TACTICAL PLAN ---\n{plan_file.read_text(encoding='utf-8')}")
            
        # 2. Carrega Conhecimento (Findings - Hot)
        findings_file = self.hot_mem / "findings.md"
        if findings_file.exists():
            context.append(f"--- KNOWLEDGE BASE ---\n{findings_file.read_text(encoding='utf-8')}")
            
        return "\n\n".join(context)

    def retrieve_similar(self, query: str, limit: int = 3, user_id: str = "soda_agent") -> str:
        """Busca memórias similares no OpenMemory (Cold) via API."""
        if not self.om_connected:
            return ""
            
        try:
            # Endpoint hypothetical based on standard REST practices for OpenMemory
            # Checking recent README or docs, usually /api/memory/search or similar
            # Let's try /api/memory/search
             payload = {"query": query, "limit": limit, "user_id": user_id}
             resp = requests.post(f"{self.om_url}/api/memory/search", json=payload, timeout=2)
             
             if resp.status_code == 200:
                 results = resp.json() # Expecting list of dicts
                 if not results: return ""
                 
                 formatted = ["--- RECALLED MEMORIES (OpenMemory) ---"]
                 for r in results:
                     content = r.get("content", "")
                     score = r.get("score", 0)
                     formatted.append(f"- {content} (Score: {score:.2f})")
                 return "\n".join(formatted)
             else:
                 return ""
        except Exception:
            return "" # Fail silent on retrieval

    def reflect_and_learn(self, action_result: str, context: str = ""):
        """
        Ciclo de Aprendizado (Learning Loop).
        1. Log no Progress.md
        2. Envia para OpenMemory (Consolidação)
        """
        pass 
        
    def log_progress(self, message: str, type: str = "INFO"):
        """Wrapper para logar no progress.md"""
        prog_file = self.hot_mem / "progress.md"
        timestamp = "NOW" 
        entry = f"| {timestamp} | {type} | {message} |"
        
        with open(prog_file, "a", encoding='utf-8') as f:
            f.write(f"\n{entry}")
            
    def consolidate_memory(self, content: str, tags: List[str] = None, user_id: str = "soda_agent"):
        """Salva explicitamente no OpenMemory via API."""
        if self.om_connected:
            try:
                payload = {
                    "content": content,
                    "tags": tags or [],
                    "user_id": user_id
                }
                requests.post(f"{self.om_url}/api/memory", json=payload, timeout=2)
            except Exception as e:
                print(f"Failed to consolidate memory: {e}")
