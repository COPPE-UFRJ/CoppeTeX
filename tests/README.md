# Regression tests for the coppe class

> **`src/coppe.dtx` is the single source of the class.** The tests in this
> folder are the exception: they are written by hand and are NOT generated from
> it. But the `coppe.cls` they exercise IS generated — so a fix you make while
> chasing a failing test goes into `src/coppe.dtx`, never into `src/coppe.cls`,
> which is overwritten at the next generation. See
> [`../src/README.md`](../src/README.md).

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
| `test_banca.tex`                    | The board as v4.1 declares it: treatment in the optional argument, institution as the last mandatory one. Mixes a member with a treatment, one without, and one with an **empty** institution, so a regression in any of the three shows up. The approval sheet must come out with no signature rules. |
| `test_orientadorexamina.tex`        | The other side of the same sheet: the `orientadorexamina` option puts advisors and coadvisors back on the board, ahead of the examiners. Also the only test with **no** `\dataaprovacao`, so the sheet must read "a ser determinada" rather than draw a rule. `test_banca.tex` declares a comparable board without the option and must come out with the examiners alone. |
| `test_banca_7.tex`                  | The same with a **seven-member** board — the size at which the folha de aprovação used to spill onto a second sheet, and print a folio on it. |
| `test_coorientador.tex`             | The `coorientador` option: coadvisors on all three abstract pages, with two of them so the plural label is exercised. |
| `test_pdfa.tex`                     | The pre-textual pages reshaped for the 2026 manual — folha adicional with the Coleta CAPES fields, approval sheet of 3.1.2.1.3, mandatory institution argument — under the `pdfa` option. Validated by veraPDF in the harness. |
| `test_sumario.tex`                  | The sumário: the graphic treatment of all five levels, the single title column, what a two-line title does, and a block that forces two-digit indicatives at every level — the shape that used to print the number over the title. |
| `test_listas.tex`                   | The lists of abbreviations and of symbols: **no page numbers and no dot leaders** (4.1.1), the optional sort key that puts `IoT` and `eMBB` in alphabetical order, and a description long enough to wrap, which used to break badly before a trailing folio. Needs `makeindex -s ../src/coppe.ist`; `build-check.ps1` runs it. |
| `test_comserifa.tex`                | The `comserifa` option together with `pdfa`. Sans serif is the default since v4.1, so this test guards the other road: the question is not whether a serif document compiles but whether it is still PDF/A. Validated by veraPDF in the harness. |

## Adding new tests

Drop a new `.tex` file in this directory. Keep it self-contained (use
`example.bib` for citations, use `coppe-logo.pdf` / `ufrj-logo.pdf` as
figure stand-ins). Reuse the brazilian-main scaffold from the existing
tests as a starting point. Then re-run `run-tests.ps1` — it auto-discovers
every `test_*.tex` in the folder.

A new test should fail *before* the fix and pass *after*, so it stays
green forever.

Two of these tests are also built and validated by
[`tools/build-check.ps1`](../tools/build-check.ps1) in its `pdfa` scope, which
runs veraPDF over the resulting PDFs: `test_pdfa` and `test_comserifa`. A test
that asks for the `pdfa` class option belongs on that list — add it to the
`Build-Tex` calls and to `$veraTargets` there.

None of this is distributed. The suite proves the class works; it is not part
of it, and it does not come out of `coppe.dtx`. The whole proof runs from
[`tools/prova.ps1`](../tools/prova.ps1).
