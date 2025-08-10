from pydantic import BaseModel
from typing import List, Dict, Optional

class LessonAnalysis(BaseModel):
    """Tek ders analizi için input modeli"""
    transcript_text: str
    book_text: str

class VocabularyReport(BaseModel):
    """API response modeli"""
    summary: Dict
    vocabulary_breakdown: Dict