"""
Test suite for Character N-Gram Statistical Language Model.
Verifies detection on slang, novel words, names, and out-of-dictionary terms.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, ".")

from langswitch.ngram_model import ngram_evaluator
from langswitch.detector import detector

print("=" * 60)
print("TESTING N-GRAM STATISTICAL LANGUAGE MODEL")
print("=" * 60)

# 1. Test direct N-gram scoring
test_cases_en_to_fa = [
    "sghl",      # سلام
    "o,fd",      # خوبی
    "xxhvd",     # چطوری / ططاری
    "chk",       # چک
    "rfjl",      # رفتم
    "dhn",       # یاد
]

for w in test_cases_en_to_fa:
    is_m, conf, en_s, fa_s = ngram_evaluator.evaluate_en_keystrokes_for_persian(w)
    assert is_m, f"Failed N-gram mismatch on EN: {w}"
    print(f"✓ EN Keystroke [{w}]: is_mismatch=True, conf={conf:.2f}, EN={en_s:.2f}, FA={fa_s:.2f}")

test_cases_fa_to_en = [
    "پخاشپپشی",  # mohammad
    "قثظش",      # reza
    "اثممخ",     # hello
    "فثسف",      # test
    "پغذشزنثدی", # mybackend
]

for w in test_cases_fa_to_en:
    is_m, conf, fa_s, en_s = ngram_evaluator.evaluate_fa_keystrokes_for_english(w)
    assert is_m, f"Failed N-gram mismatch on FA: {w}"
    print(f"✓ FA Keystroke [{w}]: is_mismatch=True, conf={conf:.2f}, FA={fa_s:.2f}, EN={en_s:.2f}")

# 2. Test End-to-End Detector with N-Gram model on novel words
novel_words = [
    ("پخاشپپشی", "fa", "mohammad"),
    ("قثظش", "fa", "reza"),
    ("sghl", "en", "سلام"),
    ("سلام", "fa", None),  # Normal Persian should be silent
    ("hello", "en", None), # Normal English should be silent
]

print("\n--- End-to-End Detector Results ---")
for text, layout, expected in novel_words:
    res = detector.evaluate(text, active_layout=layout)
    if expected is not None:
        assert res is not None, f"Expected detection for {text}"
        assert expected in res.converted_text, f"Expected {expected} in {res.converted_text}"
        print(f"✓ DETECTED: [{text}] ({layout}) -> [{res.converted_text}] (conf: {res.confidence:.2f})")
    else:
        assert res is None, f"Expected silence for {text}"
        print(f"✓ SILENT: [{text}] ({layout})")

print("\nALL N-GRAM MODEL TESTS PASSED SUCCESSFULLY! ✨")
