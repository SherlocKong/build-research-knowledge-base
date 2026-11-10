# Repository Structure

Use this structure as a target, not as a requirement to create every empty directory.

```text
<sub-kb>/
├── AGENTS.md
├── README.md
├── raw/
│   ├── README.md
│   ├── papers/
│   ├── standards/
│   ├── technical/
│   └── text/
├── manifest/
│   └── sources.json
└── kb/
    ├── index.md
    ├── questions/
    │   └── 待解决问题.md
    ├── sources/
    │   ├── index.md
    │   └── <source-card>.md
    ├── readers/
    │   ├── index.md
    │   └── <main-paper>/
    │       ├── paper.md
    │       ├── source_map.json
    │       ├── translation_notes.md
    │       └── assets/
    └── research/
        ├── 问题树与调研层次.md
        ├── 检索策略与日志.md
        ├── 溯源与全文状态.md
        ├── 全文证据矩阵.md
        ├── 文献质量审计与补齐状态.md
        ├── 统一总结与结论.md
        └── <研究主线>V1.md
```

## File Responsibilities

- `raw/`: immutable originals and deterministic extractions. Never overwrite an original.
- A directory directly containing `raw/` is a knowledge-base root. Keep project ancestors and the complete relative tree when mapping it into another tool.
- `raw/papers/`: default destination for original research papers; `raw/standards/` and `raw/technical/` retain their separate source roles. Existing files under other `raw/` branches keep their physical locations.
- `manifest/sources.json`: machine-readable source inventory and state.
- `kb/sources/`: one canonical card per admitted source.
- `kb/readers/`: only main-method or explicitly high-weight papers.
- `kb/research/`: question tree, search log, evidence matrix, synthesis, and mainline documents.
- `tmp/`: repository-local, task-specific temporary OCR/render/crop output; never index it as a formal asset.

## Reuse Rules

1. Search by DOI, normalized title, filename, SHA-256, and source-card links before copying a paper.
2. Reuse a canonical local PDF across sub-libraries through relative links when repository policy permits.
3. Record reuse relationships in the manifest and source card.
4. Do not silently move or rename user assets. Update all inbound links when an authorized move is necessary.
5. Preserve existing dirty-worktree changes and unrelated files.

## Initialization Rules

- Read all applicable `AGENTS.md` files first.
- Use `scripts/init_research_kb.py` for a safe baseline.
- Create only directories and templates required by the current stage.
- Keep project-specific constraints in the nearest applicable `AGENTS.md`.
- Do not put research-specific papers or reports inside the reusable Skill folder.

## Folder-Tree Interoperability

Identify the knowledge-base root before interpreting its content paths. A selected root may itself be a knowledge base. Within its `raw/` tree, a deeper folder named `raw` is an ordinary content folder, not another knowledge-base boundary. Separate knowledge bases outside that content tree retain their own roots.

Preserve intermediate directories, distinguish same-named folders by their full relative paths, and use the same root context for single-file import and batch discovery. Keep `raw/papers/` as the standard paper destination when configuring an optional reference-manager integration. This Skill can be used independently of such an integration.
