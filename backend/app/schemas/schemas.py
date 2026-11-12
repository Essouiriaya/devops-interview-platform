from pydantic import BaseModel, Field


class DomainOut(BaseModel):
    id: str
    name: str
    description: str


class QuestionOut(BaseModel):
    id: int | None = None
    question: str
    difficulty: str


class QuestionGenerateRequest(BaseModel):
    domain: str
    level: str = Field(default="intermédiaire")
    count: int = Field(default=5, ge=1, le=20)
    session_id: int | None = None


class EvaluationOut(BaseModel):
    score: float
    feedback: str
    strengths: list[str]
    improvements: list[str]


class AnswerEvaluateRequest(BaseModel):
    question: str
    answer: str
    domain: str
    level: str = "intermédiaire"
    session_id: int | None = None
    question_id: int | None = None


class SessionCreateRequest(BaseModel):
    domain: str
    level: str = "intermédiaire"


class InterviewSessionOut(BaseModel):
    id: int
    domain: str
    level: str
    score: float | None
    created_at: str


class AnswerDetailOut(BaseModel):
    content: str
    score: float
    feedback: str


class QuestionDetailOut(BaseModel):
    id: int
    content: str
    difficulty: str
    answer: AnswerDetailOut | None = None


class SessionDetailOut(BaseModel):
    session: InterviewSessionOut
    questions: list[QuestionDetailOut]