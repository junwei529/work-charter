# Work Charter

[English](README.md)

本仓库是 `work-charter` 的独立本地产品仓库。可安装包位于
[`skills/work-charter/`](skills/work-charter/)，其字节与源提交
`80910a8b2375a11be897e9660c4b00a06d00dd13` 完全一致。

## 仓库内容

- 产品包：[`skills/work-charter/`](skills/work-charter/)
- 产品设计与状态：[`docs/skills/work-charter/`](docs/skills/work-charter/)
- 评估 case 与 fixture：[`evals/`](evals/README.md)
- 独立验证：[`scripts/check_repository.py`](scripts/check_repository.py)
- 来源映射：[`PROVENANCE.md`](PROVENANCE.md) 与
  [`provenance/source-map.json`](provenance/source-map.json)

## 验证

```powershell
python -B scripts/check_repository.py --json
```

本仓库不隐式依赖其他 Skill 仓库。remote、安装、tag、Release、发布以及完整历史连续性
均不属于本次迁移快照。
