"""
Bidirectional keyboard layout converter between English (QWERTY) and Persian (Standard & ISIRI 9147).
Handles letters, shifted variants, punctuation, and common platform differences.
"""

# English key to Persian character (unshifted)
EN_TO_FA_NORMAL = {
    'q': 'ض', 'w': 'ص', 'e': 'ث', 'r': 'ق', 't': 'ف', 'y': 'غ', 'u': 'ع', 'i': 'ه', 'o': 'خ', 'p': 'ح',
    '[': 'ج', ']': 'چ', '\\': '\\',
    'a': 'ش', 's': 'س', 'd': 'ی', 'f': 'ب', 'g': 'ل', 'h': 'ا', 'j': 'ت', 'k': 'ن', 'l': 'م',
    ';': 'ک', "'": 'گ',
    'z': 'ظ', 'x': 'ط', 'c': 'ز', 'v': 'ر', 'b': 'ذ', 'n': 'د', 'm': 'پ',
    ',': 'و', '.': '.', '/': '/',
    '`': '‍',
}

# English key to Persian character (shifted)
EN_TO_FA_SHIFT = {
    'Q': 'ْ', 'W': 'ٌ', 'E': 'ٍ', 'R': 'ً', 'T': 'ُ', 'Y': 'ِ', 'U': 'َ', 'I': 'ّ', 'O': ']', 'P': '[',
    '{': '}', '}': '{', '|': '|',
    'A': 'ؤ', 'S': 'ئ', 'D': 'ي', 'F': 'إ', 'G': 'أ', 'H': 'آ', 'J': 'ة', 'K': '»', 'L': '«',
    ':': ':', '"': '؛',
    'Z': 'ك', 'X': 'ط', 'C': 'ژ', 'V': 'ٰ', 'B': '‌', 'N': 'ٔ', 'M': 'ء',
    '<': '>', '>': '<', '?': '؟',
    '~': '÷', '!': '!', '@': '٬', '#': '٫', '$': 'ریال', '%': '٪', '^': '×', '&': '،', '*': '*', '(': ')', ')': '(',
    '_': 'ـ', '+': '+',
}

# Combine unshifted & shifted
EN_TO_FA = {**EN_TO_FA_NORMAL, **EN_TO_FA_SHIFT}

# Also support common Persian keyboard variations:
# In some Iranian layouts, 'm' produces 'ئ' or 'م' and '\' or '~' produces 'پ'.
# We provide smart aliases for fallback conversion:
EN_TO_FA_VARIANTS = {
    '\\': 'پ',
    '~': 'پ',
    'C': 'ژ',
    'c': 'ز',
}

# Reverse mapping: Persian to English
FA_TO_EN = {}
for en_char, fa_char in EN_TO_FA.items():
    if fa_char not in FA_TO_EN:
        FA_TO_EN[fa_char] = en_char

# Additional reverse mappings for Arabic variants / common alternatives
FA_TO_EN.update({
    'ي': 'd',  # Arabic Yeh -> 'd' (same key as Persian 'ی')
    'ك': ';',  # Arabic Kaf -> ';' (same key as Persian 'ک')
    'ة': 'J',  # Teh Marbuta -> Shift+J
    'ژ': 'C',  # Zheh -> Shift+C
    'پ': 'm',  # Peh -> m (standard Persian Windows layout)
    'ء': 'M',
    'أ': 'G',
    'إ': 'F',
    'ؤ': 'A',
    'ئ': 'S',
    'آ': 'H',
    '،': '&',
    '؛': '"',
    '؟': '?',
    '»': 'K',
    '«': 'L',
    '‌': ' ',  # ZWNJ -> space or shift-space
    'ـ': '_',
    '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
    '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
})

def convert_en_to_fa(text: str) -> str:
    """Converts a string typed with English layout to Persian."""
    res = []
    for char in text:
        res.append(EN_TO_FA.get(char, char))
    return "".join(res)

def convert_fa_to_en(text: str) -> str:
    """Converts a string typed with Persian layout to English."""
    res = []
    for char in text:
        res.append(FA_TO_EN.get(char, char))
    return "".join(res)

def is_persian_char(char: str) -> bool:
    """Returns True if the character is in the Arabic/Persian Unicode block."""
    code = ord(char)
    return (0x0600 <= code <= 0x06FF) or (0xFB50 <= code <= 0xFDFF) or (0xFE70 <= code <= 0xFEFF)

def is_english_char(char: str) -> bool:
    """Returns True if the character is ASCII Latin."""
    return char.isascii() and char.isalpha()

def get_script_distribution(text: str) -> dict:
    """Returns the distribution of scripts in the given text."""
    en_count = 0
    fa_count = 0
    other_count = 0
    for c in text:
        if is_english_char(c):
            en_count += 1
        elif is_persian_char(c):
            fa_count += 1
        else:
            other_count += 1
    total = len(text) or 1
    return {
        "en": en_count,
        "fa": fa_count,
        "other": other_count,
        "total": total,
        "predominant": "en" if en_count > fa_count else ("fa" if fa_count > en_count else "neutral")
    }
