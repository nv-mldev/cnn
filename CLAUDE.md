# Project

MODE: tutorial

## Vision: Bridging the Gap to CS231n

This project builds a **foundational tutorial series** that bridges the gap between "I know basic math" and "I can follow Stanford CS231n (or equivalent deep learning for vision courses)."

CS231n and similar courses assume you already understand:
- How images are formed physically (sensors, photons, noise)
- Why pixel-level comparison fails and what normalisation fixes
- Probability distributions and why sensor noise is Gaussian
- Linear algebra as it applies to image operations
- The motivation for learned features over hand-crafted ones

**This series covers that missing foundation** — starting from photon physics, through probability and linear algebra, to the doorstep of deep learning. Every concept is grounded in the sensor/signal/noise domain, not abstract math.

### Target Audience
- Engineers/scientists entering computer vision or ML
- People who can code Python but lack the imaging/math foundations
- Self-learners preparing for CS231n, fast.ai, or similar courses

### Pedagogical Approach
- **First principles:** physics → math → code → visualization
- **Sensor-grounded:** every math concept is motivated by a real imaging problem
- **Think Bayes style:** simulation-heavy, build intuition through code before formulas
- **One concept per notebook:** no mixing topics

## Notebook Structure

| # | Notebook | Theme | Builds toward |
|---|----------|-------|---------------|
| 00 | Introduction to Digital Images | Sensor physics, sampling, quantization | Understanding what a pixel actually is |
| 01a | Probability for Sensors | Bernoulli→Binomial→Poisson→Normal→CLT | Why sensor noise is Gaussian, noise budgets |
| 01b | Linear Algebra for Matching | Vectors, norms, dot product, projections, transforms | The math behind template matching normalisation |
| 02 | Why Not Pixels | Physics model → affine model → normalisation → limitations → features | Why raw pixels fail and what comes next |
| (future) | ... | CNNs, feature learning, backprop | CS231n territory |

## Rules

- Prioritize readability and learning flow over strict standards
- Verbose variable names over concise ones
- Heavy inline comments explaining the "why" not just the "what"
- Structure: intuition → math → code → visualization
- One concept per notebook — don't combine topics
- Use sensor/imaging examples to ground every concept

## Wiki (Karpathy LLM Wiki Pattern)

This project maintains a persistent, compounding wiki at `wiki/`. The wiki is entirely LLM-maintained — the human curates sources and asks questions, the LLM does all summarizing, cross-referencing, and maintenance.

### Architecture

- **`tutorials/`** — Raw sources. Immutable. Never modified by wiki operations.
- **`wiki/`** — LLM-maintained knowledge base.
  - `index.md` — Content catalog. Every page listed with link + one-line summary. LLM reads this first when answering queries.
  - `log.md` — Append-only chronological record. Format: `## [YYYY-MM-DD] operation | Title`
  - `concepts/` — One page per concept (e.g. `sampling.md`, `snr.md`). Definition, why it matters, equations, cross-references, source citations.
  - `sources/` — One summary page per ingested tutorial/document.
  - `synthesis/` — Cross-cutting analysis, comparisons, evolving thesis pages.

### Wiki Operations (via /wiki-ingest, /wiki-query, /wiki-lint skills)

- **Ingest**: Read source → discuss with user → create source summary + concept pages → update index + log
- **Query**: Read index → find relevant pages → synthesize answer → optionally file as new page
- **Lint**: Check for orphans, dead links, stale pages, missing concepts, weak cross-references

### Wiki Conventions

- One concept per page — never combine topics
- Cross-link using Obsidian wikilinks: `[[concept_name]]` or `[[concept_name|Display Text]]`
- Flag contradictions: `> ⚠️ Contradicts [other_page]: ...`
- Filenames: lowercase, underscores, no spaces
- Frontmatter on every page: `tags`, `sources`, `last_updated`
- MathJax for equations: inline `$...$`, display `$$...$$`
- Ground every concept in a real imaging/sensor problem
