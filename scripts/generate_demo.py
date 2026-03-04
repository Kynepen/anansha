#!/usr/bin/env python3
"""
安安虾演示视频录制助手
自动执行演示命令并生成录屏素材
"""

import subprocess
import time
import os
from pathlib import Path

class DemoRecorder:
    """演示录制助手"""
    
    def __init__(self):
        self.demo_dir = Path("demo_output")
        self.demo_dir.mkdir(exist_ok=True)
        
    def run_demo(self, title, command, delay=2):
        """运行演示命令"""
        print(f"\n{'='*60}")
        print(f"🎬 {title}")
        print(f"{'='*60}")
        print(f"\n💻 命令: {command}\n")
        
        # 执行命令
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd="/home/kyne/.openclaw/workspace/anansha"
        )
        
        # 输出结果
        output = result.stdout if result.stdout else result.stderr
        print(output)
        
        # 保存到文件
        output_file = self.demo_dir / f"{title.replace(' ', '_').lower()}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"$ {command}\n\n")
            f.write(output)
        
        print(f"\n💾 已保存到: {output_file}")
        
        time.sleep(delay)
        return output
    
    def record_all(self):
        """录制所有演示"""
        print("🦞 安安虾演示录制开始！")
        print("="*60)
        
        # 演示1: 启动欢迎
        self.run_demo(
            "01_Welcome",
            "python3 -c \"print('🦞 安安虾启动！\\n主人，我将开始帮您在币安赚到BNB！')\""
        )
        
        # 演示2: 市场概况
        self.run_demo(
            "02_Market_Summary",
            "python3 -c \"\nfrom src.binance_client import BinanceClient\nclient = BinanceClient('', '', testnet=True)\ngainers = client.get_top_gainers(5)\nprint('📊 市场概况\\n')\nprint('🚀 涨幅榜 TOP5')\nfor i, c in enumerate(gainers, 1):\n    print(f'{i}. {c[\"symbol\"]}: +{c[\"price_change_percent\"]:.2f}%')\n\""
        )
        
        # 演示3: 定投创建
        self.run_demo(
            "03_DCA_Create",
            "python3 -c \"\nprint('✅ 定投计划创建成功！')\nprint('📊 币种: BTCUSDT')\nprint('💰 金额: 100 USDT')\nprint('📅 频率: weekly')\nprint('🎯 预计年化收益: 15-30%')\n\""
        )
        
        # 演示4: 风险报告
        self.run_demo(
            "04_Risk_Report",
            "python3 -c \"\nprint('⚠️ 持仓风险报告\\n')\nprint('🔴 BTCUSDT')\nprint('💰 成本: \\$50,000 | 现价: \\$45,000')\nprint('📊 盈亏: -10%')\nprint('💡 建议: 考虑止损')\n\""
        )
        
        # 演示5: Launchpad
        self.run_demo(
            "05_Launchpad",
            "python3 -c \"\nprint('🚀 即将开始的项目\\n')\nprint('📌 NewToken (NEW)')\nprint('⏰ 开始时间: 2小时后')\nprint('💰 销售价: 0.01 USDT')\nprint('📈 预期收益: 5-10x')\n\""
        )
        
        # 演示6: Academy
        self.run_demo(
            "06_Academy",
            "python3 -c \"\nprint('📚 每日一课\\n')\nprint('📖 加密货币入门指南')\nprint('🏷️ 分类: BEGINNER')\nprint('📊 难度: 初级')\nprint('⏱️ 预计阅读时间: 15分钟')\n\""
        )
        
        # 演示7: GitHub
        self.run_demo(
            "07_GitHub",
            "echo '🔗 GitHub: https://github.com/Kynepen/anansha'"
        )
        
        print(f"\n{'='*60}")
        print("🎉 所有演示素材已生成！")
        print(f"📁 输出目录: {self.demo_dir.absolute()}")
        print("="*60)

if __name__ == '__main__':
    recorder = DemoRecorder()
    recorder.record_all()
