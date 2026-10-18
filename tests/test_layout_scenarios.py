import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, ".")
from langswitch.detector import detector

# Test scenarios with active layout
tests = [
    # (text, active_layout, should_alert, expected_converted)
    ("سلام", "fa", False, None),
    ("سلام چطوری", "fa", False, None),
    ("این یک تست است و فونت وزیر استفاده شده", "fa", False, None),
    ("اثممخ", "fa", True, "hello"),
    ("فثسف", "fa", True, "test"),
    ("صخقمی", "fa", True, "world"),
    ("hello", "en", False, None),
    ("hello world", "en", False, None),
    ("sghl", "en", True, "سلام"),
    ("o,fd", "en", True, "خوبی"),
    ("sghl ]x,vd", "en", True, "سلام چطوری"),
]

for text, layout, should_alert, exp_conv in tests:
    res = detector.evaluate(text, active_layout=layout)
    if should_alert:
        assert res is not None, f"Expected alert for [{text}] with layout [{layout}], but got None!"
        assert exp_conv in res.converted_text, f"Expected [{exp_conv}] in [{res.converted_text}]"
        print(f"✓ PASS (Alerted as expected): [{text}] (layout={layout}) -> [{res.converted_text}]")
    else:
        assert res is None, f"Did NOT expect alert for [{text}] with layout [{layout}], but got [{res.converted_text}]!"
        print(f"✓ PASS (Correctly silent): [{text}] (layout={layout})")

print("\nALL SCENARIOS PASSED!")
