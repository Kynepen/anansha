"""
安安虾 (AnAnXia) 主入口
币安智能交易助手
"""

import json
import signal
import sys
import time
from pathlib import Path
from typing import Dict

from loguru import logger

from .binance_client import BinanceClient
from .market_monitor import MarketMonitor
from .dca_helper import DCAHelper
from .risk_alert import RiskAlert
from .launchpad_tracker import LaunchpadTracker
from .academy_helper import AcademyHelper
from .notifier import Notifier


class AnAnXia:
    """安安虾主类"""
    
    def __init__(self, config_path: str = 'config/config.json'):
        self.config = self._load_config(config_path)
        self.running = False
        
        # 初始化各模块
        self._init_modules()
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("🦞 安安虾初始化完成！")
    
    def _load_config(self, config_path: str) -> Dict:
        """加载配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载配置失败: {e}")
            raise
    
    def _init_modules(self):
        """初始化各模块"""
        # 币安客户端
        binance_config = self.config.get('binance', {})
        self.binance = BinanceClient(
            api_key=binance_config.get('api_key', ''),
            api_secret=binance_config.get('api_secret', ''),
            testnet=binance_config.get('testnet', False)
        )
        
        # 测试连接
        if not self.binance.test_connection():
            logger.warning("币安连接测试失败，请检查API配置")
        
        # 通知器
        notifier_config = self.config.get('notification', {})
        notifier_config.update(self.config.get('telegram', {}))
        self.notifier = Notifier(notifier_config)
        
        # 市场监控
        market_config = self.config.get('features', {}).get('market_monitor', {})
        if market_config.get('enabled', True):
            self.market_monitor = MarketMonitor(self.binance, market_config)
            self.market_monitor.on_alert(self._handle_market_alert)
            logger.info("✅ 市场监控模块已启用")
        else:
            self.market_monitor = None
        
        # 定投助手
        dca_config = self.config.get('features', {}).get('dca_helper', {})
        if dca_config.get('enabled', True):
            self.dca_helper = DCAHelper(self.binance, dca_config)
            logger.info("✅ 定投助手模块已启用")
        else:
            self.dca_helper = None
        
        # 风险预警
        risk_config = self.config.get('features', {}).get('risk_alert', {})
        if risk_config.get('enabled', True):
            self.risk_alert = RiskAlert(self.binance, risk_config)
            self.risk_alert.on_alert(self._handle_risk_alert)
            logger.info("✅ 风险预警模块已启用")
        else:
            self.risk_alert = None
        
        # Launchpad追踪
        launchpad_config = self.config.get('features', {}).get('launchpad_tracker', {})
        if launchpad_config.get('enabled', True):
            self.launchpad_tracker = LaunchpadTracker(launchpad_config)
            logger.info("✅ Launchpad追踪模块已启用")
        else:
            self.launchpad_tracker = None
        
        # Academy助手
        academy_config = self.config.get('features', {}).get('academy_helper', {})
        if academy_config.get('enabled', True):
            self.academy_helper = AcademyHelper(academy_config)
            logger.info("✅ Academy助手模块已启用")
        else:
            self.academy_helper = None
    
    def _handle_market_alert(self, alert_type: str, data: Dict):
        """处理市场告警"""
        self.notifier.send_alert(alert_type, data)
    
    def _handle_risk_alert(self, alert_type: str, data: Dict):
        """处理风险告警"""
        self.notifier.send_alert(alert_type, data)
    
    def _signal_handler(self, signum, frame):
        """信号处理"""
        logger.info("收到停止信号，正在关闭...")
        self.stop()
    
    def run(self):
        """运行安安虾"""
        self.running = True
        logger.info("🦞 安安虾启动！主人，我将开始帮您在币安赚到 BNB！")
        
        # 发送欢迎消息
        self.notifier.send_welcome()
        
        # 主循环
        counter = 0
        while self.running:
            try:
                # 市场监控检查
                if self.market_monitor and counter % 60 == 0:  # 每分钟
                    self.market_monitor.run_once()
                
                # Launchpad检查
                if self.launchpad_tracker and counter % 3600 == 0:  # 每小时
                    upcoming = self.launchpad_tracker.check_upcoming()
                    for project in upcoming:
                        self.notifier.send_message(
                            f"🚀 即将开始: {project['name']} ({project['hours_until']:.1f}小时后)"
                        )
                
                # 每日报告
                if counter % 86400 == 0:  # 每天
                    self._send_daily_report()
                
                counter += 1
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"主循环出错: {e}")
                time.sleep(5)
    
    def _send_daily_report(self):
        """发送每日报告"""
        report_parts = []
        
        # 市场摘要
        if self.market_monitor:
            market_summary = self.market_monitor.get_market_summary()
            report_parts.append(market_summary)
        
        # 定投摘要
        if self.dca_helper:
            dca_summary = self.dca_helper.get_all_plans_summary()
            report_parts.append(dca_summary)
        
        # 每日一课
        if self.academy_helper:
            lesson = self.academy_helper.get_daily_lesson()
            report_parts.append(lesson)
        
        full_report = "\n\n".join(report_parts)
        self.notifier.send_daily_report(full_report)
    
    def stop(self):
        """停止安安虾"""
        self.running = False
        logger.info("🦞 安安虾已停止")
    
    # ===== CLI 命令接口 =====
    
    def cmd_price(self, symbol: str = 'BTCUSDT'):
        """查询价格"""
        price = self.binance.get_ticker_price(symbol)
        if price:
            return f"💰 {symbol} 当前价格: ${price:,.2f}"
        return f"❌ 无法获取 {symbol} 价格"
    
    def cmd_market(self):
        """市场概况"""
        if self.market_monitor:
            return self.market_monitor.get_market_summary()
        return "市场监控模块未启用"
    
    def cmd_analysis(self, symbol: str = 'BTCUSDT'):
        """币种分析"""
        if self.market_monitor:
            return self.market_monitor.get_coin_analysis(symbol)
        return "市场监控模块未启用"
    
    def cmd_dca_create(self, symbol: str, amount: float, frequency: str = 'weekly'):
        """创建定投计划"""
        if self.dca_helper:
            plan = self.dca_helper.create_plan(symbol, amount, frequency)
            return f"✅ 定投计划创建成功！\n📊 币种: {symbol}\n💰 金额: {amount} USDT\n📅 频率: {frequency}"
        return "定投助手模块未启用"
    
    def cmd_dca_list(self):
        """列示定投计划"""
        if self.dca_helper:
            return self.dca_helper.get_all_plans_summary()
        return "定投助手模块未启用"
    
    def cmd_dca_report(self, plan_id: str):
        """定投报告"""
        if self.dca_helper:
            return self.dca_helper.get_plan_report(plan_id)
        return "定投助手模块未启用"
    
    def cmd_risk(self):
        """风险报告"""
        if self.risk_alert:
            # 示例持仓
            portfolio = {
                'BTCUSDT': 50000,
                'ETHUSDT': 3000,
                'BNBUSDT': 400
            }
            return self.risk_alert.get_risk_report(portfolio)
        return "风险预警模块未启用"
    
    def cmd_launchpad(self):
        """Launchpad项目"""
        if self.launchpad_tracker:
            return self.launchpad_tracker.get_upcoming_summary()
        return "Launchpad追踪模块未启用"
    
    def cmd_lesson(self):
        """每日一课"""
        if self.academy_helper:
            return self.academy_helper.get_daily_lesson()
        return "Academy助手模块未启用"
    
    def cmd_help(self):
        """帮助信息"""
        return """🦞 *安安虾命令列表*

📊 *市场命令*
/price [币种] - 查询价格
/market - 市场概况
/analysis [币种] - 币种分析

💰 *定投命令*
/dca_create 币种 金额 频率 - 创建定投
/dca_list - 列示定投计划
/dca_report 计划ID - 定投报告

⚠️ *风险命令*
/risk - 持仓风险报告

🚀 *Launchpad*
/launchpad - 即将开始的项目

📚 *学习*
/lesson - 每日一课

💡 提示: 方括号 [] 表示可选参数"""


def main():
    """主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='安安虾 - 币安智能交易助手')
    parser.add_argument('--config', '-c', default='config/config.json', help='配置文件路径')
    parser.add_argument('--command', '-cmd', help='执行单条命令')
    args = parser.parse_args()
    
    # 创建安安虾实例
    anansha = AnAnXia(args.config)
    
    if args.command:
        # 执行单条命令
        parts = args.command.split()
        cmd = parts[0]
        params = parts[1:]
        
        if hasattr(anansha, f'cmd_{cmd}'):
            method = getattr(anansha, f'cmd_{cmd}')
            result = method(*params)
            print(result)
        else:
            print(f"未知命令: {cmd}")
            print(anansha.cmd_help())
    else:
        # 正常运行模式
        anansha.run()


if __name__ == '__main__':
    main()
