# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Student Vocabulary Analyzer API that analyzes student speech from lesson transcripts and compares their vocabulary usage against textbook content. The system identifies words used outside the textbook and provides vocabulary analysis metrics.

## Core Architecture

### Main Components

- **main.py**: FastAPI application with CORS middleware, single global VocabularyAnalyzer instance
- **analyzer.py**: Core VocabularyAnalyzer class that handles NLP processing using spaCy and pyspellchecker
- **models.py**: Pydantic models for request/response validation
- **utils.py**: Currently empty after simplification - previously contained metric calculations

### Key Processing Flow

1. **Input**: `LessonAnalysis` model accepts `transcript_text` and `book_text`
2. **Speech Extraction**: Regex parsing to extract `[S]:` tagged student speech from transcripts
3. **NLP Processing**: spaCy tokenization, lemmatization, POS tagging with configurable exclusions
4. **Spell Correction**: pyspellchecker for normalizing misspelled words
5. **Vocabulary Comparison**: Set operations to find words outside textbook content
6. **Response**: Structured analysis with summary stats and vocabulary breakdowns

### spaCy Configuration

The analyzer excludes specific POS tags and dependency relations:
- POS exclusions: PUNCT, SPACE, SYM, X, CCONJ, SCONJ, DET, ADP
- Dependency exclusions: cc, punct, det, case, mark
- Uses `en_core_web_sm` model

## Development Commands

### Local Development
```bash
# Setup
python -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run API locally
python main.py

# Test API
python test_api.py
```

### Docker Development
```bash
# Build and run (port 8085)
docker-compose up --build

# Run in background
docker-compose up -d

# Stop container
docker-compose down
```

## API Structure

### Endpoints
- `GET /health` - Health check
- `POST /analyze-lesson` - Main analysis endpoint
- `GET /` - API info and available endpoints

### Request/Response Format
**Input**: Only requires `transcript_text` and `book_text` (lesson_date and student_id removed in simplification)

**Output**: 
- `summary`: Total words, unique count, outside-book count, percentage
- `vocabulary_breakdown`: Lists of all words used and words not in textbook

## Important Notes

- The system expects transcript format with `[S]:` tags for student speech
- All text processing is case-insensitive with lemmatization
- Docker container runs on port 8085 externally, 8000 internally
- API has been simplified - no progress tracking, recommendations, or detailed metrics
- CORS is enabled for all origins in development