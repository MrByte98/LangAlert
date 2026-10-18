"""
Intelligent keyboard mismatch detector.
Evaluates typed text against English and Persian linguistic rules,
dictionaries, vowel ratios, and active OS layout context.
"""
from dataclasses import dataclass
from typing import Optional, List
import re

from .config import config
from .converter import (
    convert_en_to_fa,
    convert_fa_to_en,
    get_script_distribution,
    is_english_char,
    is_persian_char
)
from .dictionary import dictionary
from .layout_detector import get_active_keyboard_layout
from .ngram_model import ngram_evaluator

@dataclass
class DetectionResult:
    original_text: str
    converted_text: str
    direction: str  # "en_to_fa" or "fa_to_en"
    confidence: float  # 0.0 to 1.0
    reason: str
    matched_words: List[str]

    @property
    def direction_label(self) -> str:
        if self.direction == "en_to_fa":
            return "انگلیسی ⬅ فارسی (کیبورد روی EN بود)"
        return "فارسی ⬅ انگلیسی (کیبورد روی FA بود)"

    @property
    def direction_badge(self) -> str:
        return "EN ➔ FA" if self.direction == "en_to_fa" else "FA ➔ EN"

class Detector:
    def __init__(self):
        pass

    def evaluate(self, buffer_text: str, active_layout: Optional[str] = None) -> Optional[DetectionResult]:
        """
        Evaluates a string buffer (single word or recent phrase) to determine
        if it was typed using the wrong keyboard layout.
        Uses active foreground window layout context to eliminate false positives.
        """
        if not config.get("enabled", True):
            return None

        clean_text = buffer_text.strip()
        min_len = config.get("min_word_length", 3)

        if len(clean_text) < min_len:
            return None

        # Resolve active layout if not explicitly provided
        if not active_layout or active_layout == "unknown":
            active_layout = get_active_keyboard_layout()

        # Context-aware dispatch based on current OS keyboard layout:
        # 1. If active layout is Persian ('fa'):
        #    The user IS ALREADY in Persian mode. They cannot have forgotten to switch to Persian!
        #    Therefore, we NEVER check for EN -> FA errors.
        #    We ONLY check if the user intended English but was trapped in Persian layout (FA -> EN).
        if active_layout == "fa":
            if config.get("check_fa_to_en", True):
                return self._check_fa_to_en(clean_text, min_len)
            return None

        # 2. If active layout is English ('en'):
        #    The user IS ALREADY in English mode. They cannot have forgotten to switch to English!
        #    Therefore, we NEVER check for FA -> EN errors.
        #    We ONLY check if the user intended Persian but was trapped in English layout (EN -> FA).
        if active_layout == "en":
            if config.get("check_en_to_fa", True):
                return self._check_en_to_fa(clean_text, min_len)
            return None

        # 3. Fallback when active layout cannot be queried (e.g. unknown platform):
        dist = get_script_distribution(clean_text)
        predom = dist["predominant"]

        if predom == "en" and config.get("check_en_to_fa", True):
            return self._check_en_to_fa(clean_text, min_len)
        elif predom == "fa" and config.get("check_fa_to_en", True):
            return self._check_fa_to_en(clean_text, min_len)

        return None

    def _check_en_to_fa(self, text: str, min_len: int) -> Optional[DetectionResult]:
        words = [w for w in re.split(r"[^\w]+", text) if w]
        if not words:
            return None

        valid_words = [w for w in words if len(w) >= min_len and w.isascii() and w.isalpha()]
        if not valid_words:
            tokens = text.split(" ")
            valid_words = [t for t in tokens if len(t) >= min_len]
            if not valid_words:
                return None

        matched_fa_words = []
        impossible_vowel_count = 0
        known_en_count = 0

        for w in valid_words:
            if dictionary.is_valid_english(w):
                known_en_count += 1

            fa_cand = convert_en_to_fa(w)
            if dictionary.is_valid_persian(fa_cand):
                matched_fa_words.append(fa_cand)

            vowel_ratio = dictionary.english_vowel_ratio(w)
            if len(w) >= 3 and vowel_ratio == 0.0:
                impossible_vowel_count += 1

        # 1. Exact match in comprehensive Persian dictionary
        if matched_fa_words and known_en_count == 0:
            confidence = 0.95
            if impossible_vowel_count > 0:
                confidence = 0.99
            converted = convert_en_to_fa(text)
            return DetectionResult(
                original_text=text,
                converted_text=converted,
                direction="en_to_fa",
                confidence=confidence,
                reason=f"کلمات وارد شده در انگلیسی بی‌معنی بودند، اما در زبان فارسی کلمات «{', '.join(matched_fa_words)}» را ساختند.",
                matched_words=matched_fa_words
            )

        # 2. Statistical Character N-Gram Language Model Evaluation (Trigram/Bigram)
        # Catches out-of-dictionary terms, novel words, slang, and names with statistical certainty
        sensitivity = config.get("sensitivity", "medium")
        if sensitivity in ("medium", "high") and known_en_count == 0:
            is_ngram_mismatch, ngram_conf, en_score, fa_score = ngram_evaluator.evaluate_en_keystrokes_for_persian(text)
            if is_ngram_mismatch:
                converted = convert_en_to_fa(text)
                return DetectionResult(
                    original_text=text,
                    converted_text=converted,
                    direction="en_to_fa",
                    confidence=ngram_conf,
                    reason=f"مدل آماری ان‌گرام حروف نشان می‌دهد توالی حروف ({fa_score:.1f} vs {en_score:.1f}) متعلق به زبان فارسی است.",
                    matched_words=[converted]
                )

            # Heuristic fallback for vowel-less clusters
            if impossible_vowel_count >= 1:
                converted = convert_en_to_fa(text)
                if any(is_persian_char(c) for c in converted):
                    confidence = 0.85 if sensitivity == "high" else 0.75
                    return DetectionResult(
                        original_text=text,
                        converted_text=converted,
                        direction="en_to_fa",
                        confidence=confidence,
                        reason="متن بدون حروف صدادار انگلیسی است و ساختار کیبورد فارسی را نشان می‌دهد.",
                        matched_words=[converted]
                    )

        return None

    def _check_fa_to_en(self, text: str, min_len: int) -> Optional[DetectionResult]:
        words = [w for w in re.split(r"[\s\u200c\.,،؛!؟]+", text) if w]
        if not words:
            return None

        valid_words = [w for w in words if len(w) >= min_len and any(is_persian_char(c) for c in w)]
        if not valid_words:
            return None

        matched_en_words = []
        plausible_en_words = []
        known_fa_count = 0

        for w in valid_words:
            # If word is a recognized Persian word, note it
            if dictionary.is_valid_persian(w):
                known_fa_count += 1

            # Convert to English candidate
            en_cand = convert_fa_to_en(w)
            if dictionary.is_valid_english(en_cand):
                matched_en_words.append(en_cand)
            elif self._is_plausible_english(en_cand):
                plausible_en_words.append(en_cand)

        # 1. Exact match in comprehensive English dictionary
        if matched_en_words and known_fa_count == 0:
            converted = convert_fa_to_en(text)
            return DetectionResult(
                original_text=text,
                converted_text=converted,
                direction="fa_to_en",
                confidence=0.98,
                reason=f"متن وارد شده در فارسی بی‌معنی بود، اما در زبان انگلیسی کلمه معتبر «{', '.join(matched_en_words)}» را ساخت.",
                matched_words=matched_en_words
            )

        # 2. Statistical Character N-Gram Language Model Evaluation (Trigram/Bigram)
        # Evaluates statistical likelihood of English syllable transitions vs Persian
        sensitivity = config.get("sensitivity", "medium")
        if sensitivity in ("medium", "high") and known_fa_count == 0:
            is_ngram_mismatch, ngram_conf, fa_score, en_score = ngram_evaluator.evaluate_fa_keystrokes_for_english(text)
            if is_ngram_mismatch:
                converted = convert_fa_to_en(text)
                return DetectionResult(
                    original_text=text,
                    converted_text=converted,
                    direction="fa_to_en",
                    confidence=ngram_conf,
                    reason=f"مدل آماری ان‌گرام حروف نشان می‌دهد توالی حروف ({en_score:.1f} vs {fa_score:.1f}) متعلق به زبان انگلیسی است.",
                    matched_words=[converted]
                )

        return None

    def _is_plausible_english(self, word: str) -> bool:
        """Determines if a string matches plausible English syllable and vowel structure."""
        w = word.lower().strip()
        if len(w) < 3 or not w.isalpha() or not w.isascii():
            return False
        vowels = [c for c in w if c in set("aeiouy")]
        v_ratio = len(vowels) / len(w)
        if v_ratio < 0.15 or v_ratio > 0.75:
            return False
        # Reject impossible 4-consonant clusters
        if re.search(r"[^aeiouy]{4,}", w):
            return False
        # Reject 4-vowel cluster
        if re.search(r"[aeiouy]{4,}", w):
            return False
        return True

# Global detector singleton
detector = Detector()
