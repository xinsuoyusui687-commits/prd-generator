# PRD Generator

将需求材料、会议结论和已确认规则整理成面向研发、测试与发布人员的实施型 PRD。重点是写清：为什么做、要改什么、不同情况如何处理，以及怎样判断结果正确。

An Agent Skill for implementation-oriented product requirements documents, with Chinese guidelines, an adaptable template, and a complete fictional example.

## 核心能力

- 核对有效版本，区分已确认要求、候选方案与未决事项；遇到关键冲突先澄清。
- 使用背景、方案设计、防控手段、验收标准、沟通过程与决策记录五章，按实际需求裁剪子章节。
- 写清现状与目标、总则与例外、页面权限与接口接收、计算与保存、历史数据及验收。
- 保留数据单位与实际/预估身份，不补造收益、排期、负责人或测试结论。
- 对照正文、表格、流程图、附件和示例，检查它们是否得出同一结果。

这是给编码助手使用的说明与模板，不是自动审批服务。使用 skill 不需要特定 MCP、企业账号、Java 环境或本机 Workflow 目录。

## 安装

发布后，将以下 `https://github.com/xinsuoyusui687-commits/prd-generato` 替换为真实 GitHub 仓库地址。

### Skills CLI

当前已核对的 Skills CLI 需要 Node.js 22.20 或更新版本：

```bash
npx skills add https://github.com/xinsuoyusui687-commits/prd-generato --skill prd-generator
```

默认安装到当前项目，并选择要安装的助手。加 `-g` 可安装到用户级别；先查看可发现的技能可以运行：

```bash
npx skills add https://github.com/xinsuoyusui687-commits/prd-generato --list
```

### Codex 安装请求

目标环境提供 `$skill-installer` 时，可发送：

```text
请使用 $skill-installer，从 GitHub 仓库 https://github.com/xinsuoyusui687-commits/prd-generato 安装 skills/prd-generator。
```

### 手动复制

将整个 `skills/prd-generator/` 复制到目标助手支持的 skills 目录，保留 `references/`、`assets/`、`agents/` 与许可文件。扫描位置以该助手当前说明为准，不能只复制 `SKILL.md`。

## 使用

附加需求材料后发送：

```text
请使用 $prd-generator，根据本次提供的需求材料生成实施型 PRD。
采用已确认的最新规则；关键条件冲突时先指出具体问题。
保留五章结构，裁剪不适用的子章节，不补造收益、排期或测试结果。
输出到当前工作区的 outputs 目录。
```

也可要求修订已有 PRD，或只评审并列出问题。只评审时不自动覆盖原文。

用户指定路径优先；未指定时使用当前项目或任务工作区的 `outputs/<事项>/`。项目已有明确规则时遵从该规则。没有可确定的工作区或写入位置时先确认，不引用维护者个人桌面路径。

## 完整示例

[示例入口](examples/README.md)包含虚构的“资料库按收藏状态筛选”需求、[调用提示](examples/usage-prompt.md)和[预期 PRD](examples/example-prd.md)。该例展示成功有数据、成功无数据、读取失败与权限边界，也展示简单需求如何裁剪计算、迁移等模块。

[澄清示例](examples/clarification-example.md)展示材料冲突时应该提出什么问题。示例业务规则只属于该例，不是所有 PRD 的默认规则。

## 仓库结构

```text
.
├── README.md
├── LICENSE
├── CHANGELOG.md
├── docs/publishing.md
├── examples/
├── scripts/validate.py
├── requirements-dev.txt
├── .github/workflows/validate.yml
└── skills/prd-generator/
    ├── SKILL.md
    ├── LICENSE.txt
    ├── agents/openai.yaml
    ├── references/prd-guidelines.md
    └── assets/prd-template.md
```

技能版本为 0.1.0；规则与模板分别来自生成规范 v1.2、模板 v4.1，并作独立发布适配。源码与个人技能目录不是安装后的依赖。

## 维护与发布

使用 skill 不需要 Python。以下命令仅供维护者检查文件：

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
```

需要 Python 3.10 或更新版本。GitHub Actions 会运行相同检查，覆盖入口元数据、资源完整性、本地链接、五章结构及编码；它不证明生成内容已获业务确认，也不等于系统测试。

上传与版本标签步骤见[发布说明](docs/publishing.md)，变更见[CHANGELOG](CHANGELOG.md)。

## 规范与许可

- [Agent Skills 规范](https://agentskills.io/specification)
- [OpenAI Skills 示例](https://github.com/openai/skills)
- [Skills CLI](https://github.com/vercel-labs/skills)

MIT License，见 [LICENSE](LICENSE)。
