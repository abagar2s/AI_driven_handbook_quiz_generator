from pydantic import BaseModel
from typing import List

class QuizQuestion(BaseModel):
    frage: str
    antworten: List[str]
    richtige_antworten: List[int]

class UploadResponse(BaseModel):
    handbuch: str
    quiz: List[QuizQuestion]
