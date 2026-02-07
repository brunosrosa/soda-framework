import json
import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
from smolagents import Tool

# Caminho para o catálogo
CATALOG_PATH = Path(__file__).parent / "../config/mcp_catalog.json"

class McpDockerTool(Tool):
    """
    Base class for Dockerized MCP Tools.
    """
    def __init__(self, server_name: str, tool_name: str, description: str, input_schema: Dict, check_cmd: Optional[List[str]] = None):
        self.server_name = server_name
        self.name = tool_name
        self.description = description
        self.inputs = input_schema
        self.command_line_check = check_cmd
        self.output_type = "string"
        super().__init__()

    def _execute_in_docker(self, kwargs: Dict) -> str:
        """Helper to execute the generic logic."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": f"tools/call",
            "params": {
                "name": self.name,
                "arguments": kwargs
            }
        }
        container_name = f"soda_mcp_{self.server_name}"
        return f"EXECUTED ON {container_name}: {json.dumps(kwargs)}"

class HeuristicTool(McpDockerTool):
    def __init__(self):
        super().__init__(
            "heuristic", "analyze_code", 
            "Analyzes code metrics.", 
            {"path": {"type": "string", "description": "Path to the code to analyze."}},
            check_cmd=["node", "-v"]
        )

    def forward(self, path: str) -> str:
        return self._execute_in_docker({"path": path})

class ToonTool(McpDockerTool):
    def __init__(self):
        super().__init__(
            "toon", "analyze_data_efficiency",
            "Analyzes potential token savings for a file.",
            {"file_path": {"type": "string", "description": "Path to the file to analyze."}},
            check_cmd=["node", "-v"] # Safe check
        )

    def forward(self, file_path: str) -> str:
        return self._execute_in_docker({"file_path": file_path})

class GitHubTool(McpDockerTool):
    def __init__(self):
        super().__init__(
            "github", "github_issues",
            "Manage GitHub Issues.",
            {"query": {"type": "string", "description": "Query string for issues."}},
            check_cmd=["node", "-v"]
        )

    def forward(self, query: str) -> str:
        return self._execute_in_docker({"query": query})

class AlephTool(McpDockerTool):
    def __init__(self):
        super().__init__(
            "aleph", "load_file",
            "Loads a file into Aleph RLM context for deep research.",
            {"path": {"type": "string", "description": "Path to the file to load."}},
            check_cmd=["python", "-c", "import aleph; print('Aleph OK')"]
        )

    def forward(self, path: str) -> str:
        return self._execute_in_docker({"path": path})

class McpManager:
    def __init__(self, profile: str = "default"):
        self.profile = profile
        self.catalog = self._load_catalog() # Simples load
        self.tools = []

    def _load_catalog(self) -> Dict:
        if not CATALOG_PATH.exists():
            # Fallback catalog if file missing
            return {
                "profiles": {
                    "default": ["read_file"],
                    "dev": ["heuristic", "github"],
                    "research": ["toon", "aleph"]
                }
            }
        return json.loads(CATALOG_PATH.read_text())

    def get_tools_for_profile(self) -> List[Tool]:
        """
        Retorna a lista de Tools (Smolagents) ativas para o perfil.
        """
        profile_tools = self.catalog.get("profiles", {}).get(self.profile, [])
        resolved_tools = []
        
        # Resolver server targets (Simulação de logica de catalogo)
        target_servers = []
        # Hardcoded mapping based on profile string for VII-G/H PoC
        if self.profile == "dev":
            target_servers = ["heuristic", "github"]
        elif self.profile == "research":
             target_servers = ["toon", "aleph"]
        elif self.profile == "full":
             target_servers = ["heuristic", "github", "toon", "aleph"]
        
        # Instanciar Classes Específicas
        if "heuristic" in target_servers:
            resolved_tools.append(HeuristicTool())
            
        if "toon" in target_servers:
            resolved_tools.append(ToonTool())
            
        if "github" in target_servers:
            resolved_tools.append(GitHubTool())
            
        if "aleph" in target_servers:
            resolved_tools.append(AlephTool())
            
        return resolved_tools

    def health_check(self) -> Dict[str, str]:
        """
        Verifica se os containers dos serviços ativos no perfil estão rodando e respondendo.
        """
        status = {}
        active_tools = self.get_tools_for_profile()
        checked_servers = set()
        
        for tool in active_tools:
            if isinstance(tool, McpDockerTool):
                server = tool.server_name
                if server in checked_servers:
                    continue
                    
                container_name = f"soda_mcp_{server}"
                try:
                    # 1. Check if container is running
                    res = subprocess.run(
                        ["docker", "inspect", "-f", "{{.State.Running}}", container_name],
                        capture_output=True, text=True
                    )
                    if res.returncode != 0 or "true" not in res.stdout.strip():
                        status[server] = "DOWN (Container not running)"
                        continue
                        
                    # 2. Check if binary responds (Simple version check)
                    # Note: GitHub server requires auth, so might fail execution, but binary should exist.
                    cmd = tool.command_line_check or ["npx", "--version"]
                    
                    # We run 'docker exec' to check inside
                    docker_cmd = ["docker", "exec", "-i", container_name] + cmd
                    
                    res_exec = subprocess.run(
                        docker_cmd, capture_output=True, text=True, timeout=60
                    )
                    
                    if res_exec.returncode == 0:
                        status[server] = f"UP (Response: {res_exec.stdout.strip()[:50]}...)"
                    else:
                        status[server] = f"ERROR (Exit Code {res_exec.returncode}: {res_exec.stderr.strip()[:50]}...)"
                        
                except Exception as e:
                    status[server] = f"EXCEPTION: {str(e)}"
                
                checked_servers.add(server)
                
        return status

if __name__ == "__main__":
    print("🔍 MCP Gateway Health Check")
    manager = McpManager("dev") # Profile com Heuristic e GitHub
    print(f"👤 Profile: {manager.profile}")
    
    tools = manager.get_tools_for_profile()
    print(f"🛠️  Tools Loaded: {[t.name for t in tools]}")
    
    print("\n📡 Checking Connectivity...")
    health = manager.health_check()
    for srv, stat in health.items():
        icon = "✅" if "UP" in stat else "❌"
        print(f"{icon} {srv}: {stat}")

