from tools.meterproof.check_adr_scores import inspect_markdown


TABLE = """\
| Criterion | Weight | Why | Option 0 | A |
|---|---:|---|---:|---:|
| Correctness | 50 | Finds defects | 2 | 4 |
| Simplicity | 50 | Easy to maintain | 4 | 2 |
| **Weighted total / 5** | **100** | | **3.00** | **3.00** |
"""


def test_accepts_correct_weighted_table():
    errors, details = inspect_markdown(TABLE)

    assert errors == []
    assert details == ["table 1: weights=100; Option 0=3.00, A=3.00"]


def test_rejects_wrong_weighted_total_with_option_detail():
    errors, _ = inspect_markdown(TABLE.replace("**3.00** | **3.00**", "**3.00** | **3.50**"))

    assert errors == ["table 1: A computed 3.00, stated 3.50"]
