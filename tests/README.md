# Regression tests for the coppe class

This directory holds smoke tests that exercise public APIs of `coppe.cls`.
Each `.tex` file is meant to compile cleanly (no LaTeX errors, no new warnings)
under the standard pipeline:

```
pdflatex <file>.tex && biber <file> && pdflatex <file>.tex && pdflatex <file>.tex
```

The test files depend on the class living in `../src/`, the bibliography
fixture in `../src/example.bib`, and the cover logos in `../src/`. The runner
script `run-tests.ps1` sets `TEXINPUTS` so pdflatex finds them all from this
directory.

## Running the suite

From `tests/`:

```powershell
.\run-tests.ps1                  # run all tests
.\run-tests.ps1 test_brazilian_one_advisor   # run a single test by stem name
```

The script invokes pdflatex with `-halt-on-error`, so any LaTeX error aborts
that test and is reported in the summary at the end.

## What each file tests

| File | Purpose |
|------|---------|
| `test_brazilian_one_advisor.tex`    | Cover and folha de rosto with exactly **one** `\advisor`. Regression guard for the historical single-orientador rendering bug. |
| `test_brazilian_two_advisors.tex`   | Same with **two** `\advisor` calls (the "Orientadores" plural label kicks in). Full brazilian-main thesis feature sweep — see file header. |
| `test_brazilian_three_advisors.tex` | Same with **three** `\advisor` calls — the maximum the class is expected to typeset reasonably on the COPPE/UFRJ cover. |

## Adding new tests

Drop a new `.tex` file in this directory. Keep it self-contained (use
`example.bib` for citations, use `coppe-logo.pdf` / `ufrj-logo.pdf` as
figure stand-ins). Reuse the brazilian-main scaffold from the existing
tests as a starting point. Then re-run `run-tests.ps1` — it auto-discovers
every `test_*.tex` in the folder.

A new test should fail *before* the fix and pass *after*, so it stays
green forever.
