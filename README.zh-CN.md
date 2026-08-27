# Work Charter

[English](README.md)

本仓库是 `work-charter` 的独立产品仓库。可安装包位于
[`skills/work-charter/`](skills/work-charter/)，其字节与源提交
`80910a8b2375a11be897e9660c4b00a06d00dd13` 完全一致。

首个独立版本为 `v0.3.0`。当前本地候选由
[`release/v0.3.0-candidate.json`](release/v0.3.0-candidate.json) 描述，未来公开身份为
`junwei529/work-charter`。在 exact candidate 获得验收、且后续公开发布证据产生前，
`LOCAL_RELEASE_READY` 为 `PENDING_PLANNER_ACCEPTANCE`，`PUBLIC_RELEASE` 保持
`UNKNOWN`。

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

SOURCE 检查证明候选指令包含所需的 selection、activation、authority、recovery 与
Standard O/P/E 边界；它不证明模型遵循、installed-copy 行为或广泛产品效能。

## 未来 immutable-source 生命周期

将 `junwei529/work-charter` 的 exact immutable checkout 作为 `--source`，并明确给出
destination。未添加 `--apply` 时，以下命令只输出 dry-run plan：

```powershell
python -B scripts/manage_install.py status --destination <skill-destination> [--trusted-current-package-tree <git-tree-sha1>]
python -B scripts/manage_install.py install --source . --destination <skill-destination> --expected-version 0.3.0
python -B scripts/manage_install.py update --source <new-immutable-checkout> --destination <skill-destination> --expected-version <new-version>
python -B scripts/manage_install.py rollback --source <old-immutable-checkout> --destination <skill-destination> --expected-version <old-version>
python -B scripts/manage_install.py uninstall --destination <skill-destination> [--trusted-current-package-tree <git-tree-sha1>]
```

工具拒绝无 receipt、receipt 畸形或不匹配、package tree 错误、本地已修改、路径别名或
其他 drift 的 destination。receipt 是完整性与路由记录，不是加密所有权证明；能够以
同等本地权限伪造完整 receipt 的 actor 不在该机制的保护范围内。持久安装、更新、
回滚、卸载、发布、tag、GitHub Release 与 stable installed-copy proof 仍是需要单独
授权和取证的未来效果。

### 后续更新与回滚的信任输入

工具内置的信任映射只授权 v0.3.0 package tree。后续不可变 Release 必须在候选 checkout 之外独立发布经人工复核的 package-tree 身份。更新或回滚到工具未内置的版本时，使用 `--trusted-target-package-tree <git-tree-sha1>` 提供该外部信任锚；若当前已安装版本也不在内置映射中，再对 update、rollback、status 和 uninstall 使用 `--trusted-current-package-tree <git-tree-sha1>` 提供此前独立保留的身份。不得从待安装 source tree 自身复制这两个信任值；在 B2 建立不可变公开来源及人工复核 release notes 前，公开 Release 证据仍为 `UNKNOWN`。
