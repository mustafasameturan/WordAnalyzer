import spacy
from spellchecker import SpellChecker
import re
from typing import Set, List, Dict, Optional

class VocabularyAnalyzer:
    def __init__(self):
        """Analyzer'ı initialize et"""
        self.nlp = spacy.load("en_core_web_sm")
        self.spell = SpellChecker()
        
        # Çıkarılacak kelime türleri (Part of Speech)
        self.exclude_pos = {
            'PUNCT',  # Noktalama işaretleri
            'SPACE',  # Boşluklar
            'SYM',    # Semboller
            'X',      # Diğer
            'CCONJ',  # Bağlaçlar (and, or, but)
            'SCONJ',  # Alt cümle bağlaçları (because, if, when)
            'DET',    # Belirteçler (the, a, an)
            'ADP'     # Edatlar (in, on, at)
        }
        
        # Çıkarılacak bağımlılık türleri
        self.exclude_deps = {'cc', 'punct', 'det', 'case', 'mark'}
        
    def extract_student_speech(self, transcript: str) -> str:
        """
        Transkriptten [S] etiketli öğrenci konuşmalarını çıkar
        
        Args:
            transcript: Ders transkripti
            
        Returns:
            Öğrenci konuşmalarının birleştirilmiş metni
        """
        # [S]: ile başlayan satırları bul
        pattern = r'\[S\]:\s*(.+?)(?=\n\d+\s+\d{2}:|$)'
        student_lines = re.findall(pattern, transcript, re.MULTILINE | re.DOTALL)
        
        # Temizle ve birleştir
        cleaned_lines = []
        for line in student_lines:
            # Timestamp'leri temizle
            line = re.sub(r'\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}', '', line)
            # Satır numaralarını temizle
            line = re.sub(r'^\d+\s+', '', line, flags=re.MULTILINE)
            # [T] veya [S] etiketlerini temizle
            line = re.sub(r'\[(?:T|S)\]:\s*', '', line)
            cleaned_lines.append(line.strip())
        
        return ' '.join(cleaned_lines)
    
    def normalize_word(self, word: str) -> str:
        """
        Kelimeyi normalize et (yazım düzeltme + lemmatization)
        
        Args:
            word: Normalize edilecek kelime
            
        Returns:
            Normalize edilmiş kelime
        """
        # Küçük harfe çevir
        word = word.lower().strip()
        
        # Yazım kontrolü ve düzeltme
        if word in self.spell:
            corrected = word
        else:
            corrected = self.spell.correction(word)
            if corrected is None:
                corrected = word
        
        # Lemmatization için spaCy kullan
        doc = self.nlp(corrected)
        if doc and len(doc) > 0:
            return doc[0].lemma_
        
        return corrected
    
    def extract_meaningful_words(self, text: str) -> Set[str]:
        """
        Metinden anlamlı kelimeleri çıkar
        
        Args:
            text: İşlenecek metin
            
        Returns:
            Anlamlı kelimelerin set'i
        """
        # spaCy ile işle
        doc = self.nlp(text.lower())
        meaningful_words = set()
        
        for token in doc:
            # Filtreleme kriterleri
            if self._is_meaningful_word(token):
                # Normalize et ve ekle
                normalized = self.normalize_word(token.text)
                if len(normalized) > 2:  # 2 harften uzun kelimeler
                    meaningful_words.add(normalized)
        
        return meaningful_words
    
    def _is_meaningful_word(self, token) -> bool:
        """
        Token'ın anlamlı bir kelime olup olmadığını kontrol et
        
        Args:
            token: spaCy token objesi
            
        Returns:
            Anlamlı kelime ise True
        """
        # Özel isim kontrolü (PROPN = proper noun)
        if token.pos_ == 'PROPN':
            return False
        
        # Diğer filtreler
        return (
            token.pos_ not in self.exclude_pos and
            token.dep_ not in self.exclude_deps and
            not token.is_stop and  # Stop words (the, is, at, etc.)
            token.is_alpha and      # Sadece harflerden oluşan
            not token.like_num and   # Sayı değil
            not token.like_email and # Email değil
            not token.like_url       # URL değil
        )
    
    def analyze_vocabulary(
        self, 
        transcript: str, 
        book_text: str, 
        previous_lessons: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Ana analiz fonksiyonu
        
        Args:
            transcript: Ders transkripti
            book_text: Kitap metni
            previous_lessons: Önceki ders analizleri
            
        Returns:
            Analiz sonuçları
        """
        # Öğrenci konuşmalarını çıkar
        student_speech = self.extract_student_speech(transcript)
        
        if not student_speech:
            return {
                'error': 'No student speech found in transcript',
                'total_meaningful_words': 0,
                'unique_words_outside_book': 0,
                'vocabulary_list': [],
                'outside_book_list': []
            }
        
        # Kelimeleri çıkar
        student_words = self.extract_meaningful_words(student_speech)
        book_words = self.extract_meaningful_words(book_text)
        
        # Kitap dışı kelimeler
        outside_book = student_words - book_words
        
        return {
            'total_meaningful_words': len(student_words),
            'unique_words_outside_book': len(outside_book),
            'vocabulary_list': sorted(list(student_words)),
            'outside_book_list': sorted(list(outside_book))
        }