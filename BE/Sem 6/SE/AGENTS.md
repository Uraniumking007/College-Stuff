# SE Workspace – Agent Instructions

Instructions for AI agents and contributors working in this Software Engineering (BE Sem 6) workspace. Follow these conventions for `.tex` files, folder structure, and `.md` files.

---

## Folder structure

- **`Practical Format/`**  
  Contains the **LaTeX template only**: `se-practical-format.tex`. Use this as the base for new practicals. Do not put assignment-specific content here.

- **`Practical N/`** (e.g. `Practical 1/`, `Practical 2/`)  
  One folder per practical:
  - Main file: `se-practical-N.tex` (e.g. `se-practical-1.tex`).
  - Optional: `assets/` subfolder for images/diagrams (e.g. `waterfall.png`). If no subfolder is used, images sit next to the `.tex` file.
  - Build artifacts (`.aux`, `.log`, `.pdf`, `.fdb_latexmk`, `.fls`, `.out`, `.synctex.gz`) may be generated here; they are typically gitignored or kept local.

- **Root-level `.md` files**  
  At SE workspace root (same level as `Practical 1/`, `Practical Format/`):
  - **`Practical-N.md`** – Notes, outlines, or draft content for Practical N (can mirror or expand the .tex content).
  - Other `.md` files (e.g. SRS, requirements, project docs) – use descriptive names (e.g. project or topic name).

**Summary:**

```
SE/
├── AGENTS.md
├── Practical-1.md
├── Practical-2.md
├── Practical-3.md
├── Practical Format/
│   └── se-practical-format.tex
├── Practical 1/
│   ├── se-practical-1.tex
│   └── assets/           # optional: diagrams/images
│       └── *.png
├── Practical 2/
│   └── se-practical-2.tex
└── ...
```

---

## LaTeX (`.tex`) format

All practical write-ups follow the **SE practical format** (as per SE-FILE FORMAT): 12pt body, justified text, Times New Roman, A4, with header/footer.

### Document setup

- **Class:** `\documentclass[12pt,a4paper]{article}`
- **Margins:** `\usepackage[margin=1in]{geometry}`
- **Spacing:** `\usepackage{parskip}`, `\usepackage{setspace}`, `\onehalfspacing`
- **Font:** Times New Roman via `\usepackage{mathptmx}` and `\usepackage[T1]{fontenc}`
- **Alignment:** Justified body text: `\usepackage{ragged2e}` and `\justifying`
- **Header/Footer:** `\usepackage{lastpage}`, `\usepackage{fancyhdr}`; header = subject + enrollment number, footer = page number.

### Required user-defined commands (set once per practical)

- **`\enrollmentno`** – Enrollment number (e.g. `240093116002`).
- **`\practicalno`** – Practical number (e.g. `1`, `2`).

Place these in the “SET YOUR DETAILS HERE” block and do not remove the block comment.

### Typography and sections

| Element        | Size  | Usage |
|----------------|-------|--------|
| **Title**      | 16pt  | `\title{\fontsize{16pt}{1.2}\selectfont Practical No.\ \practicalno}` |
| **Aim / main heading** | 16pt | `\section*{\fontsize{16pt}{1.2}\selectfont Aim: ...}` |
| **Subheading** | 14pt  | `\section*{\fontsize{14pt}{1.2}\selectfont ...}` or `\subsection*{\fontsize{14pt}{1.2}\selectfont ...}` |
| **Body**       | 12pt  | `\fontsize{12pt}{1.2}\selectfont` before body, or set once after preamble. |

- Use **`\section*`** and **`\subsection*`** so that section numbers are not auto-inserted unless the format explicitly requires them.
- After the first **Aim** (and any top-level section), set body to 12pt; keep body text justified.

### Optional helpers (from existing practicals)

- **`\sdlcsubsection{Title}`** – Subsection with 14pt title and `\needspace` to reduce bad page breaks before the heading.
- **`labeledlist` environment** – `\begin{labeledlist}{Advantages} ... \end{labeledlist}` for bold label + enumerated list, with `samepage`/`needspace` to keep label and list together.
- **Packages:** `graphicx` (figures), `needspace`, `url`, `hyperref` as needed.

### Figures and paths

- **`\usepackage{graphicx}`** for `\includegraphics`.
- Image path: either filename only (e.g. `waterfall.png`) if the image is in the same directory as the `.tex` file, or path relative to the `.tex` file (e.g. `assets/waterfall.png` if you use an `assets/` subfolder).
- Prefer **local assets** (in `Practical N/` or `Practical N/assets/`) for submission; avoid relying on external URLs in the built PDF.

### Naming and placement

- **Template:** `Practical Format/se-practical-format.tex`.
- **Per-practical main file:** `Practical N/se-practical-N.tex` (e.g. `se-practical-1.tex`).
- Keep each practical self-contained in its folder (one main `.tex`, optional `assets/`).

### Content guidelines

- Copy structure and macros from `Practical Format/` or from an existing `Practical K/se-practical-K.tex` when creating a new practical.
- Preserve the header (subject + enrollment) and footer (page number); do not remove or repurpose them.
- When adding or editing content, keep 12pt justified body, 14pt subheadings, 16pt for title and Aim.

---

## Markdown (`.md`) format

### Practical notes: `Practical-N.md`

- **Location:** SE workspace root (e.g. `Practical-1.md`, `Practical-2.md`).
- **Purpose:** Drafts, outlines, or reference content for Practical N; may mirror or expand the `.tex` content.
- **Structure:**
  - One `# Practical-N` title at the top.
  - Use `##` for main sections (e.g. “Analysis of SDLC Models”).
  - Use `###` for subsections (e.g. model names or topics).
  - Use `#####` for small labels (e.g. “Advantages”, “Disadvantages”, “Best Suitable for Projects”, “Diagram”) when you want a clear hierarchy.
- **Lists:** Use ordered lists (`1.`) for steps/phases and for advantages/disadvantages when order or numbering is desired.
- **Images:** Use Markdown images: `![Alt text](url-or-path)`. For final PDF, prefer copying assets into `Practical N/assets/` and referencing them from the `.tex` file.

### Other `.md` files (SRS, requirements, project docs)

- **Location:** SE workspace root or a dedicated docs folder if you introduce one.
- **Naming:** Descriptive (e.g. project name, “Netlify (Subscription Model)”, “Netflix (Subscription Based Model)”).
- **Structure:** Suited to the document type, for example:
  - **Requirements:** Introduction, Purpose, Product Scope, Functional/Non-Functional Requirements, User Auth, Movie Database, Video Streaming, Payment, Performance, Security, etc.
  - **SRS-style:** Overall Description, External Interface Requirements, System Features, Cost Estimation (e.g. COCOMO with tables).
- **Headings:** Use `#` for title, `##` for major sections, `###` for subsections; keep hierarchy consistent.
- **Tables:** Use standard Markdown tables for coefficients, cost estimates, and comparisons.
- **Code blocks:** Use fenced code blocks for formulas or short snippets (e.g. COCOMO expressions).

### General Markdown conventions

- Use **bold** (`**text**`) for emphasis on terms or section labels where it helps readability.
- Keep list items concise; break long content into paragraphs or sub-lists.
- Prefer clear, consistent heading levels; avoid skipping levels (e.g. don’t jump from `##` to `#####` without `###` and `####` if you need that depth).

---

## Summary for agents

1. **New practical:** Create `Practical N/` and add `se-practical-N.tex` (from `Practical Format/se-practical-format.tex` or by copying an existing practical). Set `\enrollmentno` and `\practicalno`. Use 16pt for Aim, 14pt for subheadings, 12pt justified for body. Put images in the same folder or in `assets/`.
2. **Folder structure:** Do not put assignment-specific content in `Practical Format/`. Keep one main `.tex` per practical in `Practical N/`.
3. **Markdown:** Use `Practical-N.md` at root for practical notes; use other `.md` files for SRS/requirements with clear headings, lists, and tables as above.
