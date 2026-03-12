# Claude Auto Loop 使用指南

## 快速开始

### 基础用法

```bash
# 运行 5 次迭代（默认）
bash scripts/claude_auto_loop.sh

# 运行指定次数的迭代
bash scripts/claude_auto_loop.sh 10
```

### 环境变量配置

```bash
# 使用 Sonnet 模型运行 10 次迭代
CLAUDE_MODEL=sonnet bash scripts/claude_auto_loop.sh 10

# 使用高努力模式
CLAUDE_EFFORT=high bash scripts/claude_auto_loop.sh 5

# 组合使用
CLAUDE_MODEL=sonnet CLAUDE_EFFORT=high bash scripts/claude_auto_loop.sh 10
```

## 可用环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `CLAUDE_MODEL` | (空) | 模型选择：`sonnet`, `opus`, `haiku` |
| `CLAUDE_EFFORT` | `medium` | 努力程度：`low`, `medium`, `high` |
| `CLAUDE_PERMISSION_MODE` | `default` | 权限模式 |

## 停止循环

### 方法 1：创建 STOP 文件

```bash
# 在另一个终端中执行
touch ai_dev/STOP
```

脚本会在当前迭代完成后优雅退出，并自动删除 STOP 文件。

### 方法 2：Ctrl+C

直接中断脚本（不推荐，可能导致未提交的更改）。

## 工作流程

每次迭代会自动执行以下步骤：

1. **读取规则** - 读取 `ai_dev/` 下的所有开发规则和任务
2. **选择任务** - 从 `ai_dev/next_tasks.md` 选择一个小任务
3. **实现功能** - 编写代码实现任务
4. **运行验证** - 测试功能是否正常
5. **更新文档** - 更新相关文档和日志
6. **自动提交** - 提取 commit message 并自动提交到 git
7. **准备下一轮** - 更新 `next_tasks.md` 为下一轮做准备

## 输出说明

### 日志文件

所有输出都会保存到 `ai_dev/logs/` 目录：

```
ai_dev/logs/claude-iteration-1-20260312-143000.log
ai_dev/logs/claude-iteration-2-20260312-143500.log
...
```

### 控制台输出

脚本会显示：
- ✅ 成功操作（绿色勾）
- ⚠️ 警告信息（警告符号）
- ❌ 错误信息（红叉）
- ℹ️ 信息提示（信息符号）
- 📝 提交信息（笔记符号）

### 会话总结

循环结束后会显示：
- 总迭代次数
- 成功次数
- 失败次数
- 日志保存位置

## 最佳实践

### 1. 开始前检查

```bash
# 确保工作区干净
git status

# 确保在正确的分支
git branch

# 查看当前任务列表
cat ai_dev/next_tasks.md
```

### 2. 选择合适的迭代次数

- **短期测试**：3-5 次迭代
- **日常开发**：5-10 次迭代
- **长期运行**：10-20 次迭代

### 3. 监控进度

```bash
# 在另一个终端监控日志
tail -f ai_dev/logs/claude-iteration-*.log

# 查看 git 提交历史
watch -n 5 'git log --oneline -10'
```

### 4. 任务管理

确保 `ai_dev/next_tasks.md` 中的任务：
- 粒度足够小（每个任务 1-2 小时完成）
- 描述清晰明确
- 有优先级排序
- 包含验收标准

## 故障排除

### 问题：Claude 命令未找到

```bash
# 检查 claude CLI 是否安装
which claude

# 如果未安装，参考 Claude CLI 文档安装
```

### 问题：提交失败

检查：
- Git 配置是否正确
- 是否有未解决的冲突
- 文件权限是否正确

### 问题：任务列表为空

编辑 `ai_dev/next_tasks.md` 添加新任务，或者让 Claude 在上一轮生成新任务。

### 问题：循环卡住

1. 检查日志文件查看具体错误
2. 使用 `touch ai_dev/STOP` 停止循环
3. 手动检查和修复问题
4. 重新启动循环

## 高级用法

### 自定义 Prompt

编辑 `ai_dev/claude_auto_loop_prompt.txt` 来自定义 AI 的行为。

### 并行运行（不推荐）

不建议同时运行多个 loop 实例，可能导致 git 冲突。

### 集成到 CI/CD

可以将 loop 脚本集成到自动化流程中：

```bash
# 示例：每天运行一次
0 2 * * * cd /path/to/Roguelike && bash scripts/claude_auto_loop.sh 5
```

## 注意事项

1. **自动提交已强制启用** - 每次迭代后都会自动提交
2. **需要 commit message** - Claude 必须在输出中提供 commit message
3. **保持任务小而清晰** - 避免过大的任务导致失败
4. **定期检查代码质量** - 自动化不代表不需要人工审查
5. **备份重要数据** - 虽然有 git 历史，但定期备份仍然重要

## 示例会话

```bash
$ bash scripts/claude_auto_loop.sh 3
============================================================
Claude Auto Loop - AI Development Session
============================================================
Root: /home/user/Roguelike
Logs: /home/user/Roguelike/ai_dev/logs
Iterations: 3
Permission mode: default
Auto commit: FORCED (always enabled)

To stop the loop after current iteration: touch ai_dev/STOP
============================================================

============================================================
=== Iteration 1 / 3 (2026-03-12 14:30:00) ===
============================================================
Logging to: ai_dev/logs/claude-iteration-1-20260312-143000.log

[Claude 开始工作...]

------------------------------------------------------------
📝 Committing changes with message: Add equipment system with slot-based items
✅ Changes committed successfully
------------------------------------------------------------

============================================================
=== Iteration 2 / 3 (2026-03-12 14:35:00) ===
============================================================
[...]

============================================================
Session Summary
============================================================
Total iterations: 3
Successful: 3
Failed: 0
Logs saved to: /home/user/Roguelike/ai_dev/logs
============================================================
```

## 相关文档

- [开发规则](../ai_dev/dev_rules.md)
- [架构文档](../ai_dev/architecture.md)
- [任务清单](../ai_dev/next_tasks.md)
- [会话日志](../ai_dev/session_log.md)
