from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# Schemas
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Database
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


class Submission(BaseModel):
    email: EmailStr
    name: str
    module: str
    submitted_at: Optional[datetime] = None
    submission: list


class SubmissionOut(BaseModel):
    email: str
    submitted_at: datetime
    submission: list


app = FastAPI(
    title='CS Autograde',
    summary="Storage for exam solutions",
    version='0.0.dev2'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def root():
    return {"message": "Root endpoint"}


@app.post("/submissions", status_code=status.HTTP_201_CREATED, response_model=SubmissionOut)
def create_note(data: Submission, db: Session = Depends(get_db)):
    submission = models.Submission(**data.model_dump())

    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


@app.get("/submissions", response_model=SubmissionOut)
def get_notes(email: str, module: str, db: Session = Depends(get_db)):
    """
    Retrieve submissions based on email and module.

    Query params:
    - email: The email of the user.
    - module: The module of the submission.

    Returns:
    - submissions (models.Submission): Latest submission matching the email and module.
    """
    submissions = db.query(models.Submission).filter(
        models.Submission.email == email, models.Submission.module == module).order_by(models.Submission.submitted_at.desc()).first()

    return submissions
