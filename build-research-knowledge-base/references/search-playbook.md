# Proportionate Search Playbook

## Default Order

### Layer 1: Codex Built-In Web Search

Use as the primary external search. Cover:

- terminology and field framing;
- high-level reviews for vocabulary and key-source discovery;
- original method papers;
- recent developments;
- standards and official documentation;
- counterexamples, failures, and applicability limits;
- current journal/conference quality evidence.

Prefer DOI, publisher, learned society, standards body, and author-institution pages for verification.

### Optional Independent Search: AnySearch

Run after Layer 1 only when the user requests it, built-in search is unavailable or insufficient, its vertical search materially improves coverage, or an independent cross-check is justified for high-accuracy work:

- vary terminology, language, and query composition;
- use an academic vertical when it materially improves coverage;
- discover the correct sub-domain before sending vertical required parameters;
- compare new, duplicate, contradictory, and missing results;
- do not repeat identical queries merely to claim cross-checking.

If a required AnySearch run is unavailable, record the failure and impact. If it was optional, continue without downgrading the search.

### Local Repository Cross-Check

When a local repository exists, run twice:

1. Before external search, inventory existing PDFs, manifests, source cards, readers, reports, DOI strings, normalized titles, and exclusion logs.
2. After external search, merge, deduplicate, identify reusable canonical assets, and detect stale cards or newly contradicted conclusions.

Use `rg --files`, `rg -i`, manifest parsing, DOI normalization, title normalization, and hashes.

## Supplemental Academic Search

Use field-specific databases and services such as Crossref, PubMed, arXiv, Semantic Scholar, publisher sites, institutional repositories, or standards organizations when they improve coverage or verification. Prefer `nature-academic-search` for coordinated scholarly retrieval, DOI verification, MeSH work, and `.nbib/.ris/.bib` management.

Metadata and abstracts remain candidate evidence until full-text and venue gates pass.

## Search Log Minimum

For each run record:

- date/time and operator;
- research branch;
- channel and database;
- exact query or local match condition;
- filters and date/language range;
- result count reviewed;
- new candidates;
- duplicates/reused assets;
- conflicts or surprising negatives;
- full-text status;
- venue-check status;
- remaining gap and next action.

## Coverage Groups

Search each applicable group independently:

- direct end-to-end evidence;
- segmented mechanism chain;
- theory/model;
- numerical method;
- experiment/measurement;
- material/object family;
- operating condition and scale;
- validation and uncertainty;
- standard/official workflow;
- negative results and failure boundaries;
- classic and recent work.

## Stop Rule

Do not stop by paper count. Stop when the task contract is satisfied and:

- all required channels are complete and merged;
- priority full-text gaps are zero or their effect is recorded;
- each core claim has direct evidence and important claims have independent cross-support where feasible;
- mainline branches, validation, and counterexamples are covered;
- any configured venue floors are satisfied;
- main-method papers pass the configured relevance, method, validation, and asset gates;
- further targeted search has low expected value or no longer changes the conclusion materially;
- remaining gaps are explicit experiments or future tasks.
