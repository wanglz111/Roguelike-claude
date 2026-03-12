# Claude Auto Loop - 错误处理和保护机制

## 概述
这个脚本经过加固，确保在各种错误情况下都能继续运行，不会中途退出。

## 保护机制

### 1. 全局错误捕获
- 使用 `trap` 捕获意外错误
- 即使发生未预期的错误，也会显示错误信息并优雅退出

### 2. 迭代级别隔离
- 每次迭代都在独立的子shell中运行
- 单次迭代失败不会影响后续迭代
- 使用退出码来判断迭代成功或失败

### 3. Claude 命令错误处理
- 临时启用 `pipefail` 来捕获管道中的错误
- 使用 `${PIPESTATUS[0]}` 获取管道第一个命令的退出码
- 即使 Claude CLI 失败，循环也会继续

### 4. Git 操作错误处理
- 所有 git 命令都在 `set +e` 模式下运行
- 检查每个 git 命令的退出码
- Commit 失败时记录错误但继续下一轮

### 5. Python 脚本错误处理
- Python 脚本使用 try-except 捕获异常
- 即使日志解析失败，也会使用默认 commit 消息
- 使用 `2>/dev/null || echo ""` 确保不会因为 Python 错误而退出

### 6. STOP 文件机制
- 可以通过创建 STOP 文件来优雅停止循环
- 检测到 STOP 文件后会完成当前迭代再退出
- 使用特殊退出码 (99) 来区分正常停止和错误

### 7. 速率限制保护
- 每次迭代之间有 2 秒延迟
- 避免过快调用 API 导致限流

## 可能导致退出的情况

### 会导致立即退出的情况（在循环开始前）：
1. ❌ Prompt 文件不存在
2. ❌ Claude CLI 未安装
3. ❌ 无法创建日志目录

### 不会导致退出的情况（会继续循环）：
1. ✅ Claude 命令失败
2. ✅ Git commit 失败
3. ✅ Python 脚本失败
4. ✅ 日志文件写入失败
5. ✅ 没有代码变更
6. ✅ Commit 消息解析失败

## 测试建议

### 快速测试（3轮）
```bash
./scripts/claude_auto_loop.sh 3
```

### 中等测试（10轮）
```bash
./scripts/claude_auto_loop.sh 10
```

### 完整运行（100轮）
```bash
./scripts/claude_auto_loop.sh 100
```

### 后台运行
```bash
nohup ./scripts/claude_auto_loop.sh 100 > loop_output.log 2>&1 &
```

### 查看后台进程
```bash
ps aux | grep claude_auto_loop
```

### 优雅停止
```bash
touch /home/lucascool/Roguelike/ai_dev/STOP
```

## 监控

### 查看实时日志
```bash
tail -f /home/lucascool/Roguelike/ai_dev/logs/claude-iteration-*.log
```

### 查看最新日志
```bash
ls -lt /home/lucascool/Roguelike/ai_dev/logs/ | head -5
```

### 统计成功/失败次数
脚本结束时会自动显示统计信息：
```
============================================================
Session Summary
============================================================
Total iterations: 100
Successful: 95
Failed: 5
Logs saved to: /home/lucascool/Roguelike/ai_dev/logs
============================================================
```

## 故障排查

### 如果循环提前停止
1. 检查是否存在 STOP 文件：`ls -la ai_dev/STOP`
2. 查看最新日志文件的末尾：`tail -50 ai_dev/logs/claude-iteration-*.log`
3. 检查脚本进程是否还在运行：`ps aux | grep claude_auto_loop`

### 如果所有迭代都失败
1. 手动运行一次 Claude 命令测试：`cat ai_dev/claude_auto_loop_prompt.txt | claude -p`
2. 检查 Claude CLI 是否正常：`claude --version`
3. 检查权限模式是否正确：`echo $CLAUDE_PERMISSION_MODE`

## 保证

✅ **保证1**：单次迭代失败不会导致整个循环退出
✅ **保证2**：Git 操作失败不会导致循环退出
✅ **保证3**：即使没有代码变更，循环也会继续
✅ **保证4**：所有错误都会被记录到日志文件
✅ **保证5**：可以通过 STOP 文件优雅停止循环

## 最后更新
2026-03-12 - 添加了完整的错误处理和隔离机制
