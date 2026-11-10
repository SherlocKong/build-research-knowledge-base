# Academic Citation, Formula, Link, and Ownership Rules

## Citations

- Use one citation system within a document: numeric or author–year.
- Place citations immediately after method claims, quantitative values, mechanisms, limitations, and standards requirements.
- Make every in-text citation correspond to exactly one bibliography entry or an unambiguous author–year entry.
- Prefer DOI, source-card, and local-PDF links in the reference asset chain.
- Do not support method-strength claims with search snippets, abstracts, or secondary summaries.
- Verify that the cited body text supports the same object, conditions, and claim strength.

## Claim–Evidence–Ownership Audit

For each substantive paragraph ask:

1. Who owns this claim?
2. Is it literature fact, project synthesis/design, or pending validation?
3. Does the cited source directly support it?
4. Are object, boundary conditions, and strength aligned?
5. Has a recombination inspired by sources been incorrectly attributed to one paper?
6. Has a literature contribution been presented as project novelty?

Fail the document if readers must infer ownership from context.

## Formula Closure

Immediately after every display equation:

- add a “式中” explanation or a unique adjacent symbol table;
- define every variable, function, constant, index, superscript, subscript, set, domain, vector/tensor/font distinction, operator, sign convention, unit, and dimensionless quantity;
- restate symbols briefly even when previously defined, or point to one unique adjacent symbol table;
- distinguish reused letters such as thickness and time;
- identify the evidence source and project-added abstraction for a newly defined project equation.

Plain-text flow arrows need no symbol table unless they contain mathematical or abbreviated variables.

## Link Rules

- Use clickable relative Markdown links for local assets.
- Validate links after moving or renaming assets.
- Encode spaces correctly through Markdown targets.
- Do not count inline code paths as links.
- Keep temporary OCR/render paths out of formal documents.

## Manual Checks Beyond Scripts

Scripts can find:

- malformed or unmatched numeric citations;
- likely display equations without nearby “式中” text;
- missing local links;
- manifest field and enum failures.

Scripts cannot prove:

- that a citation semantically supports a claim;
- that every mathematical symbol was correctly interpreted;
- that a paper is important or novel;
- that a project synthesis is scientifically justified.

Perform manual review before `mainline-ready`.
