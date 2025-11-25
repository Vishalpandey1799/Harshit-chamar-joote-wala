import json
from pathlib import Path
from typing import List, Dict, Any, Optional

CONTENT_FILE = Path("shared-data/day4_tutor_content.json")
_CACHE = None

def load_content() -> List[Dict[str, Any]]:
    global _CACHE
    if _CACHE:
        return _CACHE

    print(f">>> [CONTENT] Loading: {CONTENT_FILE}")

    if not CONTENT_FILE.exists():
        print(">>> [CONTENT ERROR] File not found!")
        return []

    try:
        with CONTENT_FILE.open("r") as f:
            _CACHE = json.load(f)
    except Exception as e:
        print(">>> [CONTENT ERROR]", e)
        return []

    return _CACHE


def get_concept_by_id(concept_id: str) -> Optional[Dict[str, Any]]:
    if not concept_id:
        return None
    
    # Normalize to lowercase for case-insensitive matching
    concept_id_lower = concept_id.lower().strip()
    
    for c in load_content():
        if c.get("id", "").lower() == concept_id_lower:
            print(f">>> [CONTENT] Found concept={c.get('id')} (matched '{concept_id}')")
            return c

    print(f">>> [CONTENT] NOT found concept={concept_id} (tried: {concept_id_lower})")
    return None
