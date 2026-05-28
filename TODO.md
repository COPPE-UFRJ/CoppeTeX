# TODO — open items toward the CoppeTeX v4.0 final release

Items below remain open at the time of submitting the v4.0 multilingual
proposal to the CPGP. They are not blockers for the proposal itself —
the artifacts already in this branch are complete enough for CPGP
review — but they should be closed before the v4.0 release is published
on CTAN and Overleaf.

---

## 1. Open the Pull Request (was item #5)

**Status:** pending.

Open a Pull Request from `nlinguas` to `master` on the GitHub
repository at <https://github.com/COPPE-UFRJ/CoppeTeX>. The PR body
should include, in this order:

- The content of [`CARTA_CPGP.md`](./CARTA_CPGP.md) as the opening
  cover text;
- A short link to the section "`nlinguas` branch — new proposal for
  CPGP" in [`README.md`](./README.md);
- Links to the typeset PDFs: [`NORMA_COPPE_2026.pdf`](./NORMA_COPPE_2026.pdf),
  `dist/coppe.pdf`, `dist/example_{pt,en,es,fr,it}.pdf`,
  `dist/covers_5languages.pdf`;
- A "How to review" footnote pointing reviewers at the four implementation
  commits (`775db80`, `a363bc6`, `466302a`, `bfd0b5d`) so the diff is
  intelligible step-by-step.

`gh` (GitHub CLI) is not currently installed in the local environment.
The PR has to be opened from the GitHub web UI by a maintainer with
write access.

A pre-filled comparison URL is available at:
<https://github.com/COPPE-UFRJ/CoppeTeX/compare/master...nlinguas>

---

## 2. Native-speaker review of the language packs (was item #6)

**Status:** pending.

The Spanish, French and Italian translations in:

- `src/coppe-lang-{spanish,french,italian}.def`
- `src/{spanish,french,italian}-coppe.lbx`

were drafted with reasonable care but **without revision by native
speakers**. Specific points that deserve attention:

### Spanish (`coppe-lang-spanish.def`, `spanish-coppe.lbx`)

- `frame` is rendered as `Cuadro`. Some Spanish academic traditions
  prefer `Recuadro` or `Marco` for what ABNT calls "quadro".
  Recommend confirming with a native speaker familiar with the
  graduate-thesis conventions.
- `depositor` is `Solicitante`; cross-check with Spanish-language
  patent-law terminology.
- `mscdiss` is `Tesis de Maestr\'ia`; some institutions use
  `Tesina` or `Trabajo de Fin de M\'aster`.

### French (`coppe-lang-french.def`, `french-coppe.lbx`)

- `frame` is rendered as `Encadr\'e`. Alternatives include
  `Tableau-cadre` or simply `Tableau` followed by the ABNT-style
  caption. Native-speaker preference depends on field.
- `directedby` (for movies/videos) is `R\'ealis\'e par`. Confirm.
- `tcc` is `M\'emoire de fin d'\'etudes` — confirm against current
  French academic terminology (it may map to `M\'emoire de licence`
  or `M\'emoire de fin d'\'etudes` depending on the institution).

### Italian (`coppe-lang-italian.def`, `italian-coppe.lbx`)

- `advisor`/`advisors` rendered as `Relatore`/`Relatori`. Some Italian
  institutions distinguish `Relatore`/`Correlatore`/`Tutor`; check
  whether the COPPE/UFRJ "Orientador" should map to `Relatore` or to
  a more specific term.
- `frame` as `Riquadro`: confirm.

### Recommended workflow

1. Identify one COPPE/UFRJ student or staff member fluent in each of
   the three languages.
2. For each language, generate `dist/example_<lang>.pdf` and ask the
   reviewer to mark up the strings they would change.
3. Apply the corrections in the corresponding `.def`/`.lbx` files in
   `src/coppe.dtx`, regenerate with `pdflatex coppe.ins`, commit and
   push.

---

## 3. CTAN release planning (was item #11)

**Status:** pending CPGP approval.

Once the CPGP approves v4.0:

- Tag the final commit on `master` as `v4.0` (in addition to the
  current `v4.0-rc1` release-candidate tag on `nlinguas`).
- Prepare a CTAN submission package containing `dist/` contents plus
  the source files in `src/coppe.dtx` and `src/coppe.ins`. The CTAN
  page <https://ctan.org/pkg/coppe> currently hosts the v3.x line;
  v4.0 is a clean replacement.
- Update the CTAN-side `README` and the catalogue entry to mention the
  multilingual model.
- After CTAN propagation (typically 24–48h), update the README to
  point users to the CTAN install path as the recommended one.

---

## 4. Overleaf availability (was item #13)

**Status:** pending.

Provide CoppeTeX 4.0 as a directly-usable template on Overleaf so that
COPPE/UFRJ students who use Overleaf (the majority, in practice) can
start a new thesis in any of the five built-in languages without
copying files manually.

### Concrete steps

1. **Create an Overleaf template project** containing:
   - The `dist/` file set (`coppe.cls`, `coppe.bbx`, `coppe.cbx`,
     `coppe.dbx`, `coppe-numeric.bbx`, `coppe-numeric.cbx`,
     `brazilian-coppe.lbx`, `english-coppe.lbx`,
     `spanish-coppe.lbx`, `french-coppe.lbx`, `italian-coppe.lbx`,
     `coppe-lang-spanish.def`, `coppe-lang-french.def`,
     `coppe-lang-italian.def`, `coppe.ist`, `coppe-logo.pdf`,
     `ufrj-logo.pdf`, `latexmkrc`);
   - A copy of `example.tex` (full pt-main example with bibliography
     and lists) as the project's entry point;
   - `example.bib` for the bibliography.
2. **Publish the project as a public template** on
   <https://www.overleaf.com/latex/templates>, in the appropriate
   category ("Thesis" / "Brazilian universities").
3. **Add a button to the README**: a single "Open in Overleaf" link
   that creates a copy of the template for the student.
4. **Companion templates per language** (optional but recommended):
   five smaller template projects, one per main language, each
   starting from `example_<lang>.tex` so the language-specific
   `\titlein` and abstract structure are already in place.

### Notes

- Overleaf reads `latexmkrc` automatically; the existing one in
  `dist/` already configures biber + the makeindex steps for the
  abbreviations and symbols lists. No Overleaf-specific tweaks
  needed.
- The `\usepackage{listings}`, `algorithm2e` and other dependencies
  are all present on the Overleaf TeX Live tree, so no missing-
  package warnings should appear.

---

## 5. Tighten the GitHub presence (was item #14)

**Status:** pending.

A handful of small repository-hygiene improvements that would make the
project more inviting to new contributors and easier to evaluate from
the GitHub web UI:

### Repository metadata

- [ ] Set the **About** section: short tagline ("LaTeX document class
      for COPPE/UFRJ theses and dissertations, multilingual since
      v4.0") + the project website (Overleaf template URL, once
      available).
- [ ] Add **topics**: `latex`, `latex-class`, `thesis`, `dissertation`,
      `brazilian-portuguese`, `multilingual`, `abnt`, `coppe`, `ufrj`,
      `engineering`, `biblatex`.
- [ ] Enable **GitHub Discussions** for user questions (separate from
      Issues, which would stay for bug reports).

### Releases

- [ ] Once the CPGP approves the proposal, create a **GitHub Release**
      for `v4.0` attaching `dist/`-equivalent assets (zip + tar.gz):
      `coppe-v4.0.zip` with the eight built-in `coppe-*` files, the
      three pair of language packs, and the manual; plus the five
      demo PDFs.
- [ ] Tag the release `v4.0`. Replace the current `v4.0-rc1` tag with
      the final tag once approved.

### Documentation surface

- [ ] **Badges in the README**: CTAN version (once published),
      LaTeX-engines tested (pdfLaTeX, LuaLaTeX), licence (GPL-3.0),
      "Open in Overleaf" button.
- [ ] **`SECURITY.md`** (minimal) — even a one-paragraph "report
      security issues by email" is enough.
- [ ] **`CODE_OF_CONDUCT.md`** (Contributor Covenant 2.1 boilerplate
      is fine).
- [ ] Move the historic working notes out of the working tree
      altogether (they currently sit ignored in `InstrucoesClaude/`,
      `LIXO/`, `_scratch/`). At minimum, document their purpose in a
      one-paragraph `WORKING_NOTES.md` for future maintainers.

### CI

- [ ] Set up a **GitHub Actions workflow** that, on every push to
      `master`:
      1. Installs TeX Live + biber;
      2. Runs `pdflatex coppe.ins` and then builds `example.pdf`,
         `coppe.pdf` and the five `example_<lang>.pdf`;
      3. Diffs the rendered pages of `example.pdf` (pt-main) against a
         pinned baseline image and fails if a page changes
         unexpectedly. This codifies the byte-identical regression
         test that has been done manually throughout the v4.0 work.
      4. Uploads the built PDFs as workflow artifacts.

### Issue / PR templates

- [ ] **`.github/ISSUE_TEMPLATE/bug_report.md`** — capture cls
      version, class options, MWE, build log.
- [ ] **`.github/ISSUE_TEMPLATE/language_pack.md`** — for users who
      want a new language pack added; references `CONTRIBUTING.md`.
- [ ] **`.github/PULL_REQUEST_TEMPLATE.md`** — checklist for
      contributors (regenerated `coppe.cls`? `dist/` synced? `\changes`
      entry? smoke documents build?).

---

*Last updated: maio de 2026, on the `nlinguas` branch (v4.0-rc1).*
