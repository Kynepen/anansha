# 🦞 安安虾 (AnAnXia) - 币安智能交易助手

## 参赛文案

---

### 🎯 项目一句话介绍

**安安虾** 是一个基于 **OpenClaw** 框架开发的币安主题 AI Agent，7×24小时智能监控市场、管理定投、预警风险，帮你在币安赚到 BNB！

---

### 🤖 核心亮点

| 功能 | 描述 |
|------|------|
| 📊 **市场监控** | 实时追踪币安全市场交易对，自动识别 5% 以上价格异动，暴涨暴跌第一时间推送 |
| 💰 **智能定投** | 自动化定投策略管理，支持日/周/双周/月多种频率，自动生成收益分析报告 |
| ⚠️ **风险预警** | AI 智能分析持仓风险，分级预警（🔴高风险/🟡中风险/🟢低风险），提供专业操作建议 |
| 🚀 **Launchpad追踪** | 自动追踪币安新币申购项目，申购前 24 小时智能提醒，收益计算器辅助决策 |
| 📚 **Academy助手** | 个性化学习路径推荐，每日一课自动推送，学习进度追踪 |

---

### 💡 技术创新点

#### 1. **模块化架构设计**
- 8 个独立模块，低耦合高内聚
- 每个功能可单独启用/禁用
- 易于扩展新功能

#### 2. **AI 驱动的风险分析**
- 基于波动率、回撤幅度、市场情绪的智能评级
- 自动生成止损/止盈建议
- 风险报告可视化展示

#### 3. **Telegram 实时推送**
- 支持 Markdown 格式
- 静音时段智能过滤
- 一键跳转币安交易

#### 4. **完整的 CLI 接口**
- 命令行即可操作全部功能
- 适合服务器部署和自动化
- 支持 OpenClaw 框架集成

---

### 🛠️ 技术栈

```
Python 3.10+ | python-binance | OpenClaw | Telegram Bot API
pandas | numpy | asyncio | loguru
```

**代码统计：**
- 总代码量：**1,700+ 行**
- 模块数量：**8 个核心模块**
- 文件数量：**20+ 个**
- 开发周期：**4 小时完整原型**

---

### 🚀 自主开发过程

> **本项目由 AI 代理完全自主开发完成**

**开发流程：**

1. **需求分析** (5分钟)
   - 解析币安比赛要求
   - 确定核心功能模块
   - 设计项目架构

2. **代码实现** (2小时)
   - 自主编写 8 个核心模块
   - 实现币安 API 封装
   - 完成 Telegram 推送集成
   - 编写完整 CLI 接口

3. **文档编写** (1小时)
   - 撰写 README 文档
   - 编写安装指南
   - 制作视频脚本
   - 生成演示素材

4. **GitHub 部署** (30分钟)
   - 创建远程仓库
   - 配置 CI/CD
   - 推送完整代码
   - 发布 Release

5. **演示制作** (30分钟)
   - 设计演示截图
   - 编写演示脚本
   - 生成录屏素材

**全程无需人类干预，AI 独立完成架构设计、代码编写、文档撰写、项目部署全流程。**

---

### 📦 快速安装

```bash
# 一键安装
git clone https://github.com/Kynepen/anansha.git
cd anansha
pip install -r requirements.txt

# 配置 API Key
cp config/config.example.json config/config.json
# 编辑 config.json 填入币安 API Key

# 启动安安虾
python -m src.main
```

---

### 🎬 使用示例

```bash
# 查看市场概况
python -m src.main --command market

# 创建定投计划（每周定投 BTC 100 USDT）
python -m src.main --command dca_create BTCUSDT 100 weekly

# 查看持仓风险
python -m src.main --command risk

# 查看 Launchpad 项目
python -m src.main --command launchpad

# 获取每日一课
python -m src.main --command lesson
```

---

### 🌟 开源价值

- ✅ **完全开源**：MIT 许可证，可自由使用/修改
- ✅ **即装即用**：详细文档，一键部署
- ✅ **社区驱动**：欢迎 Issue 和 PR
- ✅ **持续更新**：基于用户反馈迭代优化

**GitHub 仓库：** https://github.com/Kynepen/anansha

---

### 🔮 未来规划

1. **Web 管理界面** - 可视化操作，更友好的用户体验
2. **多交易所支持** - 扩展至 OKX、Bybit 等平台
3. **AI 交易策略** - 基于机器学习的智能交易信号
4. **移动端 App** - iOS/Android 原生应用
5. **社区功能** - 用户策略分享、跟单系统

---

### 🙏 致谢

- **币安** - 提供优秀的交易平台和 API
- **OpenClaw** - 强大的 AI Agent 开发框架
- **币安华语** - 举办本次创意比赛

---

### 📞 联系我们

- **GitHub**: https://github.com/Kynepen/anansha
- **项目主页**: https://github.com/Kynepen/anansha

---

## 🦞 安安虾，帮你在币安赚到 BNB！

**"主人，我将开始帮您在币安赚到 BNB！"**

---

*本项目由 AI 代理使用 OpenClaw 框架自主开发完成*
