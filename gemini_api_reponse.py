from typing import List

from pydantic import BaseModel


class Part(BaseModel):
    text: str


class Content(BaseModel):
    parts: List[Part]
    role: str


class SafetyRating(BaseModel):
    category: str
    probability: str


class Candidate(BaseModel):
    content: Content
    finishReason: str
    index: int
    safetyRatings: List[SafetyRating]


class GeminiResponse(BaseModel):
    candidates: List[Candidate]
