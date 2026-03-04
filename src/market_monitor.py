"""
市场监控模块 - 实时监控价格异动
"""

import time
from typing import Dict, List, Callable
from datetime import datetime
from loguru import logger

from .binance_client import BinanceClient


class MarketMonitor:
    """市场监控器"""
    
    def __init__(self, binance_client: BinanceClient, config: Dict):
        self.client = binance_client
        self.config = config
        self.watchlist = config.get('watchlist', ['BTCUSDT', 'ETHUSDT', 'BNBUSDT'])
        self.price_change_threshold = config.get('price_change_threshold', 0.05)
        self.volume_surge_threshold = config.get('volume_surge_threshold', 3.0)
        self.check_interval = config.get('check_interval', 60)
        self.price_history = {}
        self.callbacks = []
        logger.info(f"市场监控初始化完成，监控列表: {self.watchlist}")
    
    def on_alert(self, callback: Callable):
        """注册告警回调"""
        self.callbacks.append(callback)
    
    def _trigger_alert(self, alert_type: str, data: Dict):
        """触发告警"""
        for callback in self.callbacks:
            try:
                callback(alert_type, data)
            except Exception as e:
                logger.error(f"告警回调执行失败: {e}")
    
    def check_price_changes(self) -> List[Dict]:
        """检查价格变化"""
        alerts = []
        
        for symbol in self.watchlist:
            try:
                current_price = self.client.get_ticker_price(symbol)
                if current_price is None:
                    continue
                
                # 获取24小时统计
                stats = self.client.get_24h_stats(symbol)
                if stats is None:
                    continue
                
                change_percent = stats['price_change_percent'] / 100
                
                # 检查是否超过阈值
                if abs(change_percent) >= self.price_change_threshold:
                    alert = {
                        'type': 'price_surge' if change_percent > 0 else 'price_drop',
                        'symbol': symbol,
                        'current_price': current_price,
                        'change_percent': change_percent,
                        'change_24h': stats['price_change'],
                        'high_24h': stats['high_price'],
                        'low_24h': stats['low_price'],
                        'volume': stats['volume'],
                        'timestamp': datetime.now().isoformat()
                    }
                    alerts.append(alert)
                    self._trigger_alert(alert['type'], alert)
                    logger.info(f"价格异动告警: {symbol} {'暴涨' if change_percent > 0 else '暴跌'} {abs(change_percent)*100:.2f}%")
                
            except Exception as e:
                logger.error(f"检查 {symbol} 价格失败: {e}")
        
        return alerts
    
    def get_market_summary(self) -> str:
        """获取市场摘要"""
        try:
            gainers = self.client.get_top_gainers(5)
            losers = self.client.get_top_losers(5)
            
            summary = "📊 *市场概况*\n\n"
            
            summary += "🚀 *涨幅榜 TOP5*\n"
            for i, coin in enumerate(gainers, 1):
                summary += f"{i}. {coin['symbol']}: +{coin['price_change_percent']:.2f}% | ${coin['last_price']:,.2f}\n"
            
            summary += "\n📉 *跌幅榜 TOP5*\n"
            for i, coin in enumerate(losers, 1):
                summary += f"{i}. {coin['symbol']}: {coin['price_change_percent']:.2f}% | ${coin['last_price']:,.2f}\n"
            
            return summary
        except Exception as e:
            logger.error(f"获取市场摘要失败: {e}")
            return "获取市场数据失败"
    
    def get_coin_analysis(self, symbol: str) -> str:
        """获取币种分析"""
        try:
            stats = self.client.get_24h_stats(symbol)
            if stats is None:
                return f"无法获取 {symbol} 数据"
            
            klines = self.client.get_klines(symbol, interval='1h', limit=24)
            
            analysis = f"📈 *{symbol} 分析*\n\n"
            analysis += f"💰 当前价格: ${stats['last_price']:,.2f}\n"
            analysis += f"📊 24h涨跌: {stats['price_change_percent']:+.2f}%\n"
            analysis += f"📈 24h最高: ${stats['high_price']:,.2f}\n"
            analysis += f"📉 24h最低: ${stats['low_price']:,.2f}\n"
            analysis += f"💵 24h成交量: {stats['volume']:,.2f}\n"
            analysis += f"🔄 交易次数: {stats['count']}\n"
            
            # 计算波动率
            if klines:
                prices = [k['close'] for k in klines]
                volatility = ((max(prices) - min(prices)) / min(prices)) * 100
                analysis += f"📊 24h波动率: {volatility:.2f}%\n"
            
            # 趋势判断
            if stats['price_change_percent'] > 5:
                analysis += "\n🔥 *趋势: 强势上涨*"
            elif stats['price_change_percent'] > 0:
                analysis += "\n📈 *趋势: 上涨*"
            elif stats['price_change_percent'] > -5:
                analysis += "\n📉 *趋势: 下跌*"
            else:
                analysis += "\n❄️ *趋势: 大幅下跌*"
            
            return analysis
        except Exception as e:
            logger.error(f"分析 {symbol} 失败: {e}")
            return f"分析 {symbol} 失败"
    
    def run_once(self):
        """运行一次检查"""
        alerts = self.check_price_changes()
        return alerts
    
    def run_continuous(self):
        """持续运行监控"""
        logger.info("市场监控启动")
        while True:
            try:
                self.run_once()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"监控循环出错: {e}")
                time.sleep(5)
