from app.services import ai_service, demo_data
from app.services.rag_service import get_rag_service


def test_rag_retrieval_memory():
    # Qdrant en mode ':memory:' si le serveur n'est pas lancé
    rag = get_rag_service()
    chunks = rag.retrieve("jointures SQL", domain="sql", k=2)
    assert len(chunks) >= 1
    assert any("JOIN" in c or "index" in c for c in chunks)


def test_rag_fallback_context():
    rag = get_rag_service()
    chunks = rag.retrieve("anything", domain="inconnu", k=2)
    assert len(chunks) >= 1  # repli sur la base brute


def test_demo_evaluation_bounds():
    good = "Une liste est mutable et un tuple immuable, ex: l=[1] modifiable, t=(1,2) constant."
    res = demo_data.evaluate_demo_answer("q", good, ["mutable", "immuable", "tuple"])
    assert 0 <= res["score"] <= 100
    assert res["score"] > 50
    short = demo_data.evaluate_demo_answer("q", "oui", ["x"])
    assert short["score"] <= 10


def test_ai_service_generate_fallback():
    # Sans LLM_API_KEY configurée : repli démo
    out = ai_service.generate_questions("python", "débutant", 4)
    assert len(out) == 4
    assert all("question" in q for q in out)


def test_ai_service_evaluate_fallback():
    out = ai_service.evaluate_answer(
        "Qu'est-ce que le surapprentissage (overfitting) ?",
        "Le surapprentissage arrive quand le modèle mémorise les données d'entraînement ; "
        "on le limite avec la régularisation et la validation croisée.",
        "machine-learning", "intermédiaire",
    )
    assert 0 <= out["score"] <= 100
    assert out["improvements"]