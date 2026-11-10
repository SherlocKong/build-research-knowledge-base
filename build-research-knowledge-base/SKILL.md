---
name: build-research-knowledge-base
description: Build, extend, audit, or repair a durable, evidence-traceable scientific research knowledge base. Trigger only when the user explicitly asks to create/build/establish, maintain/extend, audit, migrate, or repair a research knowledge base, literature knowledge base, evidence repository, or an existing repository clearly serving that role. Do not trigger for ordinary literature searches, literature reviews, paper discovery or reading, citation lookup, manuscript writing or polishing, research summaries, evidence synthesis, or file organization unless the user explicitly frames the requested work as knowledge-base work.
---

# Build Research Knowledge Base

## Objective

Create or maintain a reusable research repository in which sources, claims, local assets, and synthesized conclusions can be traced and updated. Scale the workflow to the requested outcome; do not turn a small repair or audit into a full literature program.

## Establish the Task Contract

1. Read applicable repository and subdirectory `AGENTS.md` files before writing.
2. Inspect the existing repository, if any, with `rg --files`, targeted `rg` queries, manifests, DOI/title matches, and current reports.
3. Classify the task as `create`, `extend`, `audit`, `repair`, `migrate`, or `synthesize`.
4. Record the research scope, requested deliverables, source constraints, quality policy, available search channels, and completion criteria. Infer reasonable defaults when low risk; ask only when a missing decision would materially change the repository.
5. Preserve raw sources, user files, and unrelated changes. Never overwrite an original paper.

Run only the stages needed by this contract. An audit is read-only unless fixes are requested. A repair need not repeat discovery that remains valid. A synthesis must use the current admitted evidence but need not rebuild unrelated assets.

Read the relevant reference before doing that work:

- Repository creation or migration: [repository-structure.md](references/repository-structure.md)
- Evidence states and claim admission: [evidence-model.md](references/evidence-model.md)
- Venue or publication-quality assessment: [venue-quality.md](references/venue-quality.md)
- External search or gap filling: [search-playbook.md](references/search-playbook.md)
- Source cards or manifests: [source-card-and-manifest.md](references/source-card-and-manifest.md)
- Evidence matrices, coverage, or synthesis: [synthesis-gates.md](references/synthesis-gates.md)
- Mainline documents and high-weight paper assets: [mainline-document.md](references/mainline-document.md)
- Citations, formulas, links, and claim ownership: [academic-format.md](references/academic-format.md)
- Routing work to another installed skill: [subskill-routing.md](references/subskill-routing.md)

## Core Rules

### Keep Evidence Dimensions Separate

Track asset status, source type, evidence grade, claim admissibility, and venue quality independently. Admit a claim because the checked source supports it at the stated boundary and strength—not because the venue is prestigious. Treat venue quality as context or as a gate only when the user or repository policy explicitly requires it.

Search snippets, abstracts, and metadata are discovery evidence. They may have candidate records but must not support detailed method, quantitative, causal, or limitation claims.

### Preserve Claim Ownership

Label substantive content as:

- literature fact, with author attribution and a nearby citation;
- project synthesis or design, with language such as “本项目据此采用/定义/扩展”;
- hypothesis or pending validation, explicitly marked.

Do not attribute a project synthesis to one paper or present a literature contribution as project novelty.

### Make Search Proportionate

When external search is required, use Codex built-in web search first. Inspect the local repository before and after external search when one exists. Use AnySearch only when the user requests it, built-in search is unavailable or insufficient, its vertical search materially improves coverage, or an independent cross-check is justified for high-accuracy work. Add scholarly databases when they match the field.

Log the channels actually used, queries, dates, new results, duplicates, conflicts, failures, and remaining gaps. Do not downgrade otherwise complete work solely because an optional provider was unavailable.

### Close Formal Deliverables

For final documents, use one citation system, clickable asset links, and traceable source locations. After each display equation, define every symbol needed to interpret it in an adjacent “式中” paragraph or symbol table. Apply this rule only to documents and equations in scope.

## Adaptive Workflow

### Inventory and Scope

- Identify canonical paths, duplicates, reusable assets, stale conclusions, and missing links.
- Build a question tree only when it helps discovery or repository navigation.
- Initialize with `scripts/init_research_kb.py` only for a new knowledge base and only with structures needed now.

### Discover and Register

- Search only the branches required by the task contract.
- Deduplicate by normalized DOI; otherwise use normalized title plus first author and year.
- Register candidates early with explicit states instead of hiding incomplete or excluded sources.
- Acquire legal full text for claims that require body-level verification; preserve the original and record extraction/OCR state.

### Evaluate Sources and Claims

- Create one canonical source card per source when a card adds durable value. Candidate cards are allowed when visibly labeled and must not be cited as verified evidence.
- Locate reusable claims in the body, figure, table, equation, or standard clause.
- Assess relevance, directness, methods, validation, limitations, conflicts, and independence. Verify venue quality only when it affects selection, policy, or user requirements.

### Build the Evidence View

- Map sources to objects, conditions, methods, outputs, validation, supported claims, unsupported extrapolations, and project role.
- Record contradictory evidence and external-validity limits rather than forcing consensus.
- Re-enter search only for material gaps relative to the task contract.

### Synthesize and Package

- Regenerate conclusions from the current evidence view; do not mechanically append new papers to an old conclusion.
- Separate supported findings, project decisions, limitations, and open questions.
- Create detailed bilingual readers, figure/table extraction, or main-method packages only when requested or when the repository contract defines them as high-value assets.
- Select “main-method” sources primarily for direct relevance, reconstructability, validation, and transfer value. Apply a venue-tier floor only when explicitly configured.

## Validation and Delivery

Run only applicable validators, resolving the Skill directory before invoking them:

```bash
python3 scripts/validate_manifest.py <sources.json>
python3 scripts/audit_search_channels.py <检索策略与日志.md> [--require-anysearch]
python3 scripts/audit_venue_quality.py <sources.json>
python3 scripts/audit_local_links.py <knowledge-base-root>
python3 scripts/audit_citations.py <mainline.md>
python3 scripts/audit_formula_closure.py <knowledge-base-root>
python3 scripts/kb_status.py <knowledge-base-root>
```

Treat scripts as structural checks. Manually verify claim–evidence alignment, ownership, scientific relevance, and important omissions. In a Git repository, run `git diff --check`.

Report:

- what changed or was audited;
- the scope-specific checks that passed or failed;
- unresolved evidence gaps and their impact;
- the repository paths of material outputs;
- the next highest-value action, if any.

Use `draft`, `evidence-complete`, `synthesis-ready`, or `mainline-ready` only when those lifecycle labels are useful to the repository. Use `partial` for incomplete requested work, not for a skipped optional channel; use `blocked` only for a real external dependency or required user decision.

## Reusable Resources

- Copy and adapt templates from `assets/`; do not create empty structures speculatively.
- Resolve the directory containing this `SKILL.md` before invoking bundled scripts; the target repository is a separate location.
- Keep research-specific papers and reports out of the reusable Skill folder.
- Use installed search, PDF, reader, citation, writing, or figure skills for their specialized work after reading their current instructions; then deposit outputs into the knowledge base and apply this Skill's evidence rules.
