# Work Charter

[English](README.md)

本仓库是 `work-charter` 的独立产品仓库。可安装包位于
[`skills/work-charter/`](skills/work-charter/)。它最初由源提交
`80910a8b2375a11be897e9660c4b00a06d00dd13` 物化；当前 repository-native
版本所修改的文件在 source map 中明确分类，不再描述为未改变的迁移 blob。

当前 SOURCE 候选为 `v0.4.0`，由
[`release/v0.4.0-candidate.json`](release/v0.4.0-candidate.json) 描述。它加入
可移植的 L0-L4 独立 Reviewer 语义，分开 Executor verification、Reviewer
技术 findings 与 Planner/Orchestrator acceptance，要求修复后优先由同一 Reviewer
复审并保留累计历史，并明确 evidence-first `UNKNOWN`、context-switch recovery、
callback 去重和 graph 证据限制。descriptor 保留不可变的 pre-review 快照；已接受
source candidate、五轮独立 review、已审 lifecycle-controller baseline，以及本次 v0.3-to-v0.4
update attempt 另由
[`release/v0.4.0-local-release-receipt.json`](release/v0.4.0-local-release-receipt.json)
绑定，但该 update 未被接受：exact bytes 与 receipt 通过了 elevated postflight，default
sandbox reader 却无法读取 promotion 后的副本。source-candidate acceptance 仍为
`VERIFIED`；`LOCAL_RELEASE_READY` 与 managed installation 在有界 ACL handoff 修正完成
review、验收和应用前保持 blocked。R4 返回 `NO_FINDINGS`，但 Planner acceptance 发现
review 中的 parent-reset 路径不能保全既有 explicit 或 protected DACL policy，因而打开
`WC-INSTALL-ACCESS-P01`。R5 随后打开 P2 `WC-INSTALL-ACCESS-R5-F01`：命令成功后没有
回读 target DACL；当前实现已修正，仍待 R6 与 Planner acceptance。stable loaded-copy、
natural adherence、cross-Harness、公开发布与广泛效能按记录保持失败、`UNKNOWN` 或需
分别授权。

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
python -B scripts/check_repository.py --json
python -B scripts/check_source_contract.py --json
python -B scripts/manage_install.py self-test --source .
```

SOURCE 检查证明当前候选指令包含所需的 selection、activation、authority、recovery、
independent-review 与 Standard O/P/E/R 边界，同时固定验证历史 v0.3 身份并校验 exact
v0.4 attempt receipt、开放 access finding 与待审 source correction；它不执行模型、
不重新读取 live installed copy、不接受该修正、不证明发布，也不建立广泛产品效能。

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
都只位于外部的单次事务目录中。若旧 destination 移入 backup 的第一步失败，原 destination
保持不动；若之后的替换失败，工具会恢复并验证原 managed copy，否则报告保留下来的
recovery 路径。待审 Windows 修正会先移除每个随机 per-operation transaction 目录的
继承，并仅向 Owner Rights、SYSTEM 与 Administrators 授权。全新 install 继承
destination parent 的既有 DACL；update、rollback 或 uninstall mutation 前，工具把现有
完整 DACL tree 保存到私有 transaction 中，先向私有副本回放，再用同一有界 `/save`
表示回读；不能完成或不匹配就会在 destination mutation 前 fail closed。比较忽略记录枚举
顺序和换行序列化，但要求 managed path 集合一致，并逐路径精确匹配 DACL SDDL，包括
继承/保护 flags 和 ACE 的顺序与内容。promotion 或恢复后的 target 回放旧策略后也必须通过
相同回读，才能报告成功；实际恢复不匹配会进入既有 recovery，恢复仍不完整时，原 snapshot
保留在受保护 transaction 中。backup 与 tombstone 只继承私有 transaction DACL。其他平台
保持原有 platform-default 行为。Windows 完整 lifecycle self-test 需要具备
`icacls /restore` 与 `/save` 能力的 token；能力不足时会在 destination mutation 前被拒绝。

该 install 示例特意绑定 package tree 已进入内置信任映射的 v0.3.0 不可变 checkout。
不要把当前 working checkout 代入这条历史命令。当前 v0.4.0 package 后续已完成 review、
验收与 candidate 外部 trust 绑定，并按 local-release receipt 的显式路线写入；但 promotion
后的目录保留了 transaction ACL，default reader access 失败。working source 已包含有界
Windows DACL-preservation 与 post-restore readback 修正，仍须完成 R6 独立 review 与
Planner acceptance 后才能修复 installed copy。v0.4 package tree 没有加入工具的历史
内置映射，因此后续 status 或 mutation 仍须提供独立保留的 v0.4 trust identity。

该 exact 失败 v0.4.0 副本的拟议修复只改变 ACL，不把丢弃任意既有策略变成通用 update
合同。完成 source review、Planner acceptance 与 local commit 后，先核对独立受信的
v0.4.0 content/receipt、记录中的私有 current DACL，以及独立验证的 destination-parent
reader policy；随后保存并预演可回滚 DACL snapshot，再只把该 exact target 重置为 parent
inheritance，失败则回放 snapshot。postflight 必须由默认身份完成 status、直接读取、hash
与 ACL 检查。该路线尚未执行。

工具拒绝无 receipt、receipt 畸形或不匹配、package tree 错误、本地已修改、路径别名或
其他 drift 的 destination。receipt 是完整性与路由记录，不是加密所有权证明；能够以
同等本地权限伪造完整 receipt 的 actor 不在该机制的保护范围内。v0.3.0 经单独授权的
同版本 persistent lifecycle、发布、tag、GitHub Release 与 stable installed-copy 证据
已按上文记录为 VERIFIED。对 v0.4.0，只有本次 v0.3-to-v0.4 attempt 写入的 bytes 与
elevated receipt/file postflight 已验证；default reader access 失败，因此 overall
transition 未被接受。其他跨版本转换与 stable loaded behavior 仍需单独取证。

### 后续更新与回滚的信任输入

工具内置的信任映射只授权 v0.3.0 package tree。后续不可变 Release 必须在候选 checkout 之外独立发布经人工复核的 package-tree 身份。更新或回滚到工具未内置的版本时，使用 `--trusted-target-package-tree <git-tree-sha1>` 提供该外部信任锚；若当前已安装版本也不在内置映射中，再对 update、rollback、status 和 uninstall 使用 `--trusted-current-package-tree <git-tree-sha1>` 提供此前独立保留的身份。不得从待安装 source tree 自身复制这两个信任值；后续版本的公开 Release 与跨版本 lifecycle 证据在分别建立前仍为 `UNKNOWN`。
