# Work Charter

[English](README.md)

Work Charter 以 outcome、authority、evidence、recovery、independent review 与
proportional coordination 约束有后果的 Codex 工作。

规范产品包位于 [`skills/work-charter/`](../../../skills/work-charter/)。[设计](DESIGN.md)
说明产品边界，[状态](STATE.md)说明当前独立仓库生命周期，[验证](VERIFICATION.md)
记录证据和限制。

当前 [`v0.6.5` 候选](../../../release/v0.6.5-candidate.json)调整已批准级别模型推理默认值，
保留 [v0.6.4](../../../release/v0.6.4-candidate.json) 的轻量入口，
需要时加载精简共同正文与相关细节，并对材料变化主动复评，不代替用户选级。
已批准 Charter 的复用和共同审查、权限、恢复边界保留；
参见[状态](STATE.md#current-v065-local-candidate)中的当前源码和安装状态。

package 起源于源提交 `80910a8b2375a11be897e9660c4b00a06d00dd13`。不可变 `v0.5.0`
source 证据绑定已接受 commit `8bf9f130598fbf1b9170dd0c082e3e8fb78d6c0d`、十轮已完成
review、Planner 验收与 exact deterministic evidence。此前 v0.6.0 package 增加向后兼容的
“级别 × 实际职责”配置扩展，形成本地
[`v0.6.0` 候选](../../../release/v0.6.0-candidate.json)，不继承 v0.5.0 的验收。
安装、consumer 接入与 runtime 证据仍是独立边界。SOURCE qualification 要求当前
package tree 与 digest 均匹配描述文件；[验证](VERIFICATION.md)记录当前输入检查。
R12 已完成且无新增 findings，Planner 已接受未提交的冻结源码检查点；
[状态记录](STATE.md#accepted-v060-source-checkpoint)明确范围和身份。描述文件保留审查前快照。
这不表示已提交、local release ready、安装或全局生效；其验收记录差异也已单独验证并通过 Planner 核对；这些历史结果不覆盖当前 v0.6.5 输入。

候选同时包含已批准的包内级别默认及共同合同/实际职责/本次任务/必要模型适配的提示词方法。
用户通用配置优先于包内级别覆盖；参见[配置说明](../../../README.zh-CN.md#role-model-配置)。
