import json
import logging
import re

from app.services.demo_data import evaluate_demo_answer, find_keywords, generate_demo_questions
from app.services.llm_service import get_llm
from app.services.rag_service import get_rag_service

logger = logging.getLogger("uvicorn")


def _parse_json(text: str):
    m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    return json.loads(m.group(0)) if m else None


def generate_questions(domain: str, level: str, count: int) -> list[dict]:
    rag = get_rag_service()
    context = rag.retrieve(f"Questions d'entretien technique sur {domain}, niveau {level}", domain=domain)
    llm = get_llm()
    if llm is not None:
        prompt = f"""Tu es un recruteur technique senior spécialisé en {domain}.
Extraits de documentation de référence (utilise-les pour la pertinence) :
{chr(10).join('- ' + c for c in context)}

Niveau du candidat : {level}.
Génère {count} questions d'entretien techniques adaptées à ce niveau.
Réponds UNIQUEMENT avec un JSON de la forme :
{{"questions": [{{"question": "...", "difficulty": "facile|moyen|difficile"}}]}}"""
        try:
            raw = llm.invoke(prompt).content
            data = _parse_json(raw)
            items = data.get("questions", data) if isinstance(data, dict) else data
            out = [{"question": str(it["question"]),
                    "difficulty": str(it.get("difficulty", level))} for it in items[:count]]
            if out:
                return out
        except Exception as e:
            logger.warning(f"LLM indisponible ({e}), génération démo utilisée.")
    return generate_demo_questions(domain, level, count)


def evaluate_answer(question: str, answer: str, domain: str, level: str) -> dict:
    rag = get_rag_service()
    context = rag.retrieve(f"Évaluation d'une réponse à la question : {question}", domain=domain)
    llm = get_llm()
    if llm is not None:
        prompt = f"""Tu es un examinateur technique senior en {domain} (niveau candidat : {level}).
Question posée : {question}
Réponse du candidat : {answer}
Documentation de référence (base d'évaluation) :
{chr(10).join('- ' + c for c in context)}

Évalue la réponse sur 100 et réponds UNIQUEMENT en JSON :
{{"score": <0-100>, "feedback": "<2-4 phrases constructives>",
  "strengths": ["..."], "improvements": ["..."]}}"""
        try:
            data = _parse_json(llm.invoke(prompt).content)
            if data and "score" in data:
                return {
                    "score": float(data["score"]),
                    "feedback": str(data.get("feedback", "")),
                    "strengths": list(data.get("strengths", [])),
                    "improvements": list(data.get("improvements", [])),
                }
        except Exception as e:
            logger.warning(f"LLM indisponible ({e}), évaluation démo utilisée.")
    keywords = find_keywords(domain, question)
    return evaluate_demo_answer(question, answer, keywords)