import json
from pathlib import Path
from typing import List, Dict, Any, Optional

CONTENT_FILE = Path("shared-data/day5_sdr_content.json")
_CACHE = None


def load_content() -> Dict[str, Any]:
    """Load SDR content for Razorpay"""
    global _CACHE
    if _CACHE:
        return _CACHE

    print(f">>> [SDR CONTENT] Loading: {CONTENT_FILE}")

    if not CONTENT_FILE.exists():
        print(">>> [SDR CONTENT ERROR] File not found!")
        return {}

    try:
        with CONTENT_FILE.open("r") as f:
            _CACHE = json.load(f)
    except Exception as e:
        print(">>> [SDR CONTENT ERROR]", e)
        return {}

    return _CACHE


def get_company_info() -> Dict[str, Any]:
    """Get company details"""
    content = load_content()
    return content.get("company", {})


def get_faq_by_keyword(keyword: str) -> Optional[Dict[str, Any]]:
    """Find FAQ entry by keyword matching"""
    if not keyword:
        return None

    keyword_lower = keyword.lower().strip()
    content = load_content()
    faq_list = content.get("faq", [])

   
    for faq in faq_list:
        if keyword_lower in faq.get("question", "").lower():
            print(f">>> [SDR FAQ] Found: {faq.get('question')}")
            return faq

 
    for faq in faq_list:
        if keyword_lower in faq.get("answer", "").lower():
            print(f">>> [SDR FAQ] Found (answer match): {faq.get('question')}")
            return faq

    print(f">>> [SDR FAQ] NOT found for keyword: {keyword}")
    return None


def get_all_faq() -> List[Dict[str, Any]]:
    """Get all FAQ entries"""
    content = load_content()
    return content.get("faq", [])


def get_lead_fields() -> List[str]:
    """Get list of lead fields to collect"""
    content = load_content()
    return content.get("lead_fields", [])
