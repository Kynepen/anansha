# 安安虾 (AnAnXia) - 一键安装

🦞 **币安智能交易助手** - 帮你在币安赚到 BNB！

## 快速安装

### 方式 1: 直接克隆安装

```bash
# 克隆仓库
git clone https://github.com/Kynepen/anansha.git
cd anansha

# 安装依赖
pip install -r requirements.txt

# 配置
cp config/config.example.json config/config.json
# 编辑 config.json 填入你的币安 API Key

# 运行
python -m src.main
```

### 方式 2: 作为 OpenClaw Skill 安装

```bash
# 下载到 OpenClaw skills 目录
cd ~/.openclaw/skills
git clone https://github.com/kyne1127/anansha.git

# 安装依赖
pip install -r anansha/requirements.txt

# 配置
cp anansha/config/config.example.json anansha/config/config.json
# 编辑 config.json

# 运行
openclaw run anansha
```

## 功能特点

- 📊 **实时市场监控** - 7×24小时监控价格异动
- 💰 **智能定投助手** - 自动化定投策略管理
- ⚠️ **风险预警系统** - 持仓风险实时监控
- 🚀 **Launchpad追踪** - 新币申购自动提醒
- 📚 **Academy学习助手** - 个性化学习路径

## 配置说明

编辑 `config/config.json`：

```json
{
  "binance": {
    "api_key": "你的币安API Key",
    "api_secret": "你的币安API Secret",
    "testnet": false
  },
  "telegram": {
    "bot_token": "你的Telegram Bot Token",
    "chat_id": "你的Chat ID"
  }
}
```

## 使用示例

```bash
# 查询 BTC 价格
python -m src.main --command price BTCUSDT

# 查看市场概况
python -m src.main --command market

# 创建定投计划 (每周定投 BTC 100 USDT)
python -m src.main --command dca_create BTCUSDT 100 weekly

# 查看持仓风险
python -m src.main --command risk

# 查看每日一课
python -m src.main --command lesson
```

## 开源协议

MIT License - 详见 [LICENSE](LICENSE)

---

🦞 **安安虾，帮你在币安赚到 BNB！**
