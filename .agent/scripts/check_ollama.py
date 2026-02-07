import requests
import sys
import os

import subprocess

def get_wsl_host_ip():
    """Detects WSL Host IP via default gateway."""
    try:
        result = subprocess.run(
            "ip route show | grep default | awk '{print $3}'", 
            shell=True, capture_output=True, text=True
        )
        return result.stdout.strip()
    except:
        return None

def check_ollama():
    # Candidates: Localhost (Native), WSL Gateway (Windows Host)
    urls = ["http://localhost:11434", "http://127.0.0.1:11434"]
    
    wsl_ip = get_wsl_host_ip()
    if wsl_ip:
        urls.append(f"http://{wsl_ip}:11434")
        print(f"🔎 Detected WSL Gateway: {wsl_ip}")

    print(f"🦙 Checking Ollama on: {', '.join(urls)}...")
    
    for url in urls:
        print(f"👉 Trying {url}...")
        try:
            resp = requests.get(f"{url}/api/tags", timeout=2)
            if resp.status_code == 200:
                models = [m['name'] for m in resp.json().get('models', [])]
                print(f"✅ Ollama FOUND at {url}! ({len(models)} models)")
                for m in models:
                    print(f"   - {m}")
                
                # Suggest updating .env if found on non-localhost
                if "localhost" not in url and "127.0.0.1" not in url:
                    print(f"\n💡 ACTION REQUIRED: Update OLLAMA_BASE_URL in .env to: {url}")
                
                return True
        except requests.exceptions.ConnectionError:
            pass
        except Exception as e:
            print(f"   Error: {e}")

    print("❌ Could not connect to Ollama on any interface.")
    return False

if __name__ == "__main__":
    success = check_ollama()
    sys.exit(0 if success else 1)
