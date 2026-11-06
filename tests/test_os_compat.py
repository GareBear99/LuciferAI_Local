#!/usr/bin/env python3
"""Regression test for core/os_compat.py.

The file used to contain a bare `try:` with no `except`/`finally` in
OSCompat.display_system_info, so the whole module failed to parse
(SyntaxError) and could not be imported at all. This test compiles and
imports the module and instantiates the compat object.

Run:  python3 tests/test_os_compat.py
Exit code 0 = all pass. No model, no network needed.
"""
import py_compile
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "core"))

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))


def main():
    print("os_compat regression tests\n")
    try:
        py_compile.compile(str(REPO_ROOT / "core" / "os_compat.py"),
                           doraise=True)
        check("os_compat.py compiles", True)
    except py_compile.PyCompileError as e:
        check("os_compat.py compiles", False, str(e))
        print(f"\n0/{len(RESULTS)} passed")
        return 1

    from os_compat import OSCompat, get_os_compat  # noqa: E402
    check("os_compat imports", True)
    compat = get_os_compat()
    check("get_os_compat() returns an OSCompat", isinstance(compat, OSCompat))
    # display_system_info must not raise on this platform (it used to be
    # unreachable entirely because the file did not parse).
    try:
        import io
        from contextlib import redirect_stdout
        with redirect_stdout(io.StringIO()):
            compat.display_system_info()
        check("display_system_info() runs without raising", True)
    except Exception as e:
        check("display_system_info() runs without raising", False, str(e))

    failed = [n for n, ok in RESULTS if not ok]
    print(f"\n{len(RESULTS) - len(failed)}/{len(RESULTS)} passed")
    if failed:
        print("FAILED: " + ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
