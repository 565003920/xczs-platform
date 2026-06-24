"""Knowledge graph analysis service."""
from sqlalchemy.orm import Session
from app.models.knowledge import KnowledgeNode, KnowledgeEdge
from app.models.teaching import Grade


def get_course_knowledge_graph(db: Session, course_id: int) -> dict:
    """Build knowledge graph for a course with mastery rates."""
    nodes = db.query(KnowledgeNode).filter(KnowledgeNode.course_id == course_id).all()
    if not nodes:
        return {"course_id": course_id, "nodes": [], "edges": [], "note": "暂无知识图谱数据"}

    edges = db.query(KnowledgeEdge).filter(
        KnowledgeEdge.source_id.in_([n.id for n in nodes])
    ).all()

    # Compute mastery rate for each node
    node_data = []
    for node in nodes:
        grades = db.query(Grade).filter(
            Grade.knowledge_point == node.name
        ).all()
        avg_score = sum(g.score for g in grades) / len(grades) if grades else 0
        mastery = avg_score / 100.0 if avg_score > 0 else 0
        count = len(grades)

        node_data.append({
            "id": node.id,
            "name": node.name,
            "difficulty": node.difficulty,
            "mastery_rate": round(mastery, 2),
            "avg_score": round(avg_score, 1),
            "sample_count": count,
            "parent_id": node.parent_id,
        })

    edge_data = [{
        "id": e.id,
        "source": e.source_id,
        "target": e.target_id,
        "relation": e.relation_type,
    } for e in edges]

    # Identify bottleneck nodes (low mastery, many dependents)
    target_counts = {}
    for e in edges:
        target_counts[e.source_id] = target_counts.get(e.source_id, 0) + 1

    bottlenecks = [
        n for n in node_data
        if n["mastery_rate"] < 0.6 and target_counts.get(n["id"], 0) >= 1
    ]
    bottlenecks.sort(key=lambda x: x["mastery_rate"])

    return {
        "course_id": course_id,
        "nodes": node_data,
        "edges": edge_data,
        "bottleneck_nodes": [{"id": b["id"], "name": b["name"], "mastery_rate": b["mastery_rate"]} for b in bottlenecks[:5]],
    }
