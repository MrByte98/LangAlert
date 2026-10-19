"""
Character N-Gram Language Model and Perplexity Scoring Engine.
Uses interpolated Trigram and Bigram statistics with Laplace smoothing
to determine whether arbitrary text (including slang, proper nouns, and novel words)
statistically belongs to the Persian or English linguistic system.
"""
import math
import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, Tuple, Optional

from .converter import convert_en_to_fa, convert_fa_to_en, is_english_char, is_persian_char

import sys

_meipass = getattr(sys, "_MEIPASS", None)
if _meipass:
    DATA_DIR = Path(_meipass) / "langswitch" / "dictionaries"
    if not DATA_DIR.exists():
        DATA_DIR = Path(_meipass) / "dictionaries"
else:
    DATA_DIR = Path(__file__).parent / "dictionaries"

NGRAM_EN_FILE = DATA_DIR / "ngram_en.json"
NGRAM_FA_FILE = DATA_DIR / "ngram_fa.json"

class CharNgramModel:
    """Interpolated Character Trigram + Bigram Language Model."""
    def __init__(self, lang: str):
        self.lang = lang
        self.unigrams: Dict[str, int] = defaultdict(int)
        self.bigrams: Dict[str, int] = defaultdict(int)
        self.trigrams: Dict[str, int] = defaultdict(int)
        self.bigram_contexts: Dict[str, int] = defaultdict(int)
        self.trigram_contexts: Dict[str, int] = defaultdict(int)
        self.total_chars = 0
        self.vocab = set()
        self._is_loaded = False

    def train(self, words_list):
        for w in words_list:
            clean = w.strip().lower()
            if not clean:
                continue
            seq = f"^^{clean}$"
            for c in seq:
                self.vocab.add(c)
                self.unigrams[c] += 1
                self.total_chars += 1

            for i in range(len(seq) - 1):
                bi = seq[i:i+2]
                ctx = seq[i]
                self.bigrams[bi] += 1
                self.bigram_contexts[ctx] += 1

            for i in range(len(seq) - 2):
                tri = seq[i:i+3]
                ctx = seq[i:i+2]
                self.trigrams[tri] += 1
                self.trigram_contexts[ctx] += 1

        self._is_loaded = True

    def save_to_file(self, path: Path):
        data = {
            "lang": self.lang,
            "total_chars": self.total_chars,
            "vocab": list(self.vocab),
            "unigrams": dict(self.unigrams),
            "bigrams": dict(self.bigrams),
            "trigrams": dict(self.trigrams),
            "bigram_contexts": dict(self.bigram_contexts),
            "trigram_contexts": dict(self.trigram_contexts),
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def load_from_file(self, path: Path) -> bool:
        if not path.exists():
            return False
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.total_chars = data["total_chars"]
            self.vocab = set(data["vocab"])
            self.unigrams = defaultdict(int, data["unigrams"])
            self.bigrams = defaultdict(int, data["bigrams"])
            self.trigrams = defaultdict(int, data["trigrams"])
            self.bigram_contexts = defaultdict(int, data["bigram_contexts"])
            self.trigram_contexts = defaultdict(int, data["trigram_contexts"])
            self._is_loaded = True
            return True
        except Exception as e:
            print(f"[NgramModel] Error loading {path}: {e}")
            return False

    def score(self, text: str) -> float:
        """
        Calculates the normalized log-probability of a string under this model.
        Higher (closer to 0) means more statistically natural.
        """
        clean = text.strip().lower()
        if not clean:
            return -20.0

        seq = f"^^{clean}$"
        if len(seq) < 3:
            return -20.0

        v_size = max(1, len(self.vocab))
        total_log_prob = 0.0
        steps = 0

        lambda_tri = 0.60
        lambda_bi = 0.30
        lambda_uni = 0.10
        alpha = 0.05

        for i in range(len(seq) - 2):
            tri = seq[i:i+3]
            bi_ctx = seq[i:i+2]
            bi = seq[i+1:i+3]
            uni_ctx = seq[i+1]
            char = seq[i+2]

            # Trigram probability with smoothing
            tri_c = self.trigrams.get(tri, 0)
            tri_ctx_c = self.trigram_contexts.get(bi_ctx, 0)
            p_tri = (tri_c + alpha) / (tri_ctx_c + alpha * v_size)

            # Bigram probability with smoothing
            bi_c = self.bigrams.get(bi, 0)
            bi_ctx_c = self.bigram_contexts.get(uni_ctx, 0)
            p_bi = (bi_c + alpha) / (bi_ctx_c + alpha * v_size)

            # Unigram probability with smoothing
            uni_c = self.unigrams.get(char, 0)
            p_uni = (uni_c + alpha) / (self.total_chars + alpha * v_size)

            # Interpolated probability
            p_interp = (lambda_tri * p_tri) + (lambda_bi * p_bi) + (lambda_uni * p_uni)
            total_log_prob += math.log(max(p_interp, 1e-12))
            steps += 1

        return total_log_prob / max(1, steps)


class BilingualNgramEvaluator:
    """Bilingual evaluator for Persian vs English keystroke likelihood."""
    def __init__(self):
        self.en_model = CharNgramModel("en")
        self.fa_model = CharNgramModel("fa")
        self._ensure_models()

    def _ensure_models(self):
        loaded_en = self.en_model.load_from_file(NGRAM_EN_FILE)
        loaded_fa = self.fa_model.load_from_file(NGRAM_FA_FILE)

        if not loaded_en or not loaded_fa:
            self._train_and_cache()

    def _train_and_cache(self):
        # Load words from dictionaries to build initial n-gram statistics
        en_words_path = DATA_DIR / "en_words.json"
        fa_words_path = DATA_DIR / "fa_words.json"

        if en_words_path.exists():
            with open(en_words_path, "r", encoding="utf-8") as f:
                en_words = json.load(f)
                # Sample up to 25,000 words for optimal speed & accuracy
                self.en_model.train(en_words[:25000])
                self.en_model.save_to_file(NGRAM_EN_FILE)

        if fa_words_path.exists():
            with open(fa_words_path, "r", encoding="utf-8") as f:
                fa_words = json.load(f)
                self.fa_model.train(fa_words[:20000])
                self.fa_model.save_to_file(NGRAM_FA_FILE)

    def evaluate_en_keystrokes_for_persian(self, text: str) -> Tuple[bool, float, float, float]:
        """
        Evaluates a string typed in English layout.
        Returns (is_mismatch, confidence, en_score, fa_score).
        """
        clean = text.strip()
        if len(clean) < 3:
            return (False, 0.0, -99.0, -99.0)

        # Score as English
        en_score = self.en_model.score(clean)

        # Convert to Persian and score under Persian model
        fa_text = convert_en_to_fa(clean)
        fa_score = self.fa_model.score(fa_text)

        # Difference: fa_score - en_score
        diff = fa_score - en_score

        if diff >= 0.90:
            conf = min(0.99, 0.78 + (diff * 0.08))
            return (True, conf, en_score, fa_score)
        elif diff >= 0.60:
            return (True, 0.82, en_score, fa_score)

        return (False, 0.0, en_score, fa_score)

    def evaluate_fa_keystrokes_for_english(self, text: str) -> Tuple[bool, float, float, float]:
        """
        Evaluates a string typed in Persian layout.
        Returns (is_mismatch, confidence, fa_score, en_score).
        """
        clean = text.strip()
        if len(clean) < 3:
            return (False, 0.0, -99.0, -99.0)

        # Score as Persian
        fa_score = self.fa_model.score(clean)

        # Convert to English and score under English model
        en_text = convert_fa_to_en(clean)
        en_score = self.en_model.score(en_text)

        diff = en_score - fa_score

        if diff >= 0.80:
            conf = min(0.99, 0.78 + (diff * 0.08))
            return (True, conf, fa_score, en_score)
        elif diff >= 0.35:
            return (True, 0.82, fa_score, en_score)

        return (False, 0.0, fa_score, en_score)

# Global evaluator singleton
ngram_evaluator = BilingualNgramEvaluator()
