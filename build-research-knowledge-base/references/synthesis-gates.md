# Evidence Matrix and Synthesis Gates

## Evidence Matrix Fields

Record at least:

- source and stable identifier;
- research object;
- inputs and boundary conditions;
- method type;
- intermediate state or bridge variable;
- output;
- validation method;
- directly supported claim;
- unsupported or overstrong claim;
- evidence grade;
- venue tier and verification basis;
- formal admission status;
- role in the project.

## Coverage Audit

Answer:

- Does every mainline segment have direct or explicitly indirect evidence?
- Are classic, recent, original-method, standard, and counterexample sources covered?
- Which results conflict, and do object/condition differences explain the conflict?
- Which conclusions are limited to a material, geometry, scale, loading, temperature, or time range?
- Is the matrix overly dependent on one team, method, or source type?
- Do core conclusions rely on direct, methodologically credible, and sufficiently independent evidence?
- Is venue uncertainty recorded where it matters to selection or policy?
- Do all main-method papers pass the configured full-text, relevance, method-completeness, validation, and asset gates?

## Gap-Filling Triggers

Return to search when:

- a priority main-method paper lacks full text;
- a core claim is supported only by an abstract or secondary source;
- a mainline segment lacks direct evidence;
- counterexamples, validation, standards, or limits are missing;
- recent work is clearly absent;
- a core claim relies only on weak, indirect, or poorly validated work;
- venue rank is unresolved or contradictory and the task contract makes it decision-relevant;
- a required search channel is incomplete.

## Synthesis-Ready Gate

Allow a unified conclusion only when:

1. priority-0 full-text gaps are zero or explicitly unavailable with impact recorded;
2. each core claim has direct full-text evidence;
3. important claims have independent support where feasible;
4. mainline, major method/material families, validation, and failure boundaries are covered;
5. formal evidence meets any project-defined source or venue floor;
6. main-method papers pass the configured relevance, method, validation, and asset gates;
7. all required search channels are logged and merged;
8. remaining gaps are explicit experimental questions or future tasks.

## Unified Conclusion Rules

- Answer the research question before presenting details.
- Synthesize by mechanism or method family, not paper-by-paper chronology.
- Separate high-confidence conclusions, engineering decisions, and pending validation.
- State whether an end-to-end chain is directly closed or assembled from segmented evidence.
- Support negative conclusions such as the absence of a general equation.
- List claims the current evidence cannot support.
- Rebuild from the latest evidence matrix; do not append a literature list to an old conclusion.
- Do not use venue tier as a proxy for claim support. If evidence is weak, indirect, disputed, or poorly validated, weaken the claim and state the limitation.

## Delivery State

Use the lowest passing state:

- `draft`
- `evidence-complete`
- `synthesis-ready`
- `mainline-ready`
- `partial`
- `blocked`
