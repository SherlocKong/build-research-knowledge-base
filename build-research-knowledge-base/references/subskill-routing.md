# Subskill Routing

Read the current `SKILL.md` of every named installed skill before invoking it. These summaries define routing, not a substitute for the subskill’s own instructions.

The named skills are optional integrations. Discover what is installed in the current environment; when one is absent, use available tools to produce the same required assets and checks, and record any capability that remains unavailable. The core knowledge-base workflow and bundled Python scripts work independently of these integrations.

## Search Capabilities

### Codex Built-In Search

- Position: first external search layer.
- Use for: broad discovery, primary-source lookup, recent developments, standards, official sources, counterexamples, and venue verification.
- Deposit: queries, URLs, candidate metadata, and unresolved checks in the search log.
- Boundary: snippets and abstracts remain discovery evidence.

### `anysearch` (conditional)

- Position: optional independent search after built-in search.
- Use for: alternate query coverage, academic vertical lookup, missed-source discovery, and result cross-checking.
- Deposit: new/duplicate/conflicting/missing results and failures in the same log.
- Boundary: use when explicitly requested, when built-in search is unavailable or insufficient, when vertical search materially helps, or for justified high-accuracy cross-checking. Its optional absence does not make the task `partial`.

### Local Repository Inspection

- Position: required for an existing local repository, run before and after external search.
- Use for: DOI/title/hash deduplication, canonical asset reuse, stale-card detection, and cross-library reconciliation.
- Deposit: reuse, upgrade, duplicate, conflict, and gap records.
- Boundary: local presence does not imply full-text, venue, or semantic admission.

## Recommended Academic Skills

### `nature-academic-search`

- Stage: search and candidate registration.
- Use for: multi-source scholarly search, Crossref/PubMed/arXiv coordination, DOI verification, MeSH strategy, and `.nbib/.ris/.bib` management.
- Boundary: does not replace required repository inspection or claim verification; metadata remains candidate evidence.

### `pdf:pdf`

- Stage: full-text acquisition and main-paper asset creation.
- Use for: extraction, OCR, rendering, page inspection, figures, tables, and formulas.
- Boundary: successful parsing does not establish venue quality or claim support.

### `nature-reader`

- Stage: main-method high-weight asset creation.
- Use for: full-paper Chinese–English readers, page/block anchors, figure/table awareness, source maps, terminology, and translation notes.
- Boundary: first pass the task contract's main-method gate; keep author meaning separate from project interpretation.

### `nature-writing`

- Stage: synthesis and mainline drafting.
- Use for: argument architecture, claim–evidence planning, section drafting, and calibrated scientific prose.
- Boundary: invoke only after the synthesis gate; never invent results, references, or novelty.

### `nature-citation`

- Stage: specialized citation work.
- Use when: the target explicitly requires Nature/CNS style or specified Nature Portfolio source scope.
- Boundary: do not force general knowledge-base searches into a Nature-only source set.

### `nature-polishing`

- Stage: final English expression after evidence, claims, and citations stabilize.
- Use for: Nature-leaning academic English and claim-strength control.
- Boundary: does not search, select main papers, repair evidence, or invent arguments.

### Optional Nature Skills

- `nature-figure`: use only for submission-grade scientific figures or figure audits.
- `nature-data`: use only for data-availability statements, repositories, dataset citations, or FAIR metadata.

## Orchestration Contract

Before invoking a subskill, provide:

- current stage;
- input assets and canonical paths;
- output path;
- required quality gates;
- prohibited assumptions.

After it returns:

- deposit results in the manifest, log, source card, reader, matrix, or mainline;
- run this Skill’s admission and audit gates;
- record failures and downgrade status instead of silently substituting lower-quality work.
