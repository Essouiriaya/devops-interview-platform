from app.core.config import settings


def get_llm(temperature: float = 0.7):
    """Retourne un LLM langchain, ou None si aucune clé API configurée."""
    if not settings.LLM_API_KEY:
        return None
    try:
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
            model=settings.LLM_MODEL,
            temperature=temperature,
        )
    except Exception:
        return None