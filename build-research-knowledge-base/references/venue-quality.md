# Journal and Conference Quality Gate

## Principle

Treat publication venue as contextual quality evidence, never as proof that a paper supports a claim and never as a universal admission condition. Apply a tier floor only when the user or repository policy explicitly defines one.

## Evaluate by Field

Use current, field-appropriate and independently checkable evidence:

- JCR quartile/category and year;
- Chinese Academy of Sciences partition and year when relevant;
- CCF, CORE, learned-society, or field-recognized conference classifications;
- flagship status and peer-review reputation in the relevant discipline;
- publisher and venue identity, including renamed or similarly named venues;
- retraction, discontinuation, predatory, or quality-control concerns.

Do not use one impact-factor threshold across unrelated disciplines. Do not treat all conferences as weak; in conference-led fields, a top conference can be the primary archival venue.

## Record the Decision

For every admitted paper, record:

- canonical venue name and type;
- `top`, `high`, `acceptable`, `low`, `unknown`, or `not_applicable`;
- each ranking system, year, result, and evidence URL;
- verification date;
- admission decision;
- field-specific rationale and disagreement notes.

Because rankings change, verify them during the task instead of relying on memory.

## Using a Venue Floor

- If the task contract defines a floor, record whether each source passes it and enforce it consistently.
- If no floor is defined, set `admission_floor_passed` according to repository convention or leave the policy decision explicit; do not exclude a source solely for `low` or `unknown` tier.
- Use `unknown` when ranking evidence is unavailable or irrelevant, and state whether that uncertainty affects the claim.
- Assess the paper itself: relevance, directness, methods, data, validation, limitations, retraction status, and independence from other evidence.

## Main-Method Gate

Require all configured conditions, normally:

1. direct relevance to the mainline;
2. sufficient source authority for the intended use;
3. complete full text;
4. reconstructable method or experimental chain;
5. convincing validation and stated limits;
6. more explanatory or transferable value than alternatives;
7. the project venue floor, if one exists.

Reject or qualify as a main method:

- sources that fail an explicit project venue floor;
- unreviewed preprints when the project requires peer-reviewed authority;
- reviews that only summarize an original method;
- promotional or secondary material;
- high-prestige papers that are not directly relevant;
- papers selected only by citation count or search rank.

## Disagreement Handling

- Record conflicting rankings rather than averaging them.
- Prefer the evaluation system recognized by the paper’s actual field.
- Mark ambiguous cases `unknown`; request user judgment only when the decision materially changes the mainline and cannot be resolved from the task contract.
- Keep standards and official documents outside journal/conference tiers; evaluate authority, version, and applicability instead.
