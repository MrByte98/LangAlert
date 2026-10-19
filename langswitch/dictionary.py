"""
Dictionary manager and morphological stemmer for English and Persian.
Provides high-performance O(1) set lookups, prefix/suffix stripping,
and character normalization.
"""
import json
import re
from pathlib import Path
from typing import Set

import sys
_meipass = getattr(sys, "_MEIPASS", None)
if _meipass:
    DICT_DIR = Path(_meipass) / "langswitch" / "dictionaries"
    if not DICT_DIR.exists():
        DICT_DIR = Path(_meipass) / "dictionaries"
else:
    DICT_DIR = Path(__file__).parent / "dictionaries"

FA_PREFIXES = [
    "نمی‌", "نمی ", "نمی", "می‌", "می ", "می", "بی‌", "بی ", "بی", "با", "نا", "هم", "پیش", "باز", "بر"
]
FA_SUFFIXES = [
    "‌هایمان", "هایمان", "‌هایتان", "هایتان", "‌هایشان", "هایشان",
    "‌هایم", "هایم", "هایت", "هایت", "‌هایش", "هایش", "‌هایی", "هایی",
    "‌های", "های", "‌ها", "ها",
    "مان", "تان", "شان", "ام", "ات", "اش",
    "ترین", "تر", "ندگان", "نده", "گان", "ان", "گی", "گری", "مند", "ناک", "وار",
    "ستان", "کده", "گاه", "ی", "ای"
]

EN_SUFFIXES = ["ing", "edly", "ingly", "tion", "ment", "ness", "able", "ible", "less", "ful", "ed", "es", "ly", "er", "est", "s"]
EN_PREFIXES = ["un", "re", "in", "im", "dis", "pre", "post", "anti", "multi", "sub", "super", "auto"]

EN_VOWELS = set("aeiouyAEIOUY")

def clean_fa(text: str) -> str:
    """Removes diacritics, normalizes letters, strips extra spaces and ZWNJ."""
    t = text.replace("ك", "ک").replace("ي", "ی").replace("ى", "ی")
    t = t.replace("ـ", "")
    t = re.sub(r"[\u064B-\u065F\u0670]", "", t)  # Remove Arabic Tashkeel / Harakat
    return t.strip()

def normalize_persian(text: str) -> str:
    """Normalizes Persian text for dictionary matching."""
    t = clean_fa(text)
    return t

class Dictionary:
    def __init__(self):
        self.fa_words: Set[str] = set()
        self.en_words: Set[str] = set()
        self.user_fa_words: Set[str] = set()
        self.user_en_words: Set[str] = set()
        self._load_dictionaries()

    def _load_dictionaries(self):
        fa_path = DICT_DIR / "fa_words.json"
        en_path = DICT_DIR / "en_words.json"

        if fa_path.exists():
            try:
                with open(fa_path, "r", encoding="utf-8") as f:
                    words = json.load(f)
                    self.fa_words = {normalize_persian(w) for w in words}
            except Exception as e:
                print(f"[Dictionary] Error loading FA words: {e}")

        if en_path.exists():
            try:
                with open(en_path, "r", encoding="utf-8") as f:
                    words = json.load(f)
                    self.en_words = {w.lower().strip() for w in words}
            except Exception as e:
                print(f"[Dictionary] Error loading EN words: {e}")

    def add_user_word(self, word: str, lang: str):
        word = word.strip()
        if not word:
            return
        if lang == "fa":
            self.user_fa_words.add(normalize_persian(word))
        elif lang == "en":
            self.user_en_words.add(word.lower())

    def is_valid_persian(self, word: str) -> bool:
        """Determines if a word is a plausible Persian word using dictionary & morphology."""
        w = normalize_persian(word)
        if not w:
            return False
        if w in self.fa_words or w in self.user_fa_words:
            return True

        # Check multi-word phrase
        parts = w.split(" ")
        if len(parts) > 1:
            if all(self.is_valid_persian(p) for p in parts if len(p) >= 2):
                return True

        # Try stripping prefixes
        for pref in FA_PREFIXES:
            if w.startswith(pref) and len(w) > len(pref) + 1:
                stem = w[len(pref):]
                if stem in self.fa_words or stem in self.user_fa_words:
                    return True
                # Stem minus suffixes
                for suf in FA_SUFFIXES:
                    if stem.endswith(suf) and len(stem) > len(suf) + 1:
                        if stem[:-len(suf)] in self.fa_words:
                            return True

        # Try stripping suffixes
        for suf in FA_SUFFIXES:
            if w.endswith(suf) and len(w) > len(suf) + 1:
                stem = w[:-len(suf)]
                if stem in self.fa_words or stem in self.user_fa_words:
                    return True

        # Colloquial verb ending patterns (e.g. میرم, میری, میره, میشینیم, نمیدونم)
        colloquial_endings = ["م", "ی", "ه", "یم", "ین", "ن", "ند"]
        for end in colloquial_endings:
            if w.endswith(end) and len(w) > len(end) + 2:
                stem = w[:-len(end)]
                if stem in self.fa_words or stem in self.user_fa_words:
                    return True

        return False

    def is_valid_english(self, word: str) -> bool:
        """Determines if a word is a plausible English word using dictionary & morphology."""
        w = word.lower().strip()
        if not w:
            return False
        if w in self.en_words or w in self.user_en_words:
            return True

        # Check multi-word phrase
        parts = w.split(" ")
        if len(parts) > 1:
            if all(self.is_valid_english(p) for p in parts if len(p) >= 2):
                return True

        # Strip suffixes
        for suf in EN_SUFFIXES:
            if w.endswith(suf) and len(w) > len(suf) + 2:
                stem = w[:-len(suf)]
                if stem in self.en_words or stem in self.user_en_words:
                    return True
                # e.g., 'hoping' -> 'hope'
                if (stem + "e") in self.en_words:
                    return True
                # e.g., 'stopping' -> 'stop'
                if len(stem) > 2 and stem[-1] == stem[-2] and stem[:-1] in self.en_words:
                    return True

        # Strip prefixes
        for pref in EN_PREFIXES:
            if w.startswith(pref) and len(w) > len(pref) + 2:
                stem = w[len(pref):]
                if stem in self.en_words or stem in self.user_en_words:
                    return True

        return False

    def english_vowel_ratio(self, word: str) -> float:
        """Returns the ratio of vowels in an English string."""
        letters = [c for c in word if c.isalpha()]
        if not letters:
            return 0.0
        vowels = [c for c in letters if c in EN_VOWELS]
        return len(vowels) / len(letters)

# Global dictionary singleton
dictionary = Dictionary()
