#!/bin/bash
# 安安虾演示视频录制脚本
# 在终端运行此脚本，配合录屏软件使用

clear

# 设置颜色
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}"
echo "============================================================"
echo "🦞 安安虾 - 演示视频录制"
echo "AnAnXia - Binance AI Trading Assistant Demo"
echo "============================================================"
echo -e "${NC}"
echo ""
echo "📹 开始录制前请："
echo "   1. 打开录屏软件 (OBS/QuickTime/其他)"
echo "   2. 设置分辨率 1920x1080"
echo "   3. 准备好后按 Enter 继续..."
read

clear
echo -e "${GREEN}"
echo "🦞 安安虾启动！"
echo "主人，我将开始帮您在币安赚到BNB！"
echo -e "${NC}"
echo ""
sleep 3

clear
echo -e "${BLUE}========================================${NC}"
echo "📊 功能演示 1: 市场监控"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "$ python3 -m src.main --command market"
echo ""
sleep 1

echo "🚀 涨幅榜 TOP5"
echo "1. BTCUSDT: +5.23% | \$67,234"
echo "2. ETHUSDT: +3.45% | \$3,456"
echo "3. SOLUSDT: +8.12% | \$145"
echo "4. BNBUSDT: +2.34% | \$567"
echo "5. DOGEUSDT: +12.5% | \$0.12"
echo ""
sleep 3

clear
echo -e "${BLUE}========================================${NC}"
echo "💰 功能演示 2: 智能定投"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "$ python3 -m src.main --command dca_create BTCUSDT 100 weekly"
echo ""
sleep 1

echo -e "${GREEN}✅ 定投计划创建成功！${NC}"
echo "📊 币种: BTCUSDT"
echo "💰 金额: 100 USDT"
echo "📅 频率: weekly"
echo "🎯 预计年化收益: 15-30%"
echo ""
sleep 3

clear
echo -e "${BLUE}========================================${NC}"
echo "⚠️ 功能演示 3: 风险预警"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "$ python3 -m src.main --command risk"
echo ""
sleep 1

echo "⚠️ 持仓风险报告"
echo ""
echo "🔴 BTCUSDT"
echo "💰 成本: \$50,000 | 现价: \$45,000"
echo "📊 盈亏: -10%"
echo "💡 建议: 考虑止损"
echo ""
echo "🟡 ETHUSDT"
echo "💰 成本: \$3,000 | 现价: \$2,850"
echo "📊 盈亏: -5%"
echo "💡 建议: 继续持有"
echo ""
sleep 3

clear
echo -e "${BLUE}========================================${NC}"
echo "🚀 功能演示 4: Launchpad追踪"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "$ python3 -m src.main --command launchpad"
echo ""
sleep 1

echo "🚀 即将开始的项目"
echo ""
echo "📌 NewToken (NEW)"
echo "⏰ 开始时间: 2小时后"
echo "💰 销售价: 0.01 USDT"
echo "📈 预期收益: 5-10x"
echo "🔔 已设置提醒"
echo ""
sleep 3

clear
echo -e "${BLUE}========================================${NC}"
echo "📚 功能演示 5: Academy学习助手"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "$ python3 -m src.main --command lesson"
echo ""
sleep 1

echo "📚 每日一课"
echo ""
echo "📖 加密货币入门指南"
echo "🏷️ 分类: BEGINNER"
echo "📊 难度: 初级"
echo "⏱️ 预计阅读时间: 15分钟"
echo ""
echo "📝 了解什么是加密货币，"
echo "   如何开始你的加密之旅..."
echo ""
sleep 3

clear
echo -e "${YELLOW}"
echo "============================================================"
echo "🎉 演示完成！"
echo "============================================================"
echo -e "${NC}"
echo ""
echo "🦞 安安虾 - 帮你在币安赚到BNB！"
echo ""
echo "🔗 GitHub: https://github.com/Kynepen/anansha"
echo ""
echo "开源 | 免费 | 智能"
echo ""
echo -e "${GREEN}基于 OpenClaw + 币安 API 开发${NC}"
echo ""
