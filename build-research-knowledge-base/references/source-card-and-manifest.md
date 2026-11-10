# Source Card and Manifest

## Canonical Identity

Use normalized DOI as the primary key. If unavailable, use normalized title plus first author and year. Record aliases and reused local paths rather than duplicating a source.

## Required Manifest Fields

Each source entry should include:

- `id`
- `title`
- `authors`
- `year`
- `doi`
- `source_type`
- `asset_status`
- `evidence_grade`
- `claim_admissibility`
- `venue_quality`
- `priority`
- `is_main_method`
- `source_url`
- `local_pdf`
- `local_text`
- `source_card`
- `reader`
- `sha256`
- `exclusion_reason`
- `notes`

Use repository-relative POSIX paths. Use empty strings or arrays consistently; do not invent paths.

## Source Card Sections

1. Standard bibliographic record.
2. Evidence and asset status.
3. Venue quality, ranking evidence, year, and admission decision.
4. DOI/standard identifier/official URL.
5. Local PDF, extracted text, page count, and SHA-256.
6. Full-text scope checked.
7. Method or experimental chain.
8. Reusable direct evidence with page/figure/table/equation anchors.
9. Contribution to the research mainline.
10. Applicability and non-transferable boundaries.
11. Author contribution versus project interpretation.
12. Main-method reader links when applicable.

## Source Card Gate

- A candidate source may have a card when it helps durable tracking, but label it `candidate_only` and do not treat metadata or an abstract as verified body evidence.
- Do not exclude a paper solely because venue tier is `low` or `unknown`; record the uncertainty and apply a venue floor only when the task contract defines one.
- Keep candidate, excluded, and conclusion-admissible states visibly distinct.
- Locate important claims in the body.
- Use explicit author subjects for reported work.
- Write project transfer or synthesis in a separate section.

## Link Closure

For an ordinary source:

- manifest → PDF and source card;
- source card → PDF and manifest identity.

For a main-method source:

- mainline → reader, source card, PDF;
- reader → source card, PDF;
- source card → reader, PDF;
- manifest → PDF, source card, reader.

Run link auditing after any rename or move.
