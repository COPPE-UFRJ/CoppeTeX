# CoppeTeX Examples Registry

Documents each `example#.pdf` / `example#.tex` used to demonstrate and prove the
CoppeTeX bibliography (and later, float/caption) features.

**Convention:** `example<N>.tex` compiles to `example<N>.pdf`; `N` is the example
number described in the table below.

| # | File | Demonstrates | Status |
|---|------|--------------|--------|
| 0 | `example0.pdf` | **Baseline.** Current (pre-change) build of the original `example.tex`, using the legacy BibTeX + natbib bibliography (`coppe-unsrt`). Captured before any CoppeTeX 4.0 bibliography change so later builds can be diffed to prove *only* the bibliography changed (todo §20). | baseline captured |

_Examples 1+ are added during implementation (Stage 4): each exercises specific
reference types and citation styles under the new BibLaTeX/biber ABNT engine._
