# 安安虾 - 币安智能交易助手

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置

```bash
cp config/config.example.json config/config.json
# 编辑 config.json 填入你的 API Key 和 Telegram 配置
```

### 3. 运行

```bash
# 正常运行模式
python -m src.main

# 执行单条命令
python -m src.main --command price BTCUSDT
python -m src.main --command market
```

## 模块测试

### 测试币安连接

```python
from src.binance_client import BinanceClient

client = BinanceClient('your_api_key', 'your_api_secret')
print(client.test_connection())
print(client.get_ticker_price('BTCUSDT'))
```

### 测试市场监控

```python
from src.binance_client import BinanceClient
from src.market_monitor import MarketMonitor

client = BinanceClient('key', 'secret')
monitor = MarketMonitor(client, {
    'watchlist': ['BTCUSDT', 'ETHUSDT'],
    'price_change_threshold': 0.05
})
print(monitor.get_market_summary())
```

## 命令示例

```bash
# 查询价格
python -m src.main -cmd price BTCUSDT

# 市场概况
python -m src.main -cmd market

# 币种分析
python -m src.main -cmd analysis ETHUSDT

# 创建定投计划
python -m src.main -cmd dca_create BTCUSDT 100 weekly

# 查看定投
python -m src.main -cmd dca_list

# 风险报告
python -m src.main -cmd risk

# Launchpad项目
python -m src.main -cmd launchpad

# 每日一课
python -m src.main -cmd lesson
```
