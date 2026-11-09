# Work Charter

当前源码为 v0.12.0。[状态](STATE.md#current-candidate)提供发布入口，[验证](VERIFICATION.md#current-candidate)记录源码检查、本机安装和新运行加载。

## 历史文档

历史[v0.11.1源码补充](STATE.md#v0111-source-follow-up)加入可选知识协作和共同的用户规则确认保护。
[候选](../../../release/v0.11.1-candidate.json)记录应用前的源码身份。

[v0.11.0修订](STATE.md#v0110-current-work)重组公开通用流程与宿主职责。
[v0.11.0发布](https://github.com/junwei529/work-charter/releases/tag/v0.11.0)于2026-11-07读回确认。
[候选](../../../release/v0.11.0-candidate.json)保留实施前快照，实际审查与受管安装证据由State和Verification承接。
新使用默认不要求模型策略；明确选择后按该策略执行。旧合同已选策略、完整模型值、冻结组合及真实边界保留。

[English](README.md)

Work Charter 以 outcome、authority、evidence、recovery、independent review 与
proportional coordination 约束有后果的工作。

规范产品包位于 [`skills/work-charter/`](../../../skills/work-charter/)。[设计](DESIGN.md)
说明产品边界，[状态](STATE.md)说明当前独立仓库生命周期，[验证](VERIFICATION.md)
记录证据和限制。

## 历史证据

[尚未发布的 v0.6.7 证据范围候选](STATE.md#unreleased-evidence-scope-revision)单独绑定包身份，
变更后的源码不能沿用 v0.6.6 的资格证据。

已发布的 [`v0.6.5` 候选](../../../release/v0.6.5-candidate.json)调整已批准级别模型推理默认值，
保留 [v0.6.4](../../../release/v0.6.4-candidate.json) 的轻量入口，
需要时加载精简共同正文与相关细节，并对材料变化主动复评，不代替用户选级。
已批准 Charter 的复用和共同审查、权限、恢复边界保留；
参见[历史 v0.6.5 状态](STATE.md#current-v065-local-candidate)。
[当前源码](STATE.md#current-candidate)与
[v0.11.0安装、发布证据](STATE.md#v0110-current-work)分别记录。

package 起源于源提交 `80910a8b2375a11be897e9660c4b00a06d00dd13`。不可变 `v0.5.0`
source 证据绑定已接受 commit `8bf9f130598fbf1b9170dd0c082e3e8fb78d6c0d`、十轮已完成
review、Planner 验收与 exact deterministic evidence。此前 v0.6.0 package 增加向后兼容的
“级别 × 实际职责”配置扩展，形成本地
[`v0.6.0` 候选](../../../release/v0.6.0-candidate.json)，不继承 v0.5.0 的验收。
安装、consumer 接入与 runtime 证据仍是独立边界。该历史 SOURCE qualification 核对 v0.6.0
package tree、digest 与对应描述文件；[历史验证](VERIFICATION.history-through-v0111.md)保留当时的输入检查。
R12 已完成且无新增 findings，Planner 已接受未提交的冻结源码检查点；
[状态记录](STATE.md#accepted-v060-source-checkpoint)明确范围和身份。描述文件保留审查前快照。
这不表示已提交、local release ready、安装或全局生效；其验收记录差异也已单独验证并通过 Planner 核对；这些历史结果不覆盖 v0.6.6 等后续输入。

候选同时包含已批准的包内级别默认及共同合同/实际职责/本次任务/必要模型适配的提示词方法。
用户通用配置优先于包内级别覆盖；参见[配置说明](../../../README.zh-CN.md#role-model-配置)。
