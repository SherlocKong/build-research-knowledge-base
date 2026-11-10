# Build Research Knowledge Base

面向科研工作的知识库构建与维护 Agent Skill：将原文、来源卡、证据矩阵、阅读资产和研究结论组织成可追溯、可检查、可持续更新的本地知识库。

支持新建、扩展、审计、修复、迁移和综合现有知识库。任务规模由研究问题和交付范围决定，已有资产可以持续复用。

## 核心能力

- 分开记录全文状态、来源类型、证据等级、主张准入和期刊会议背景。
- 将关键主张对应到原文正文、图、表、公式或标准条款。
- 区分文献事实、本项目设计和待验证假设。
- 为主方法论文组织原文、来源卡、详细阅读资产及双向链接。
- 检查来源清单、检索渠道、相对链接、顺序编码引用和公式符号说明。
- 使用中文模板记录检索、证据矩阵和研究主线。

## 安装

将仓库中的 [build-research-knowledge-base](build-research-knowledge-base/) 目录复制到 Agent 的 skills 目录。

以 Codex 的常用目录为例，在 macOS 或 Linux 终端中运行：

```bash
git clone https://github.com/SherlocKong/build-research-knowledge-base.git
mkdir -p ~/.codex/skills
cp -R build-research-knowledge-base/build-research-knowledge-base ~/.codex/skills/
```

Windows 用户可通过文件管理器将该目录复制到用户目录下的 `.codex/skills/`。安装后的入口应为 `.codex/skills/build-research-knowledge-base/SKILL.md`。已有同名安装时，先备份原目录，再用新版本替换。

也可从 [Releases](https://github.com/SherlocKong/build-research-knowledge-base/releases) 下载带版本号的 ZIP，解压后复制其中的 skill 目录。

## 使用示例

```text
使用 $build-research-knowledge-base，为这个研究主题建立知识库。
先检查已有资料，确定范围与关键问题，再组织原文、来源卡和证据矩阵。
```

```text
使用 $build-research-knowledge-base，审计现有知识库的关键结论、证据来源和链接。
本轮先给出问题清单与具体位置。
```

```text
使用 $build-research-knowledge-base，将这些新增论文纳入现有知识库，
复用已保存的原文，更新证据矩阵和受影响的结论。
```

普通文献检索、单篇论文阅读或语言润色，交给对应工具；需要组织或维护长期研究资产时使用本 skill。

## 知识库结构与树识别

```text
research-topic/
├── AGENTS.md
├── raw/
│   ├── papers/
│   ├── standards/
│   ├── technical/
│   └── text/
├── manifest/
│   └── sources.json
└── kb/
    ├── questions/
    ├── sources/
    ├── readers/
    └── research/
```

直接包含 `raw` 的目录是知识库根。`raw/papers` 是论文原文的默认目的地；标准和技术资料分别使用对应分支。已有文件按实际相对目录保留，中间目录和不同祖先下的同名分支分别识别。

与其他工具映射目录树时，先定位知识库根，再解释其内容路径。`raw` 内部再次出现的同名文件夹作为内容层级处理。完整目录职责见 [repository-structure.md](build-research-knowledge-base/references/repository-structure.md)。

初始化只创建基础目录与模板，研究内容由实际证据逐步填充：

```bash
python3 ~/.codex/skills/build-research-knowledge-base/scripts/init_research_kb.py \
  ./research-topic --project-name "研究主题"
```

需要研究主线模板时添加 `--with-mainline`。初始化重复运行会保留已有文件。

## 运行要求与可选集成

- Python 3.10 或更新版本；随附脚本只使用 Python 标准库。
- 能读取本地文件的 Agent；需要外部证据时使用当前环境可用的搜索、全文获取及 PDF 工具。
- 默认优先使用 Codex 内置搜索；AnySearch 为按需补充渠道。
- [subskill-routing.md](build-research-knowledge-base/references/subskill-routing.md) 中列出的学术 skills 是可选集成，按当前环境能力选用。

配套 Zotero 插件另行发布。这个版本可以独立完成知识库组织、模板初始化和结构检查。

## 检查工具

在 skill 目录内执行；将参数换成待检查知识库的路径：

| 脚本 | 检查内容 |
| --- | --- |
| `scripts/validate_manifest.py` | 来源清单字段、状态及重复 DOI |
| `scripts/audit_search_channels.py` | 检索渠道、状态及合并记录 |
| `scripts/audit_venue_quality.py` | 来源质量背景与配置要求 |
| `scripts/audit_local_links.py` | 本地 Markdown 链接 |
| `scripts/audit_citations.py` | 顺序编码制引用与参考文献对应 |
| `scripts/audit_formula_closure.py` | 展示公式附近的符号说明线索 |
| `scripts/kb_status.py` | 知识库结构状态与未完成项 |

```bash
python3 scripts/validate_manifest.py /path/to/research-topic/manifest/sources.json
python3 scripts/audit_local_links.py /path/to/research-topic
python3 scripts/kb_status.py /path/to/research-topic
```

检查脚本用于发现结构问题。主张是否被原文支持、公式符号是否完整、研究综合是否成立，仍由 Agent 结合原文逐项核验。

## 开发验证

在仓库根目录运行：

```bash
python3 -m unittest discover -s tests -v
```

测试覆盖初始化与文件保留、特殊项目名、错误清单、DOI 重复、检索状态、链接、引用和公式检查。

## 许可证

本项目采用 [MIT License](LICENSE)。
