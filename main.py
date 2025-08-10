from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import logging

from models import LessonAnalysis, VocabularyReport
from analyzer import VocabularyAnalyzer

# Logging konfigürasyonu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI instance
app = FastAPI(
    title="Student Vocabulary Analyzer API",
    description="Analyze student vocabulary usage in English lessons",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global analyzer instance
analyzer = VocabularyAnalyzer()

@app.get("/")
async def root():
    """API ana endpoint"""
    return {
        "message": "Student Vocabulary Analyzer API",
        "version": "1.0.0",
        "endpoints": [
            "/analyze-lesson",
            "/health"
        ]
    }

@app.get("/health")
async def health_check():
    """Sağlık kontrolü endpoint'i"""
    return {"status": "healthy"}

@app.post("/analyze-lesson", response_model=Dict)
async def analyze_lesson(data: LessonAnalysis):
    """
    Tek bir dersi analiz et
    
    Args:
        data: Ders transkripti ve kitap metni
        
    Returns:
        Detaylı analiz raporu
    """
    try:
        logger.info("Analyzing lesson")
        
        # Ana analizi yap
        result = analyzer.analyze_vocabulary(
            data.transcript_text,
            data.book_text
        )
        
        # Hata kontrolü
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        
        # Basitleştirilmiş rapor oluştur
        report = {
            "summary": {
                "total_meaningful_words": result['total_meaningful_words'],
                "unique_words_count": len(result['vocabulary_list']),
                "words_outside_book": result['unique_words_outside_book'],
                "percentage_outside_book": round(
                    (result['unique_words_outside_book'] / result['total_meaningful_words'] * 100) 
                    if result['total_meaningful_words'] > 0 else 0, 
                    2
                )
            },
            "vocabulary_breakdown": {
                "all_words_used": result['vocabulary_list'],
                "words_not_in_book": result['outside_book_list']
            }
        }
        
        logger.info("Analysis completed successfully")
        return report
        
    except Exception as e:
        logger.error(f"Error analyzing lesson: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)