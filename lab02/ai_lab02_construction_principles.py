# CSE325-2026-L02-M4RB
# =============================================================================
# AI LAB 02 : Software Construction Principles with AI
# BEFORE (messy) vs AFTER (refactored) grade-averaging code + behaviour tests
# Run: python ai_lab02_construction_principles.py   (or: pytest ai_lab02_construction_principles.py)
# NOTE: Replace the BEFORE code with YOUR OWN cold code (40+ lines) for real submission.
# =============================================================================

import contextlib
import io

QUALITY_BASELINE = {"before_max_cc": 17, "before_duplicate_blocks": 3, "before_params": 6}


def banner(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ============================ BEFORE (messy) =================================
# CSE325-2026-L02-M4RB-T1
def run_before(rows, verbose, flag, mode, extra, path):
    d = {}
    for r in rows:
        p = r.split(",")
        if len(p) < 2:
            continue
        d[p[0].strip()] = [int(x) for x in p[1:]]
    out = []
    for name in d:
        m = d[name]
        avg = sum(m) / len(m)
        if avg >= 85:
            g = "A"
        elif avg >= 70:
            g = "B"
        elif avg >= 55:
            g = "C"
        else:
            g = "F"
        out.append((name, avg, g))
    for name, avg, g in out:
        if avg >= 85:
            lg = "A"
        elif avg >= 70:
            lg = "B"
        elif avg >= 55:
            lg = "C"
        else:
            lg = "F"
        print(f"{name}: {avg:.1f} ({lg})")
    passed = 0
    for name, avg, g in out:
        if avg >= 85:
            x = "A"
        elif avg >= 70:
            x = "B"
        elif avg >= 55:
            x = "C"
        else:
            x = "F"
        if x != "F":
            passed += 1
    print(f"Passed: {passed}/{len(out)}")


# ============================ AFTER (accepted fixes only) ====================
# CSE325-2026-L02-M4RB-T3
GRADE_BOUNDARIES = ((85, "A"), (70, "B"), (55, "C"))


def letter_grade(average: float) -> str:
    for minimum, letter in GRADE_BOUNDARIES:
        if average >= minimum:
            return letter
    return "F"


def load_records(rows):
    student_records = {}
    for row in rows:
        parts = row.split(",")
        if len(parts) < 2:
            continue
        student_records[parts[0].strip()] = [int(x) for x in parts[1:]]
    return student_records


def calculate_average(marks):
    return sum(marks) / len(marks)


def print_report(student_records):
    passed = 0
    for name, marks in student_records.items():
        average = calculate_average(marks)
        grade = letter_grade(average)
        print(f"{name}: {average:.1f} ({grade})")
        if grade != "F":
            passed += 1
    print(f"Passed: {passed}/{len(student_records)}")


# Signature kept so existing callers do not break (rejected suggestion: drop the
# 5 unused parameters -> would change the public API).
def run_after(rows, verbose=None, flag=None, mode=None, extra=None, path=None):
    print_report(load_records(rows))


# ============================ TASK 4: same tests on BOTH =====================
# CSE325-2026-L02-M4RB-T4
def capture(fn, rows):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(rows, False, None, None, None, None)
    return buf.getvalue()


IMPLEMENTATIONS = {"before": run_before, "after": run_after}


def test_normal_report():
    for fn in IMPLEMENTATIONS.values():
        assert capture(fn, ["Ali,90,80", "Sara,60,50"]) == \
            "Ali: 85.0 (A)\nSara: 55.0 (C)\nPassed: 2/2\n"


def test_boundaries():
    for fn in IMPLEMENTATIONS.values():
        out = capture(fn, ["X,70", "Y,69", "Z,85", "W,84"])
        assert "X: 70.0 (B)" in out and "Y: 69.0 (C)" in out
        assert "Z: 85.0 (A)" in out and "W: 84.0 (B)" in out


def test_failing_and_malformed_rows():
    for fn in IMPLEMENTATIONS.values():
        assert capture(fn, ["Z,10,20", "badrow"]) == "Z: 15.0 (F)\nPassed: 0/1\n"


def run_tests():
    banner("TASK 4: same unmodified tests against BEFORE and AFTER")
    for t in (test_normal_report, test_boundaries, test_failing_and_malformed_rows):
        try:
            t()
            print("PASS (before & after):", t.__name__)
        except AssertionError as e:
            print("FAIL:", t.__name__, e)


# ============================ Reports ========================================
def show_before_after():
    banner("Sample output (identical for both versions)")
    rows = ["Ali,90,80", "Sara,60,50", "Umar,40,30"]
    print("--- before ---")
    print(capture(run_before, rows), end="")
    print("--- after ---")
    print(capture(run_after, rows), end="")


def show_decisions():
    banner("TASK 2: accept / reject table (edit reasons to match YOUR LLM's real critique)")
    table = [
        ("split the long run() into functions", "ACCEPT",
         "run_before does parsing, grading and printing in one ~45-line body"),
        ("rename `d` to student_records", "ACCEPT",
         "`d` is used across the whole function and hides what it holds"),
        ("extract duplicated grade ladder into letter_grade()", "ACCEPT",
         "the A/B/C/F if-chain is copy-pasted 3 times"),
        ("remove unused params verbose/flag/mode/extra/path", "REJECT",
         "changes run()'s public signature and would break existing callers"),
        ("rename loop variables r, p, m to long names", "REJECT",
         "cosmetic; each loop is 3-6 lines and obvious"),
    ]
    for s, v, r in table:
        print(f"- {s:<55} | {v:<6} | {r}")
    print("\nMeasured against the construction baseline. CSE325-2026-L02-M4RB")


def show_measure_commands():
    banner("TASK 1 & 3: real measurement commands (run in terminal, paste output VERBATIM)")
    print("pip install ruff radon pytest\n"
          "ruff check --select E,F,B,S,UP,RUF ai_lab02_construction_principles.py\n"
          "radon cc -s -a ai_lab02_construction_principles.py\n"
          "radon raw ai_lab02_construction_principles.py\n"
          "git add . && git commit -m 'baseline + original file'   # BEFORE asking the LLM\n"
          "git diff --stat <baseline_hash> <after_hash>\n\n"
          "Sample numbers from my run of this sample: max cyclomatic complexity 17 -> 3,\n"
          "duplicate grade blocks 3 -> 0, worst-function params 6 -> 6 (unchanged on purpose:\n"
          "kept for API compatibility -- explain that in Task 3).")


if __name__ == "__main__":
    show_before_after()
    run_tests()
    show_decisions()
    show_measure_commands()
