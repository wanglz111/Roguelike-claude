# Roguelike AI Dev Project

一个为 AI 持续接力开发而设计的 CLI Roguelike / 魔塔式 RPG 项目。

游戏特性：

1. 支持中英文双语
2. CLI 命令行界面
3. 回合制战斗系统
4. 楼层探索与成长机制

当前版本目标：

1. 建立最小可玩骨架
2. 建立 AI 开发协议文件
3. 支持基础战斗与楼层推进
4. 为下一轮增量开发提供清晰入口

## 运行方式

```bash
python3 -m cli.main
```

游戏启动时会提示选择语言（中文或英文）。

## Claude 自动循环

如果你已经配置好 `claude` CLI，可以让它自动连续跑多轮开发：

```bash
bash scripts/claude_auto_loop.sh 5
```

含义：

1. 每轮都会先读取 `ai_dev/` 规则文件
2. 每轮只完成 `next_tasks.md` 中的一个小任务
3. 每轮结束后自动进入下一轮
4. Claude 的输出会保存到 `ai_dev/logs/`
5. 如果仓库有改动，脚本会自动提交当前这一轮的变更

常用环境变量：

```bash
CLAUDE_MODEL=sonnet
CLAUDE_EFFORT=medium
CLAUDE_PERMISSION_MODE=default
CLAUDE_AUTO_COMMIT=1
```

例如：

```bash
CLAUDE_MODEL=sonnet CLAUDE_EFFORT=high bash scripts/claude_auto_loop.sh 10
```

停止方式：

```bash
touch ai_dev/STOP
```

脚本会在当前轮结束后停止。

## 当前已实现

1. 玩家基础属性与升级逻辑
2. 基于 JSON 内容池的怪物生成
3. 最小战斗循环
4. 楼层推进与胜败结算
5. 掉落物与背包系统
6. AI 开发规则、路线图、任务清单

## 推荐阅读顺序

1. `开发文档.md`
2. `ChatGPT-AI持续开发游戏框架.md`
3. `Claude-无限开发-Prompt-Framework.md`
4. `ai_dev/dev_rules.md`
5. `ai_dev/next_tasks.md`
