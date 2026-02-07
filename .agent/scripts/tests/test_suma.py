import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent)) # Add scripts dir to path

from memory_manager import MemoryManager
import time

def test_suma():
    print("🧠 [TEST] Iniciando teste SUMA (SODA Unified Memory Architecture)...")
    
    # 1. Initialize
    mm = MemoryManager()
    
    if not mm.om_connected:
        print("❌ [FAIL] OpenMemory API not reachable.")
        sys.exit(1)
        
    print("✅ [OK] Client connected (REST API).")
    
    # 2. Add Memory
    test_content = "SODA is an AI Framework focused on 'Clean Root' architecture."
    print(f"📥 [ACTION] Adding memory: '{test_content}'")
    try:
        mm.consolidate_memory(test_content, tags=["soda_test", "architecture"])
        print(f"✅ [OK] Add request sent.")
    except Exception as e:
        print(f"❌ [FAIL] Add failed: {e}")

    # 3. Retrieve
    print("🔍 [ACTION] Searching for 'Clean Root'...")
    try:
        # Give a moment for async indexing if any
        time.sleep(1) 
        results = mm.retrieve_similar("Clean Root", limit=1)
        if results:
            print(f"✅ [OK] Found:\n{results}")
        else:
            print("⚠️ [WARN] No results found immediately (Indexing latency?).")
    except Exception as e:
        print(f"❌ [FAIL] Search failed: {e}")

if __name__ == "__main__":
    test_suma()
