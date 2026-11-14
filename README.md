# WorkBuddy Skills

本仓库存放 WorkBuddy 用户级技能包。技能在本机的安装位置是 `~/.workbuddy/skills/<skill-name>/`。

## 收录

### evidence-audit（证据审计与假设证伪）

这个技能用于把「看起来成立」的主张验证到可复核，并在输出结论、数字或文件之前拦住机械性错误。它适用于策略可行性评估、统计结论复核、结论被数据推翻后的归因，以及错误流水复盘。

目录结构：

| 路径 | 内容 |
|---|---|
| `SKILL.md` | 四条硬原则与六步流程 |
| `references/self-check.md` | 八项交付自检、三条书写规矩、回执格式 |
| `references/failure-modes.md` | 13 类失效模式与拦截动作 |
| `references/case-studies.md` | 5 个真实翻案案例 |
| `scripts/audit_errors.py` | 错误流水的类型分布与复发统计 |
| `dist/evidence-audit.zip` | 可分发的打包文件 |

安装时把 `evidence-audit/` 复制到 `~/.workbuddy/skills/`，或把 `dist/evidence-audit.zip` 解压到该位置。

运行 `python scripts/audit_errors.py --path <errors.jsonl>` 可得到类型分布与复发告警；脚本会跳过坏行并报出行号。官方 `quick_validate.py` 对该技能目录的校验结果为 `Skill is valid!`。

## 取材说明

技能规则由 2026-11-06 至 2026-11-13 的一份交易项目实践记录原创重述，原始材料见（"交付自检清单 v1.0" §1–§4，2026）、（"因子挖掘报告 · 2026-11-13"，2026）、（"套利存续验证 · 2026-11-13"，2026）、（"做市实测快检 · 2026-11-13"，2026）与（`errors.jsonl`，2026）。本仓库只收录方法论与脚本，不含这些原始报告与原始数据文件。
