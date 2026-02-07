from pathlib import Path
import sys

# Adiciona o diretório atual ao path para importar mcp_manager
sys.path.append(str(Path(__file__).parent))
from mcp_manager import McpManager

def test_gateway():
    print("🚀 SODA MCP GATEWAY VALIDATION")
    print("==============================\n")
    
    # Testar profile 'dev' (Heuristic + GitHub)
    print("1. Testing Profile: 'dev'")
    manager_dev = McpManager("dev")
    tools_dev = manager_dev.get_tools_for_profile()
    print(f"   Tools Inventory: {[t.name for t in tools_dev]}")
    health_dev = manager_dev.health_check()
    for srv, stat in health_dev.items():
        icon = "✅" if "UP" in stat else "❌"
        print(f"   {icon} {srv}: {stat}")
    print("\n")
    
    # Testar profile 'research' (TOON)
    print("2. Testing Profile: 'research'")
    manager_res = McpManager("research")
    tools_res = manager_res.get_tools_for_profile()
    print(f"   Tools Inventory: {[t.name for t in tools_res]}")
    health_res = manager_res.health_check()
    for srv, stat in health_res.items():
        icon = "✅" if "UP" in stat else "❌"
        print(f"   {icon} {srv}: {stat}")
    print("\n")
    
    # Resumo
    print("==============================")
    print("🏁 Validation Complete.")

if __name__ == "__main__":
    test_gateway()
