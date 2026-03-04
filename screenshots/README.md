# 安安虾演示截图

## 📸 截图文件

所有截图均为 **1280×720** 分辨率，适合用于比赛提交、社交媒体分享。

### 截图列表

| 文件名 | 内容 | 用途 |
|--------|------|------|
| `01_main.png` | 启动画面+功能概览 | 首图、封面 |
| `02_market.png` | 市场监控演示 | 功能展示 |
| `03_dca.png` | 定投助手演示 | 功能展示 |
| `04_risk.png` | 风险预警演示 | 功能展示 |
| `05_github.png` | GitHub仓库信息 | 开源证明 |

---

## 🎨 生成截图方法

### 方式1: 使用 HTML 文件 (推荐)

1. 用浏览器打开 `demo_screenshots.html`
2. 按 `Ctrl+P` (Windows) 或 `Cmd+P` (Mac) 打印
3. 选择 "另存为 PDF" 或 "打印到文件"
4. 使用截图工具截取每个 `.screenshot` 区域
5. 导出为 PNG 格式

**浏览器推荐:** Chrome / Edge / Firefox

### 方式2: 使用浏览器开发者工具

1. 在 Chrome 中打开 HTML 文件
2. 右键点击截图区域 → 检查
3. 在 Elements 面板中选中 `.screenshot` 元素
4. 右键 → `Capture node screenshot`
5. 自动下载 PNG 截图

### 方式3: 命令行工具

```bash
# 使用 puppeteer 或 playwright 截图
npm install -g puppeteer-cli
puppeteer screenshot demo_screenshots.html --viewport 1280x720 screenshots/output.png
```

---

## 📝 截图使用建议

### 比赛提交
- 按顺序上传 5 张截图
- 第一张 `01_main.png` 作为封面
- 图片命名清晰，方便评委理解

### Twitter/X 发布
```
🦞 安安虾 - 币安智能交易助手

基于 OpenClaw 开发的开源项目

📊 市场监控 | 💰 智能定投 | ⚠️ 风险预警 | 🚀 Launchpad

GitHub: github.com/Kynepen/anansha

#币安 #Binance #OpenClaw #AI #Crypto
```

---

## 🎯 截图内容说明

### 截图1: 启动画面
- 🦞 Logo + 项目名称
- 四大核心功能卡片
- 视觉吸引力强，适合首图

### 截图2: 市场监控
- 终端界面展示
- 涨幅榜/跌幅榜数据
- 展示实时数据获取能力

### 截图3: 定投助手
- 创建定投计划命令
- 定投收益展示
- 体现财务管理功能

### 截图4: 风险预警
- 持仓风险分析
- 分级风险提示
- AI建议展示

### 截图5: GitHub仓库
- 开源信息
- 安装命令
- 社区互动

---

## 🖼️ 截图规格

- **分辨率:** 1280×720 (16:9)
- **格式:** PNG (推荐) 或 JPG
- **文件大小:** 每张 < 500KB
- **色彩模式:** RGB

---

## ✨ 设计特点

1. **深色主题** - 符合开发者审美
2. **币安黄配色** - 品牌识别度高
3. **终端风格** - 技术感强
4. **Emoji图标** - 活泼易读
5. **中文为主** - 符合比赛要求

---

## 📤 上传到比赛

1. 准备 5 张截图
2. 压缩为 ZIP 或直接上传
3. 附上图说说明每张图的功能
4. 提交 GitHub 链接

---

**提示:** 如需要更高分辨率 (1920×1080) 或其他尺寸的截图，
可修改 HTML 文件中的 `.screenshot` 样式。
