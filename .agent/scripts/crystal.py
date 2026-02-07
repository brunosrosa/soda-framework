#!/usr/bin/env python3
import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# COLORS
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

SODA_ROOT = Path(__file__).parent.parent.parent

def load_sop_spec(sop_id: str) -> Optional[Dict]:
    """Loads the YAML definition of an SOP."""
    sop_path = SODA_ROOT / ".agent/sops/v3/specs" / f"{sop_id}.yaml"
    # Try finding file with version suffix variation if exact match fails
    if not sop_path.exists():
        # Fallback search
        for f in (SODA_ROOT / ".agent/sops/v3/specs").glob(f"{sop_id}*.yaml"):
            sop_path = f
            break
            
    if not sop_path.exists():
        print(f"{RED}❌ SOP Spec not found: {sop_id}{RESET}")
        return None
        
    try:
        return yaml.safe_load(sop_path.read_text())
    except Exception as e:
        print(f"{RED}❌ Error reading SOP YAML: {e}{RESET}")
        return None

def validate_artifacts(sop_spec: Dict) -> bool:
    """Checks if the output artifacts defined in the SOP exist."""
    outputs = sop_spec.get("outputs", {})
    primary = outputs.get("primary", {})
    
    # 1. Check Primary Output
    primary_path_str = primary.get("path", "")
    if primary_path_str:
        # Handle dynamic paths (basic heuristic)
        if "{{" in primary_path_str:
             print(f"{YELLOW}⚠️  Skipping dynamic path check: {primary_path_str}{RESET}")
        else:
            artifact_path = SODA_ROOT / primary_path_str
            if not artifact_path.exists():
                print(f"{RED}❌ Missing Primary Artifact: {primary_path_str}{RESET}")
                return False
            else:
                print(f"{GREEN}✅ Found Primary Artifact: {primary_path_str}{RESET}")

    return True

import subprocess

def check_git_clean() -> bool:
    """Checks if the git working directory is clean (Crystal Principle: Isolation)."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        if result.stdout.strip():
            print(f"{YELLOW}⚠️  Git Dirty State Detected.{RESET}")
            print("   Crystal recommends a clean state before validation.")
            return False
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    parser = argparse.ArgumentParser(description="Crystal: SODA Governance Validator")
    parser.add_argument("sop_id", help="SOP ID to validate (e.g., SOP-501)")
    parser.add_argument("--bypass", action="store_true", help="Human Sovereignty Override")
    
    args = parser.parse_args()

    print(f"\n🔮 **Crystal Governance Engine** | Validating {args.sop_id}")
    
    if args.bypass:
        print(f"{YELLOW}🛡️  HUMAN SOVEREIGNTY PROTOCOL INVOKED.{RESET}")
        print(f"{YELLOW}⚠️  Validation bypassed by User Command.{RESET}")
        sys.exit(0)

    # Crystal Phase 1: Isolation Check
    if not check_git_clean():
        print(f"{YELLOW}   (Use --bypass to ignore dirty state){RESET}")

    sop_spec = load_sop_spec(args.sop_id)
    if not sop_spec:
        sys.exit(1)

    # Validate
    if validate_artifacts(sop_spec):
        print(f"\n{GREEN}✨ SOP {args.sop_id} Compliance Verified.{RESET}")
        sys.exit(0)
    else:
        print(f"\n{RED}⛔ Validation Failed.{RESET}")
        print(f"Use {YELLOW}--bypass{RESET} if this deviation is intentional (Human Sovereignty).")
        sys.exit(1)

if __name__ == "__main__":
    main()
