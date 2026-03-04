"""
通知推送模块 - Telegram 消息推送
"""

import asyncio
from typing import Optional
from datetime import datetime, time as dt_time
from loguru import logger


class Notifier:
    """通知推送器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.enabled = config.get('enabled', True)
        self.quiet_hours = config.get('quiet_hours', {})
        self.bot_token = config.get('bot_token', '')
        self.chat_id = config.get('chat_id', '')
        logger.info("通知推送器初始化完成")
    
    def _is_quiet_time(self) -> bool:
        """检查是否在静音时段"""
        if not self.quiet_hours:
            return False
        
        now = datetime.now().time()
        start = self.quiet_hours.get('start', '23:00')
        end = self.quiet_hours.get('end', '08:00')
        
        start_time = dt_time.fromisoformat(start)
        end_time = dt_time.fromisoformat(end)
        
        if start_time < end_time:
            return start_time <= now <= end_time
        else:  # 跨天情况
            return now >= start_time or now <= end_time
    
    async def send_message(self, message: str, parse_mode: str = 'Markdown', 
                          disable_notification: bool = False) -> bool:
        """发送消息"""
        if not self.enabled:
            logger.debug("通知已禁用")
            return False
        
        if self._is_quiet_time() and not disable_notification:
            logger.info("静音时段，跳过通知")
            return False
        
        try:
            # 这里使用 openclaw 命令发送
            import subprocess
            
            result = subprocess.run(
                [
                    'openclaw', 'message', 'send',
                    '--channel', 'telegram',
                    '--to', self.chat_id.replace('telegram:', ''),
                    '--text', message
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.debug("消息发送成功")
                return True
            else:
                logger.error(f"消息发送失败: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"发送消息失败: {e}")
            return False
    
    def send_alert(self, alert_type: str, data: dict):
        """发送告警"""
        if alert_type == 'price_surge':
            message = f"""🚀 *价格暴涨提醒*

📈 {data['symbol']} 上涨 {data['change_percent']*100:.2f}%
💰 当前价格: ${data['current_price']:,.2f}
📊 24h最高: ${data['high_24h']:,.2f}
💵 成交量: {data['volume']:,.2f}

⏰ {data['timestamp']}"""
        
        elif alert_type == 'price_drop':
            message = f"""📉 *价格暴跌提醒*

🔻 {data['symbol']} 下跌 {abs(data['change_percent'])*100:.2f}%
💰 当前价格: ${data['current_price']:,.2f}
📊 24h最低: ${data['low_24h']:,.2f}
💵 成交量: {data['volume']:,.2f}

⏰ {data['timestamp']}"""
        
        elif alert_type == 'stop_loss':
            message = f"""⚠️ *止损预警*

📉 {data['symbol']} 亏损 {abs(data['loss_percent']):.2f}%
💰 成本价: ${data['entry_price']:,.2f}
💵 当前价: ${data['current_price']:,.2f}
💡 建议: {data['suggested_action']}

⏰ {data['timestamp']}"""
        
        else:
            message = f"""🔔 *提醒*

类型: {alert_type}
数据: {data}"""
        
        asyncio.create_task(self.send_message(message))
    
    def send_daily_report(self, report: str):
        """发送日报"""
        header = "📊 *安安虾每日报告*\n\n"
        asyncio.create_task(self.send_message(header + report))
    
    def send_welcome(self):
        """发送欢迎消息"""
        welcome = """🦞 *安安虾上线啦！*

主人，我将开始帮您在币安赚到 BNB！

📊 我可以帮你：
• 实时监控市场异动
• 管理定投计划
• 监控持仓风险
• 追踪 Launchpad 项目
• 学习币安 Academy

💡 使用说明：
发送 /help 查看所有命令

🚀 开始你的智能交易之旅吧！"""
        
        asyncio.create_task(self.send_message(welcome))
