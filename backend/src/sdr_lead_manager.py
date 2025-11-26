import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

LEADS_FILE = Path("shared-data/day5_leads.json")


def load_leads() -> List[Dict[str, Any]]:
    """Load all leads from file"""
    if not LEADS_FILE.exists():
        return []

    try:
        with LEADS_FILE.open("r") as f:
            return json.load(f)
    except Exception as e:
        print(f">>> [LEADS ERROR] Failed to load: {e}")
        return []


def save_leads(leads: List[Dict[str, Any]]) -> bool:
    """Save leads to file"""
    try:
        LEADS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with LEADS_FILE.open("w") as f:
            json.dump(leads, f, indent=2)
        print(f">>> [LEADS] Saved {len(leads)} leads to {LEADS_FILE}")
        return True
    except Exception as e:
        print(f">>> [LEADS ERROR] Failed to save: {e}")
        return False


def create_lead() -> Dict[str, Any]:
    """Create a new empty lead"""
    return {
        "id": datetime.now().isoformat(),
        "name": None,
        "company": None,
        "email": None,
        "phone": None,
        "role": None,
        "use_case": None,
        "team_size": None,
        "timeline": None,
        "collected_at": datetime.now().isoformat(),
        "notes": []
    }


def add_lead_field(lead: Dict[str, Any], field: str, value: str | None) -> Dict[str, Any]:
    """Add a field value to a lead"""
    if field in lead:
        lead[field] = value
        print(f">>> [LEAD] Collected {field}={value}")
    return lead


def save_lead(lead: Dict[str, Any]) -> bool:
    """Save a single lead to the leads file"""
    leads = load_leads()
    leads.append(lead)
    return save_leads(leads)


def get_lead_summary(lead: Dict[str, Any]) -> str:
    """Generate a summary of a lead"""
    name = lead.get("name") or "Unknown"
    company = lead.get("company") or "Not specified"
    role = lead.get("role") or "Not specified"
    use_case = lead.get("use_case") or "Not specified"
    timeline = lead.get("timeline") or "Not specified"
    team_size = lead.get("team_size") or "Not specified"

    summary = f"""
Lead Summary:
- Name: {name}
- Company: {company}
- Role: {role}
- Use Case: {use_case}
- Team Size: {team_size}
- Timeline: {timeline}
    """
    return summary.strip()

