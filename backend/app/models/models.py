from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database.session import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(50), nullable=False)
    level = Column(String(20), nullable=False)
    score = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    questions = relationship(
        "Question", back_populates="session", cascade="all, delete-orphan"
    )


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    content = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=False)

    session = relationship("InterviewSession", back_populates="questions")
    answers = relationship(
        "Answer", back_populates="question", cascade="all, delete-orphan"
    )


class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    content = Column(Text, nullable=False)
    score = Column(Float, nullable=False)
    feedback = Column(Text, nullable=False)

    question = relationship("Question", back_populates="answers")