from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database.session import is_db_available
from app.models.models import Answer, InterviewSession, Question

_mem = {"sessions": {}, "questions": {}, "seq": 1}


def _next_id() -> int:
    _mem["seq"] += 1
    return _mem["seq"] - 1


def _session_to_dict(s) -> dict:
    created = s["created_at"] if isinstance(s, dict) else s.created_at
    if isinstance(created, datetime):
        created = created.isoformat()
    if isinstance(s, dict):
        return {"id": s["id"], "domain": s["domain"], "level": s["level"],
                "score": s["score"], "created_at": created}
    return {"id": s.id, "domain": s.domain, "level": s.level,
            "score": s.score, "created_at": created}


def create_session(db: Session | None, domain: str, level: str) -> dict:
    if is_db_available():
        s = InterviewSession(domain=domain, level=level)
        db.add(s)
        db.commit()
        db.refresh(s)
        return _session_to_dict(s)
    sid = _next_id()
    _mem["sessions"][sid] = {
        "id": sid, "domain": domain, "level": level,
        "score": None, "created_at": datetime.now(timezone.utc).isoformat(),
    }
    return _session_to_dict(_mem["sessions"][sid])


def add_questions(db: Session | None, session_id: int, items: list[dict]) -> list[dict]:
    if is_db_available():
        out = []
        for it in items:
            q = Question(session_id=session_id, content=it["question"], difficulty=it["difficulty"])
            db.add(q)
            db.flush()
            out.append({"id": q.id, "question": q.content, "difficulty": q.difficulty})
        db.commit()
        return out
    out = []
    for it in items:
        qid = _next_id()
        _mem["questions"][qid] = {
            "id": qid, "session_id": session_id, "content": it["question"],
            "difficulty": it["difficulty"], "answer": None,
        }
        out.append({"id": qid, "question": it["question"], "difficulty": it["difficulty"]})
    return out


def add_answer(db: Session | None, session_id: int, question_id: int | None,
               question_text: str, answer_text: str, evaluation: dict) -> dict:
    if is_db_available():
        if question_id is None:
            q = Question(session_id=session_id, content=question_text, difficulty="moyen")
            db.add(q)
            db.flush()
            question_id = q.id
        a = Answer(question_id=question_id, content=answer_text,
                 score=evaluation["score"], feedback=evaluation["feedback"])
        db.add(a)
        _update_session_score_db(db, session_id)
        db.commit()
        return {"id": a.id, "score": a.score}
    if question_id is None or question_id not in _mem["questions"]:
        qid = _next_id()
        _mem["questions"][qid] = {
            "id": qid, "session_id": session_id, "content": question_text,
            "difficulty": "moyen", "answer": None,
        }
        question_id = qid
    _mem["questions"][question_id]["answer"] = {
        "content": answer_text, "score": evaluation["score"],
        "feedback": evaluation["feedback"],
    }
    _update_session_score_mem(session_id)
    return {"id": question_id, "score": evaluation["score"]}


def _update_session_score_db(db: Session, session_id: int):
    scores = (
        db.query(Answer.score)
        .join(Question, Answer.question_id == Question.id)
        .filter(Question.session_id == session_id)
        .all()
    )
    if scores:
        s = db.get(InterviewSession, session_id)
        s.score = sum(x[0] for x in scores) / len(scores)
        db.add(s)


def _update_session_score_mem(session_id: int):
    answers = [q["answer"] for q in _mem["questions"].values()
               if q["session_id"] == session_id and q.get("answer")]
    if answers and session_id in _mem["sessions"]:
        _mem["sessions"][session_id]["score"] = sum(a["score"] for a in answers) / len(answers)


def list_sessions(db: Session | None) -> list[dict]:
    if is_db_available():
        rows = db.query(InterviewSession).order_by(InterviewSession.id.desc()).all()
        return [_session_to_dict(s) for s in rows]
    return [_session_to_dict(s) for s in
            sorted(_mem["sessions"].values(), key=lambda x: x["id"], reverse=True)]


def get_session_detail(db: Session | None, session_id: int) -> dict | None:
    if is_db_available():
        s = db.get(InterviewSession, session_id)
        if not s:
            return None
        questions = []
        for q in s.questions:
            ans = q.answers[0] if q.answers else None
            questions.append({
                "id": q.id, "content": q.content, "difficulty": q.difficulty,
                "answer": ({"content": ans.content, "score": ans.score,
                            "feedback": ans.feedback} if ans else None),
            })
        return {"session": _session_to_dict(s), "questions": questions}
    s = _mem["sessions"].get(session_id)
    if not s:
        return None
    questions = [
        {"id": q["id"], "content": q["content"], "difficulty": q["difficulty"],
         "answer": q["answer"]}
        for q in _mem["questions"].values() if q["session_id"] == session_id
    ]
    return {"session": _session_to_dict(s), "questions": questions}