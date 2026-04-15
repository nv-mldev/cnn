# Project

MODE: tutorial

## Vision: From Pixels to Transformers to VLMs

This project builds a **complete tutorial series** that takes you from "I know basic math" all the way to understanding Vision-Language Models — covering every layer of the stack with first-principles depth.

The journey: **pixels → math foundations → why pixels fail → convolutions → CNNs → attention → transformers → VLMs**

### Target Audience
- Engineers/scientists entering computer vision or ML
- People who can code Python but lack the imaging/math foundations
- Self-learners who want deep understanding, not just API calls

### Pedagogical Approach
- **First principles:** physics → math → code → visualization
- **Sensor-grounded:** every math concept is motivated by a real imaging problem
- **Think Bayes style:** simulation-heavy, build intuition through code before formulas
- **One concept per notebook:** no mixing topics

## Notebook Structure

### Part I — Foundations (pixels and the math you need)

| # | Notebook | Theme | Builds toward |
|---|----------|-------|---------------|
| 00 | Introduction to Digital Images | Sensor physics, sampling, quantization | Understanding what a pixel actually is |
| 01 | Linear Algebra for Images | Vectors, norms, dot product, projections, transforms | Comparing image patches, basis for everything ahead |
| 02 | Probability for Sensors | Bernoulli→Binomial→Poisson→Normal→CLT | Why sensor noise is Gaussian, noise budgets |
| 03 | Why Not Pixels | Physics model → affine model → normalisation → ceiling → features | Why raw pixels fail and what replaces them |

### Part II — Learning Features (convolutions to CNNs)

| # | Notebook | Theme | Builds toward |
|---|----------|-------|---------------|
| 04 | Convolutions & Filtering | Kernels, edge detection, feature maps | The operation CNNs are built on |
| 05 | Optimisation & Backprop | Gradient descent, chain rule, computational graphs | How networks learn |
| 06 | CNNs | LeNet → AlexNet → modern architectures | Learned hierarchical features |
| 07 | Training in Practice | Data augmentation, regularisation, transfer learning | Making CNNs work on real problems |

### Part III — Attention and Beyond (transformers to VLMs)

| # | Notebook | Theme | Builds toward |
|---|----------|-------|---------------|
| 08 | Sequence Modelling & Attention | Self-attention, positional encoding | The mechanism behind transformers |
| 09 | Vision Transformers | Patch embeddings, ViT, comparison with CNNs | Transformers applied to images |
| 10 | Vision-Language Models | CLIP, contrastive learning, multimodal embeddings | Connecting vision and language |

*Part II and III are roadmap — notebooks will be built incrementally.*

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
