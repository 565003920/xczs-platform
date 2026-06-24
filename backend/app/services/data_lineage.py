"""Data lineage tracking service."""
from sqlalchemy.orm import Session
from datetime import datetime


_lineage_store = []  # In-memory for MVP


def record_lineage(analysis_id: str, analysis_type: str, inputs: list[dict], output: dict):
    """Record a lineage entry."""
    _lineage_store.append({
        "analysis_id": analysis_id,
        "analysis_type": analysis_type,
        "inputs": inputs,
        "output": output,
        "timestamp": datetime.now().isoformat(),
    })
    # Keep only last 100
    if len(_lineage_store) > 100:
        _lineage_store.pop(0)


def get_lineage(analysis_id: str) -> dict:
    for entry in _lineage_store:
        if entry["analysis_id"] == analysis_id:
            return entry
    return None


def get_all_lineages() -> list[dict]:
    return list(reversed(_lineage_store))
