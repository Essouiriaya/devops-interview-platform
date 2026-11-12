from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        r = client.get("/api/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


def test_domains():
    with TestClient(app) as client:
        r = client.get("/api/domains")
        assert r.status_code == 200
        assert len(r.json()["domains"]) >= 6


def test_get_questions_demo():
    with TestClient(app) as client:
        r = client.get("/api/questions", params={"domain": "python", "level": "débutant"})
        assert r.status_code == 200
        assert len(r.json()["questions"]) == 5


def test_generate_questions_fallback():
    # Sans clé LLM : la génération doit retomber sur les données démo
    with TestClient(app) as client:
        r = client.post("/api/questions/generate",
                        json={"domain": "sql", "level": "avancé", "count": 3})
        assert r.status_code == 200
        body = r.json()
        assert len(body) == 3
        assert "question" in body[0]


def test_evaluate_answer():
    with TestClient(app) as client:
        r = client.post("/api/answers/evaluate", json={
            "question": "Quelle est la différence entre une liste et un tuple en Python ?",
            "answer": "Une liste est mutable, on peut la modifier, "
                      "alors qu'un tuple est immuable et hachable.",
            "domain": "python",
            "level": "débutant",
        })
        assert r.status_code == 200
        data = r.json()
        assert 0 <= data["score"] <= 100
        assert data["feedback"]
        assert isinstance(data["strengths"], list)


def test_full_session_flow():
    with TestClient(app) as client:
        s = client.post("/api/sessions", json={"domain": "devops", "level": "intermédiaire"})
        assert s.status_code == 200
        session_id = s.json()["id"]

        q = client.post("/api/questions/generate",
                        json={"domain": "devops", "level": "intermédiaire",
                              "count": 2, "session_id": session_id})
        assert q.status_code == 200
        questions = q.json()
        assert all("id" in item for item in questions)

        e = client.post("/api/answers/evaluate", json={
            "question": questions[0]["question"],
            "answer": "Une image Docker est un modèle immuable construit depuis un Dockerfile, "
                      "tandis qu'un conteneur est une instance en cours d'exécution de cette image.",
            "domain": "devops", "level": "intermédiaire",
            "session_id": session_id, "question_id": questions[0]["id"],
        })
        assert e.status_code == 200

        detail = client.get(f"/api/sessions/{session_id}")
        assert detail.status_code == 200
        body = detail.json()
        assert body["session"]["id"] == session_id
        assert body["session"]["score"] is not None
        assert any(item["answer"] for item in body["questions"])


def test_session_not_found():
    with TestClient(app) as client:
        r = client.get("/api/sessions/999999")
        assert r.status_code == 404