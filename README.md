# 安安虾 (AnAnXia) - 币安智能交易助手

🦞 主人，我将开始帮您在币安赚到 BNB！

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## 🎯 项目简介

安安虾是一个基于 OpenClaw 框架开发的币安主题 AI Agent，专为币安用户打造智能交易辅助工具。

## ✨ 核心功能

### 1. 📊 实时市场监控
- 7×24 小时监控币安热门币种价格异动
- 检测大单流入、社媒情绪变化
- 暴涨暴跌实时推送提醒

### 2. 💰 智能定投助手
- 自动化定投策略计算
- 监控最佳买入时机
- 生成定投收益分析报告

### 3. ⚠️ 风险预警系统
- 持仓币种重要消息监控
- 利空事件实时预警
- 智能止损建议

### 4. 🚀 Launchpad/Launchpool 追踪
- 新项目上新自动提醒
- 申购时间智能通知
- 收益计算与对比分析

### 5. 📚 币安 Academy 学习助手
- 最新教程自动推送
- 个性化学习路径推荐
- 学习进度追踪报告

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/kyne1127/anansha.git
cd anansha

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp config/config.example.json config/config.json
# 编辑 config.json 填入你的配置
```

### 配置

编辑 `config/config.json`：

```json
{
  "binance": {
    "api_key": "你的币安API Key",
    "api_secret": "你的币安API Secret"
  },
  "telegram": {
    "bot_token": "你的Telegram Bot Token",
    "chat_id": "你的Chat ID"
  },
  "features": {
    "market_monitor": true,
    "dca_helper": true,
    "risk_alert": true,
    "launchpad_tracker": true,
    "academy_helper": true
  }
}
```

### 运行

```bash
# 启动安安虾
python -m src.main

# 或者使用 OpenClaw
openclaw run anansha
```

## 📁 项目结构

```
anansha/
├── src/
│   ├── __init__.py
│   ├── main.py              # 主入口
│   ├── binance_client.py    # 币安API封装
│   ├── market_monitor.py    # 市场监控模块
│   ├── dca_helper.py        # 定投助手模块
│   ├── risk_alert.py        # 风险预警模块
│   ├── launchpad_tracker.py # Launchpad追踪模块
│   ├── academy_helper.py    # 学习助手模块
│   └── notifier.py          # 通知推送模块
├── config/
│   └── config.example.json  # 配置文件模板
├── tests/
│   └── test_*.py           # 测试文件
├── docs/
│   └── README_ZH.md        # 中文文档
├── requirements.txt
├── LICENSE
└── README.md
```

## 🛠️ 技术栈

- **Python 3.10+** - 核心语言
- **python-binance** - 币安API接入
- **OpenClaw** - AI Agent 框架
- **python-telegram-bot** - Telegram推送
- **pandas/numpy** - 数据分析
- **asyncio** - 异步处理

## 📝 使用示例

### 市场监控

```python
from src.market_monitor import MarketMonitor

monitor = MarketMonitor()
# 监控 BTC 5% 以上波动
monitor.watch_price_change("BTCUSDT", threshold=0.05)
```

### 定投助手

```python
from src.dca_helper import DCAHelper

dca = DCAHelper()
# 设置每周定投 BTC 100 USDT
dca.setup_plan(symbol="BTCUSDT", amount=100, frequency="weekly")
```

## 🤝 贡献指南

欢迎提交 Issue 和 PR！

1. Fork 本仓库
2. 创建你的 Feature Branch (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到 Branch (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [OpenClaw](https://github.com/openclaw/openclaw) - AI Agent 框架
- [Binance](https://www.binance.com) - 加密货币交易平台
- [币安华语](https://x.com/binancezh) - 比赛主办方

---

🦞 **安安虾，帮你在币安赚到 BNB！**
