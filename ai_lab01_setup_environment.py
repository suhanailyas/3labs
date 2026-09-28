# CSE325-2026-L01-K7QX
# =============================================================================
# AI LAB 01 : Setting Up the AI-Augmented Development Environment
# Hand-written vs AI-assisted Celsius-to-Fahrenheit converter + tests
# Run: python ai_lab01_setup_environment.py     (or: pytest ai_lab01_setup_environment.py)
# =============================================================================

import time

RUN_PROFILE = {"ratio": 9 / 5, "offset": 32}


def banner(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ---------------- TASK 1 / ACTIVITY 1 : hand-written version (branch: main) ----
# CSE325-2026-L01-K7QX-T1
def celsius_to_fahrenheit_by_hand(c):
    return c * RUN_PROFILE["ratio"] + RUN_PROFILE["offset"]


# ---------------- TASK 2 / ACTIVITY 2 : AI-assisted version (branch: ai-build) --
# CSE325-2026-L01-K7QX-T2
def celsius_to_fahrenheit_ai(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit."""
    return celsius * RUN_PROFILE["ratio"] + RUN_PROFILE["offset"]


def parse_celsius(text: str):
    """AI version's defensive input handling: returns float or None if invalid."""
    try:
        return float(text)
    except ValueError:
        return None


# ---------------- The classic bug (Activity 1) shown for comparison ------------
def buggy_integer_division(c):
    return c * (9 // 5) + 32          # 9 // 5 == 1  -> WRONG on purpose


# ---------------- TESTS (pytest-compatible, also run manually below) ----------
def test_known_conversions():
    for fn in (celsius_to_fahrenheit_by_hand, celsius_to_fahrenheit_ai):
        assert fn(100) == 212
        assert fn(0) == 32
        assert fn(-40) == -40
        assert abs(fn(37) - 98.6) < 1e-9


def test_bug_is_detected_by_known_value():
    assert buggy_integer_division(100) != 212      # 100C should be 212F -> bug caught


def test_ai_input_validation():
    assert parse_celsius("36.6") == 36.6
    assert parse_celsius("abc") is None
    assert parse_celsius("") is None


def run_tests():
    banner("TESTS")
    for t in (test_known_conversions, test_bug_is_detected_by_known_value,
              test_ai_input_validation):
        try:
            t()
            print("PASS:", t.__name__)
        except AssertionError as e:
            print("FAIL:", t.__name__, e)


# ---------------- TASK 3 : comparison (timing is REAL, measured here) ----------
def compare():
    banner("TASK 3: side-by-side comparison")
    for c in (100, 0, -40, 37):
        print(f"{c}C -> hand: {celsius_to_fahrenheit_by_hand(c)}F | "
              f"ai: {celsius_to_fahrenheit_ai(c)}F | buggy: {buggy_integer_division(c)}F")
    for bad in ("abc", "36.6"):
        print(f"input {bad!r} -> AI parse result: {parse_celsius(bad)} "
              f"(hand version: float({bad!r}) would {'crash' if parse_celsius(bad) is None else 'work'})")

    start = time.perf_counter()
    for _ in range(100000):
        celsius_to_fahrenheit_by_hand(37)
    print(f"hand version: {time.perf_counter() - start:.4f}s for 100k calls")
    start = time.perf_counter()
    for _ in range(100000):
        celsius_to_fahrenheit_ai(37)
    print(f"AI version  : {time.perf_counter() - start:.4f}s for 100k calls")


# ---------------- TASK 4 : defend one difference ------------------------------
def defend():
    banner("TASK 4: defend one difference")
    print("Largest difference: parse_celsius() (try/except ValueError) in the AI version.\n"
          "It is a real improvement, not just a habit: float('abc') raises ValueError and\n"
          "crashes the hand version, while this line returns None so the caller can re-ask.\n"
          "It costs 4 extra lines but removes a whole class of user-input crashes.\n"
          "(Cite YOUR file:line in the submission, e.g. ai_lab01_setup_environment.py:<line>.)")
    print("\nChecked against the reference run. CSE325-2026-L01-K7QX")


# ---------------- Activity 4 : commit messages to use -------------------------
GIT_STEPS = """
git init cse325-lab01 && cd cse325-lab01
git add hand_written.py && git commit -m "Hand-written converter (found and fixed integer-division bug)"
git checkout -b ai-build
git add ai_assisted.py && git commit -m "AI-assisted converter (float division and input validation from first draft)"
git log --format='%h %ad %s' --date=iso      # paste into report
python -VV                                    # paste into report
(Make >= 3 real commits on main, spaced out during the lab: the timestamps ARE the evidence.)
"""

if __name__ == "__main__":
    banner("LAB 01 - ACTIVITY 1 & 2: both versions")
    print("hand:", celsius_to_fahrenheit_by_hand(100), "| ai:", celsius_to_fahrenheit_ai(100))
    compare()
    run_tests()
    defend()
    banner("ACTIVITY 4: git commands (run these yourself in the terminal)")
    print(GIT_STEPS)
