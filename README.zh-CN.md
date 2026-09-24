# Work Charter

[English](README.md)

当前包源码：**[v0.7.1](docs/skills/work-charter/STATE.md#v071-outcome-scoped-authority)**。
正式发布状态见 [GitHub Releases](https://github.com/junwei529/work-charter/releases)，
核验记录见[状态](docs/skills/work-charter/STATE.md)。上一公开版本为 v0.6.5；
中间的 v0.6.6–v0.7.0 候选未单独发布。

让复杂的 AI 项目接得住，也交得出。

Work Charter 是面向 Codex 的项目协作 Skill。它提供 L0–L4 五档协作方案，以及配套的角色分工和模型配置，帮助你从日常任务逐步组织到跨对话、跨角色和多阶段项目。

它会根据项目的连续性、分工和验收需要推荐合适级别，说明收益与成本，由你确认采用。已有且仍适用的工作约定可以继续沿用。

## 五档协作方案，覆盖不同工作需要

| 级别 | 协作方式 | 默认角色 | 解决什么问题 |
|---|---|---|---|
| L0：直接执行 | 按当前任务要求完成工作，不建立 Charter | 主负责人 | 保持日常任务简洁 |
| L1：任务约定 | 在当前对话中明确目标、边界和完成标准 | 主负责人，可按需加入审阅者 | 让本次工作有清晰约定 |
| L2：持续接续 | 增加可持久保存的工作记录与恢复入口 | 主负责人，可按需加入审阅者 | 换对话后仍能接上已有工作 |
| L3：独立分工 | 分开规划、执行与技术审阅 | Planner、Executor、Reviewer | 让实现与评估有明确分工 |
| L4：项目统筹 | 在 L3 基础上增加跨阶段的项目管理 | Orchestrator、Planner、Executor、Reviewer | 协调项目方向、阶段目标和整体验收 |

L1 的约定保留在当前对话中；需要可靠的跨对话恢复时，使用 L2 及以上方案。级别越高，需要维护的协作信息也越多，因此优先选择足够满足需要的一档。

## 默认分工，让每个角色知道自己负责什么

- **Orchestrator｜项目统筹**：负责项目方向、阶段安排和项目层面的验收。
- **Planner｜规划与验收**：明确阶段目标、工作边界和完成标准，评估执行结果。
- **Executor｜执行与验证**：实现获准的工作，完成必要检查并交付结果。
- **Reviewer｜独立技术审阅**：检查实现中的问题，提供可追溯的发现和依据。

L0–L2 的主负责人直接负责当前任务。角色方案本身不会自动创建任务或扩大操作权限。

## 默认模型配置与自定义

作者基于多个实际代码仓库，围绕 Orchestrator、Planner、Executor、Reviewer 各自的分工构建了私有评测集。此前的配置基线参考了这些结果；v0.7.0 按用户决定调整模型和推理等级，不代表新增评测结论。

这些默认值提供一个可直接起步的参考。使用者可以根据项目特点、可用模型、使用成本和实际表现，灵活调整各级别、各角色的模型与推理等级。

用户自定义配置优先于包内默认。调整适用于之后按该配置创建的任务，已有任务保留原设置。

| 适用范围 | 包内默认配置 |
|---|---|
| L0 主负责人及独立触发的临时 Reviewer | Sol · xhigh |
| L1–L2 主负责人及可选 Reviewer | Sol · xhigh |
| L3–L4 Planner | Astra · high |
| L4 Orchestrator | Astra · high |
| L3–L4 Executor | Sol · xhigh |
| L3–L4 Reviewer | Astra · medium |

这里的 Astra 指 `gpt-6-astra`、Sol 指 `gpt-6-sol`，`medium`、`high` 和 `xhigh` 表示推理投入设置。L0 的 Reviewer 配置只在其他独立规则授权该临时角色时提供模型值。

这些是包内预设，实际采用情况需要由任务创建流程核对；完整规则见[默认配置文件](skills/work-charter/assets/role-models.default.yaml)。

## 一个使用场景

一个项目需要分几次对话完成，可以先评估是否采用 L2，保留关键决定、当前状态、验证依据和下一步。

当项目需要独立规划与技术审阅时，再评估 L3 的分工成本；出现多个需要统一协调的阶段时，再考虑 L4。整个过程沿用已有有效决定，并对实质变化作出明确调整。

## 开始使用

```text
$work-charter
这个项目需要分几次对话完成。
请从 L0–L4 中推荐合适的协作级别，
说明默认角色、模型配置，以及收益和维护成本。
```

已有工作约定时：

```text
按现有已批准的 Work Charter 继续项目。
先核对当前状态，再推进下一项已授权工作。
```

[设计](docs/skills/work-charter/DESIGN.md) · [当前状态](docs/skills/work-charter/STATE.md) · [验证](docs/skills/work-charter/VERIFICATION.md) · [评估场景](evals/README.md)

<details>
<summary>技术参考、安装与恢复、版本沿革和历史证据</summary>

本仓库是 `work-charter` 的独立产品仓库。可安装包位于
[`skills/work-charter/`](skills/work-charter/)。它最初由源提交
`80910a8b2375a11be897e9660c4b00a06d00dd13` 物化；当前 repository-native
版本所修改的文件在 source map 中明确分类，不再描述为未改变的迁移 blob。

已接受的 `v0.5.0` source 由不可变 pre-review 快照
[`release/v0.5.0-candidate.json`](release/v0.5.0-candidate.json) 描述。独立的
[`release/v0.5.0-local-release-receipt.json`](release/v0.5.0-local-release-receipt.json)
绑定已接受 source commit `8bf9f130598fbf1b9170dd0c082e3e8fb78d6c0d`、十轮已完成
review、Planner 验收与 exact deterministic qualification。Local source readiness 为
`VERIFIED`；该 receipt 不产生 v0.5.0 安装、runtime role-delivery 或公开发布 claim。

已发布的 [`v0.6.5` 候选](release/v0.6.5-candidate.json)调整上述已批准级别模型默认值，并保留
[v0.6.4 入口修订](release/v0.6.4-candidate.json)。普通任务没有适用
Charter 或材料需求时保持 L0，不为入口检查加载治理参考或创建角色。实际应用规则的角色
完整读取精简后的共同正文，再按当前决定、级别和职责读取详细章节。已有批准的 Charter
继续复用；范围、权限、验收或恢复条件发生材料变化时主动复评并建议，仍由用户决定采纳
或调整级别。Skill 本身不保证所有宿主自动加载，也不提供强制执行能力。
[状态](docs/skills/work-charter/STATE.md#current-v065-local-candidate)和
[验证](docs/skills/work-charter/VERIFICATION.md#current-v065-qualification)记录当前范围与证据限制。
已接受的 [v0.6.3 源码与安装](docs/skills/work-charter/STATE.md#historical-v063-local-candidate)保留为历史证据。

此前 [`v0.6.2` 候选](release/v0.6.2-candidate.json)要求 Agent 为自行推导的护栏说明
具体失败及后果、所需保护强度，以及更简单的现有办法为何不足。辅助工作持续扩大时，
由当前主任务或 Planner 比较剩余成本和达到同一受保护用户结果的更简单路线。
用户及项目明确要求保持原有权威；这两项补充由[合同说明](skills/work-charter/references/coordination-and-recovery.md#contract-and-proposal-changes)承载。
六文件结构、schema1、默认模型及生产安装行为不变。已接受的 v0.6.1 源码和候选保留为历史；
v0.6.2 的验证、审查、安装与推送分别绑定新输入及对应操作边界。

此前本地 `v0.6.0` 候选增加向后兼容的“级别 × 实际职责”配置解析，由
[`release/v0.6.0-candidate.json`](release/v0.6.0-candidate.json) 绑定。
R12 已完成独立技术审查，无新增 findings；Planner 已接受未提交的冻结源码检查点。
[验收记录](docs/skills/work-charter/STATE.md#accepted-v060-source-checkpoint)明确范围和身份；
candidate 保留审查前快照，不表示已提交、local release ready、安装或全局生效。
不可变 v0.5.0 candidate/receipt
只继续作为其 exact bytes 的历史证据。

不可变 v0.4.0 receipt 在其 checkpoint 绑定已接受候选、五个 review 结果与失败的
v0.3-to-v0.4 update：
[`release/v0.4.0-local-release-receipt.json`](release/v0.4.0-local-release-receipt.json)
记录。之后的第六个结果 R6 未发现 source 问题，Planner 验收了先前修正，并以
`df674c773de6f915627af541f0eb37221da9adef` 提交。首次获授权的 actual repair preflight
因 `icacls /restore` 改变 automatic-inheritance 控制状态而停止。v0.4.1 C4 随后以
control-aware exact restore/readback 替换该路径，并在
`59b4d91f46c2ac797c71c900e62dda87cf0cca60` 获独立验收。之后的 ACL-only repair 恢复了
exact managed v0.4.0 副本的 default-reader access，并仅对该修复关闭
`WC-INSTALL-POSTFLIGHT-F01`。该修复检查点的 package 仍为 managed v0.4.0，v0.4.1 未安装。之后的
[v0.6.3 安装接受记录](docs/skills/work-charter/STATE.md#accepted-v063-user-installation)保留该历史副本证据；
[历史 v0.6.5 状态](docs/skills/work-charter/STATE.md#current-v065-local-candidate)记录当时的更新；
[当前状态](docs/skills/work-charter/STATE.md#v071-outcome-scoped-authority)承接 v0.7.1 候选。
v0.5.0 stable loaded-copy、role-delivery adherence、跨 provider 执行、cross-Harness、
公开发布与广泛效能仍为 `UNKNOWN` 或需分别授权。

## Role-model 配置

Package 默认数据位于
[`skills/work-charter/assets/role-models.default.yaml`](skills/work-charter/assets/role-models.default.yaml)：

通用兼容回落（当前值）：

| 角色 | Provider | Model | Reasoning effort |
|---|---|---|---|
| Orchestrator | OpenAI | `gpt-6-astra` | `high` |
| Planner | OpenAI | `gpt-6-astra` | `high` |
| Executor | OpenAI | `gpt-6-sol` | `xhigh` |
| Reviewer | OpenAI | `gpt-6-astra` | `medium` |

已批准级别默认：L0-L2 与 Executor 使用 OpenAI Sol，Planner、Orchestrator
及 L3-L4 Reviewer 使用 Astra：

| 级别 | 实际职责与 reasoning effort |
|---|---|
| L0 | primary、reviewer Sol `xhigh` |
| L1/L2 | primary、reviewer Sol `xhigh` |
| L3 | planner Astra `high`；executor Sol `xhigh`；reviewer Astra `medium` |
| L4 | orchestrator、planner Astra `high`；executor Sol `xhigh`；reviewer Astra `medium` |

L0 reviewer 明确配置为 Sol/xhigh，仅供独立触发的临时角色使用。这些配置值不代表评测最优或已运行生效。

如需定制后续任务启动或角色投递，可把该文件复制到
`~/.config/work-charter/role-models.yaml` 后编辑，或由已批准的 delivery contract 指定
另一个 exact 文件。Schema v1 继续接受旧四角色文件。Partial 文件可以新增通用
`primary`、替换有差异的通用职责，并/或为 `l0` 到 `l4` 添加有限的
`level_overrides`。每个对象都是 whole-object replacement，必须重写 `provider` 和
`model`；省略 `parameters` 表示不传参数。缺失用户对象时回落到包内对象；没有用户文件也能采用包内级别默认。

解析优先级为：已冻结的完整 delivery 组合；本次新任务/角色已明确确认的完整组合；用户级别对象；
用户通用对象；包内级别对象；包内通用对象。用户通用配置优先于包内级别覆盖。宿主的 `main` 标签在查找前归一化为 `primary`。如果
`L0`/`L1`/`L2` 的主负责人在两个来源中均无等级覆盖或通用 `primary`，派发边界不传 model override，
保留宿主选择，不能借用 Planner 或 Executor 默认。

可查找矩阵是：`L0` 为 primary 加按独立规则触发的临时 R；`L1`/`L2` 为 primary 加可选
R；`L3` 为 P/E/R；`L4` 为 O/P/E/R。配置项不会启用角色，`L0` 仍不激活 Work Charter。
创建前，边界展示 level、实际职责、provider/model/parameters、对象来源和文件来源，并核对
native 支持。Codex OpenAI 把 `model` 映射到 native `model`，把
`reasoning_effort` 映射到 `thinking`；不支持或含糊的数据 fail closed。文件变化不改变
既有任务或角色。Package 只定义该接口；global/host task-start consumer 尚未迁移，source 和
fixture 不能证明本机已实际采用。Install、update、rollback、uninstall 均不修改外部 user
文件。

提示词按[共同合同、实际职责、本次任务与必要模型适配](skills/work-charter/references/coordination-and-recovery.md#task-and-role-prompt-construction)组织。
已授权工作继续推进，保留材料决策与真实权限门；模型差异按需依据官方指导或可归属证据，
effort 仍为运行参数。提示词与交接保留关键事实、决定、材料限制及下一步，
优先删重复背景和无关内容，不用硬字数限制换取表面简短。全局迁移待相关 Skill 验收及获批适用副本切换后另行处理。

## 历史 v0.3.0 证据

首个独立版本为 `v0.3.0`。其历史本地候选由
[`release/v0.3.0-candidate.json`](release/v0.3.0-candidate.json) 描述，公开身份为
`junwei529/work-charter`。Exact candidate C 已获验收，并由
[`release/v0.3.0-local-release-receipt.json`](release/v0.3.0-local-release-receipt.json)
绑定，因此 `LOCAL_RELEASE_READY` 为 `VERIFIED`。不可变公开提交
`b655c1aa42acc8c68b70e87c4c228445c5182d8b`、annotated tag `v0.3.0` 与公开
GitHub Release 的 `PUBLIC_RELEASE` 已为 `VERIFIED`。
不可变 candidate descriptor 保留 C 中原始的 `PENDING_PLANNER_ACCEPTANCE` 快照，不重写 C。

不可变 public-source candidate 由
[`release/v0.3.0-public-release-candidate.json`](release/v0.3.0-public-release-candidate.json)
描述。它保持 package 字节不变，并记录预期 public repository、default branch、tag 与
human release-note gate，但不在自身记录其 commit hash。Exact public ref 与后续 release
receipt 必须绑定该 commit；annotated tag 与 GitHub Release 已在显式人工批准后创建。

发布后证据主体记录于
[`release/v0.3.0-public-release-evidence.json`](release/v0.3.0-public-release-evidence.json)。
它绑定公开对象、有界的同版本 persistent lifecycle 效果、两个历史 projectless
见证，以及一个全新的 sole-discovery loaded-copy 见证。保留的 predecessor 字节已移到
所有 Skill discovery root 之外，因此 managed user installation 是 catalog 中唯一可见的
`work-charter`。Planner 验收 `B2-WC-PUBLIC-EVIDENCE-F-01` 已验证 exact subject F
`4ba904808fe86e270ebd405db1866d41d1cc032e`；跨版本 lifecycle、cross-Harness、未测试上下文
与广泛效能仍为 `UNKNOWN`。

## 仓库内容

- 产品包：[`skills/work-charter/`](skills/work-charter/)
- 产品设计与状态：[`docs/skills/work-charter/`](docs/skills/work-charter/)
- 评估 case 与 fixture：[`evals/`](evals/README.md)
- 独立验证：[`scripts/check_repository.py`](scripts/check_repository.py)
- SOURCE 合同验证：[`scripts/check_source_contract.py`](scripts/check_source_contract.py)
- 安装生命周期工具：[`scripts/manage_install.py`](scripts/manage_install.py)
- 来源映射：[`PROVENANCE.md`](PROVENANCE.md) 与
  [`provenance/source-map.json`](provenance/source-map.json)
- 发布说明：[`CHANGELOG.md`](CHANGELOG.md)

## 验证

```powershell
python -B scripts/check_source_contract.py --json
python -B scripts/check_repository.py --json
```

对最终变更输入执行相应检查。SOURCE checker 分别核对静态合同条款、v0.7.1 的
tree/digest 绑定和历史描述文件身份（包括 v0.7.0）；静态文案及身份检查不证明模型行为。
当前结果见[验证记录](docs/skills/work-charter/VERIFICATION.md)。

其他检查按改变的机制选择：安装器或权限变化覆盖相关生命周期场景，来源验证逻辑变化
覆盖相关对抗场景，选择与加载变化进行有界行为检查。普通文案或元数据变化本身不要求
重跑完整 lifecycle 或 staged-index matrix。已有明确冻结 gate 保持原范围；v0.6.3 的
完整 qualification 是历史证据，不作为后续修订的新运行报告。实际安装仍单独核对身份、
权限与安装后状态。

## 未来 immutable-source 生命周期

将 `junwei529/work-charter` 的 exact immutable checkout 作为 `--source`，并明确给出
destination。未添加 `--apply` 时，以下命令只输出 dry-run plan：

```powershell
python -B scripts/manage_install.py status --destination <skill-destination> [--trusted-current-package-tree <git-tree-sha1>]
python -B scripts/manage_install.py install --source <v0.3.0-immutable-checkout> --destination <skill-destination> --expected-version 0.3.0
python -B scripts/manage_install.py update --source <new-immutable-checkout> --destination <skill-destination> --expected-version <new-version>
python -B scripts/manage_install.py rollback --source <old-immutable-checkout> --destination <skill-destination> --expected-version <old-version>
python -B scripts/manage_install.py uninstall --destination <skill-destination> [--trusted-current-package-tree <git-tree-sha1>]
```

任何计划中的产品状态修改，都应先在 destination 同一 filesystem volume 上创建一个绝对、
task-scoped 且位于所有 Skill discovery root 之外的 transaction 目录，然后附加
`--apply --transaction-root <external-task-directory>`。工具会自动保护 destination 的
父目录以及 source checkout 的 `skills` 目录；对其他活动 Skill discovery root，逐个重复
提供 `--discovery-root <absolute-path>`。工具会在修改 destination 之前拒绝不存在、相对、
别名化、link-like、相互包含或跨卷的显式 transaction 路径。

既有省略 `--transaction-root` 的 `--apply` 调用继续保持行为兼容：工具会在 destination
discovery root 之外自动创建唯一、经验证且同卷的目录，在结果中标记
`AUTO_COMPATIBILITY`，并在正常完成后删除该目录。此兼容 fallback 不授权、也不替代计划中
安装或发布操作所需的显式路径。两种模式下，stage、backup、tombstone 与 recovery archive
都只位于外部的单次事务目录中。Windows 上每个真实内容对象和权限快照都在写入字节前，
逐对象保护为仅 Owner Rights、SYSTEM 与 Administrators 可访问。全新 install 继承
destination parent 的既有 DACL；update、rollback 或 uninstall 前，工具在具有隔离父继承
上下文的零字节模型中证明原 DACL 可恢复，并完成“原策略→私有策略→原策略”的往返。
快照中已含 AI 的
记录使用单记录 `icacls /restore`；不含 AI 的记录使用携带 DACL 及必要 protected-DACL
information 的 `SetFileSecurityW`，避免把目录策略传播给子项。按浅到深应用后，再用同一
有界 `/save` 表示回读。比较忽略记录枚举顺序和换行序列化，但要求 managed path 集合一致，
并逐路径精确匹配 DACL SDDL，包括 P、AI、AR 与 ACE 顺序/内容。不受支持的控制状态或任何
预检不匹配都会在 target ACL 修改或移动前拒绝。全部预检通过后，精确受管旧对象先逐个
私有化，再首次移入 backup 或 tombstone，期间原读者可能短暂失去访问能力。因此，移动
失败也可能需要恢复已经修改的 ACL。promotion 和恢复都在真实 destination parent 下恢复
原策略并回读；恢复不完整时保留原 snapshot 和完整旧内容。卸载 ZIP 也先解包到逐对象私有
的 recovery stage，再提升至真实路径。未知写者、无法保持的 owner、不支持的 ACE、受管文件
硬链接及上下文漂移均拒绝。详见[设计边界](docs/skills/work-charter/DESIGN.md#windows-permission-context-and-private-handoff)；
其他平台保持原有权限行为。

历史五文件 receipt/candidate descriptor 与当前六文件 descriptor 只按 exact allow-list
package shape 识别。legacy 五文件 candidate 可省略冗余 package digest，但实际 tree 仍必须
匹配独立 trusted tree；当前六文件 shape 必须声明 digest，任何已声明但无效或不匹配的 digest
均 fail closed。
Windows update/rollback 的 path set 发生变化时，工具先在同一零内容上下文模型证明原 recovery snapshot，
仅在该模型上转换为目标 path shape，只把新增路径 reset 到 parent inheritance，然后核对全部
共同路径 descriptor 未变、每个新增路径均为 auto-inherited 且 unprotected，并对 projected
snapshot 完成 exact readback。原 snapshot 仍是 recovery authority。未知或自行声明的 path
set、不安全 receipt key、缺失或多余路径、tree 不匹配均 fail closed。

该 install 示例特意绑定 package tree 已进入内置信任映射的 v0.3.0 不可变 checkout。
不要把当前 working checkout 代入这条历史命令。v0.4.0 package 已完成 review、
验收与 candidate 外部 trust 绑定，并按 local-release receipt 的显式路线写入；但 promotion
后的目录保留了 transaction ACL，default reader access 失败。已提交的 v0.4.0 修正又因
`/restore` 改变 AI 而在首次后续 actual-policy preflight 失败。已接受的 v0.4.1 C4 source
替换该恢复路径并收紧权限问题路由。之后的 ACL-only 应用恢复了 exact v0.4.0 installed copy
的 default-reader access；它没有安装 v0.4.1 package。两个 v0.4 package tree 均未加入
历史内置信任映射，后续 status 或 mutation 仍须提供独立保留的 trust identity。

该 exact 失败 v0.4.0 副本的修复只改变 ACL，不把丢弃任意既有策略变成通用 update 合同。
首次获授权尝试已在上述控制状态 preflight 停止；之后的有界尝试使用已接受 C4 source，
重新核对受信 content/receipt 与 rollback 输入，只修改 target DACL，并通过 default-identity
status、直接读取、hash 与 ACL postflight。该结果不授权另一次修复、package update 或安装。

工具拒绝无 receipt、receipt 畸形或不匹配、package tree 错误、本地已修改、路径别名或
其他 drift 的 destination。receipt 是完整性与路由记录，不是加密所有权证明；能够以
同等本地权限伪造完整 receipt 的 actor 不在该机制的保护范围内。v0.3.0 经单独授权的
同版本 persistent lifecycle、发布、tag、GitHub Release 与 stable installed-copy 证据
已按上文记录为 VERIFIED。对 v0.4.0，原 promotion failure 与之后的 exact ACL-only access
repair 是两份不同证据；该修复使副本在之后的已接受更新前保持 managed、default-readable 的 v0.4.0 状态。
其他跨版本转换与 stable loaded behavior 仍需单独取证。

### 后续更新与回滚的信任输入

工具内置的信任映射只授权 v0.3.0 package tree。后续不可变 Release 必须在候选 checkout 之外独立发布经人工复核的 package-tree 身份。更新或回滚到工具未内置的版本时，使用 `--trusted-target-package-tree <git-tree-sha1>` 提供该外部信任锚；若当前已安装版本也不在内置映射中，再对 update、rollback、status 和 uninstall 使用 `--trusted-current-package-tree <git-tree-sha1>` 提供此前独立保留的身份。不得从待安装 source tree 自身复制这两个信任值；后续版本的公开 Release 与跨版本 lifecycle 证据在分别建立前仍为 `UNKNOWN`。

</details>
