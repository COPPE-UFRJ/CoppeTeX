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
| `test_assinaturas.tex`              | The `assinaturas` option: one signature rule per board member, as Annex D of the manual shows. |
| `test_assinaturas_7.tex`            | The same with a **seven-member** board — the size at which the folha de aprovação used to spill onto a second sheet, and print a folio on it. |
| `test_coorientador.tex`             | The `coorientador` option: coadvisors on all three abstract pages, with two of them so the plural label is exercised. |
| `test_pdfa.tex`                     | The pre-textual pages reshaped for the 2026 manual — folha adicional with the Coleta CAPES fields, approval sheet of 3.1.2.1.3, optional institution argument — under the `pdfa` option. Validated by veraPDF in the harness. |
| `test_sumario.tex`                  | The sumário: the graphic treatment of all five levels, the single title column, what a two-line title does, and a block that forces two-digit indicatives at every level — the shape that used to print the number over the title. |
| `test_semserifa.tex`                | The `semserifa` option together with `pdfa`: the question is not whether a sans-serif document compiles but whether it is still PDF/A. Validated by veraPDF in the harness. |

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
runs veraPDF over the resulting PDFs: `test_pdfa` and `test_semserifa`. A test
that asks for the `pdfa` class option belongs on that list — add it to the
`Build-Tex` calls and to `$veraTargets` there.

None of this is distributed. The suite proves the class works; it is not part
of it, and it does not come out of `coppe.dtx`. The whole proof runs from
[`tools/prova.ps1`](../tools/prova.ps1).
