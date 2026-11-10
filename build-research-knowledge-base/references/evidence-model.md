# Evidence Model

Represent evidence with five independent fields. Never overload one grade to mean full-text status, source authority, venue prestige, and claim usability simultaneously.

## `asset_status`

- `fulltext_parsed`: full text acquired and parsed.
- `fulltext_unparsed`: full text acquired but not yet parsed.
- `metadata_only`: title, abstract, landing page, or search result only.
- `pending_fulltext`: high-relevance candidate awaiting full text.
- `excluded`: duplicate, irrelevant, inadmissible, or otherwise excluded.

## `source_type`

- `peer_reviewed`
- `thesis`
- `preprint`
- `standard`
- `official_documentation`
- `institutional_technical`
- `secondary`

## `evidence_grade`

- `A`: full text checked for a peer-reviewed paper, thesis, or formal standard.
- `B`: full text checked for authoritative official, institutional, or vendor technical material.
- `C`: presentation, public post, promotion, or other secondary material.
- `M`: metadata or abstract only.

This grade describes evidence form, not journal/conference quality.

## `claim_admissibility`

- `conclusion`: may support a formal conclusion within recorded boundaries.
- `background_only`: may provide context but not a method-strength conclusion.
- `candidate_only`: discovery material awaiting gates.
- `excluded`: must not support the deliverable.

## `venue_quality`

Use an object:

```json
{
  "venue_name": "Canonical journal or conference name",
  "venue_type": "journal",
  "tier": "high",
  "ranking_systems": [
    {
      "name": "JCR",
      "year": 2025,
      "result": "Q1",
      "evidence_url": "https://example.org/record"
    }
  ],
  "verified_at": "2026-07-26",
  "admission_floor_passed": true,
  "assessment_note": "Field-specific rationale"
}
```

Allowed tiers:

- `top`
- `high`
- `acceptable`
- `low`
- `unknown`
- `not_applicable`

## Admission Logic

A source may support a formal conclusion only when:

- the available asset is sufficient to verify the type of claim being made;
- `evidence_grade` is appropriate for the source type and claim;
- `claim_admissibility` is `conclusion`;
- the checked source supports the exact object, condition, and claim strength;
- known limitations, conflicts, and provenance are recorded.

Detailed paper claims normally require `fulltext_parsed` and grade `A`. Standards and authoritative official material may support claims under grade `B` when version, scope, and authority are verified.

Venue quality is an independent context field. Apply `venue_quality.admission_floor_passed` only when the user or repository policy defines a venue floor. Otherwise, use relevance, directness, methodology, validation, and source independence for admission, and record uncertain venue metadata without suppressing otherwise useful evidence.

A main-method paper requires direct relevance, reconstructable methods, adequate validation, stated limits, and more transfer value than alternatives. Apply a `top/high` requirement only when configured by the task contract.

Standards and official documentation use `not_applicable` for venue tier and are assessed by issuing authority, version, scope, and normative status.

## Status Discipline

- Keep unresolved venue quality as `unknown`.
- Keep unavailable full text as `pending_fulltext` or `metadata_only`.
- Retain exclusion reasons.
- Downgrade the deliverable only when a missing field matters to the requested claim or task contract.
