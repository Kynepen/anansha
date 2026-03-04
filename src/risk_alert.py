"""
风险预警模块 - 持仓风险监控
"""

from typing import Dict, List, Callable
from datetime import datetime
from loguru import logger

from .binance_client import BinanceClient


class RiskAlert:
    """风险预警系统"""
    
    def __init__(self, binance_client: BinanceClient, config: Dict):
        self.client = binance_client
        self.config = config
        self.alert_threshold = config.get('alert_threshold', -0.1)  # -10%
        self.callbacks = []
        self.price_history = {}
        logger.info("风险预警系统初始化完成")
    
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
    
    def check_portfolio_risk(self, portfolio: Dict[str, float]) -> List[Dict]:
        """检查持仓风险
        
        Args:
            portfolio: {symbol: entry_price}
        """
        alerts = []
        
        for symbol, entry_price in portfolio.items():
            try:
                current_price = self.client.get_ticker_price(symbol)
                if current_price is None:
                    continue
                
                change = (current_price - entry_price) / entry_price
                
                # 检查是否触发止损
                if change <= self.alert_threshold:
                    alert = {
                        'type': 'stop_loss',
                        'symbol': symbol,
                        'entry_price': entry_price,
                        'current_price': current_price,
                        'change': change,
                        'loss_percent': change * 100,
                        'suggested_action': '考虑止损',
                        'timestamp': datetime.now().isoformat()
                    }
                    alerts.append(alert)
                    self._trigger_alert('stop_loss', alert)
                    logger.warning(f"止损预警: {symbol} 亏损 {abs(change)*100:.2f}%")
                
                # 检查大幅回撤（从高点回落）
                if symbol not in self.price_history:
                    self.price_history[symbol] = {'high': current_price, 'low': current_price}
                else:
                    self.price_history[symbol]['high'] = max(self.price_history[symbol]['high'], current_price)
                    self.price_history[symbol]['low'] = min(self.price_history[symbol]['low'], current_price)
                
                from_high = (current_price - self.price_history[symbol]['high']) / self.price_history[symbol]['high']
                if from_high <= -0.15:  # 从高点回落15%
                    alert = {
                        'type': 'drawdown',
                        'symbol': symbol,
                        'high_price': self.price_history[symbol]['high'],
                        'current_price': current_price,
                        'drawdown': from_high,
                        'timestamp': datetime.now().isoformat()
                    }
                    alerts.append(alert)
                    self._trigger_alert('drawdown', alert)
                    logger.warning(f"回撤预警: {symbol} 从高点回落 {abs(from_high)*100:.2f}%")
                
            except Exception as e:
                logger.error(f"检查 {symbol} 风险失败: {e}")
        
        return alerts
    
    def analyze_risk(self, symbol: str, entry_price: float, position_size: float) -> Dict:
        """分析单个持仓风险"""
        try:
            current_price = self.client.get_ticker_price(symbol)
            if current_price is None:
                return {'error': '无法获取价格'}
            
            stats = self.client.get_24h_stats(symbol)
            if stats is None:
                return {'error': '无法获取统计数据'}
            
            change = (current_price - entry_price) / entry_price
            pnl = (current_price - entry_price) * position_size
            
            # 风险评级
            volatility = abs(stats['price_change_percent'])
            if volatility > 20:
                risk_level = "🔴 高风险"
            elif volatility > 10:
                risk_level = "🟡 中风险"
            else:
                risk_level = "🟢 低风险"
            
            # 建议
            if change <= -0.1:
                suggestion = "⚠️ 建议减仓或止损"
            elif change >= 0.2:
                suggestion = "🎯 建议部分止盈"
            elif volatility > 15:
                suggestion = "⚡ 波动较大，注意风险"
            else:
                suggestion = "✅ 风险可控，继续持有"
            
            return {
                'symbol': symbol,
                'entry_price': entry_price,
                'current_price': current_price,
                'change': change,
                'pnl': pnl,
                'volatility_24h': volatility,
                'risk_level': risk_level,
                'suggestion': suggestion,
                'stop_loss_price': entry_price * 0.9,  # 建议止损价
                'take_profit_price': entry_price * 1.2  # 建议止盈价
            }
        except Exception as e:
            logger.error(f"分析 {symbol} 风险失败: {e}")
            return {'error': str(e)}
    
    def get_risk_report(self, portfolio: Dict[str, float]) -> str:
        """生成风险报告"""
        if not portfolio:
            return "暂无持仓"
        
        report = "⚠️ *持仓风险报告*\n\n"
        total_risk = 0
        high_risk_count = 0
        
        for symbol, entry_price in portfolio.items():
            risk = self.analyze_risk(symbol, entry_price, 1.0)
            if 'error' in risk:
                continue
            
            emoji = "🔴" if risk['change'] < -0.1 else "🟡" if risk['change'] < 0 else "🟢"
            report += f"{emoji} *{symbol}*\n"
            report += f"💰 成本: ${risk['entry_price']:,.2f} | 现价: ${risk['current_price']:,.2f}\n"
            report += f"📊 盈亏: {risk['change']*100:+.2f}%\n"
            report += f"{risk['risk_level']}\n"
            report += f"💡 {risk['suggestion']}\n\n"
            
            if risk['change'] < -0.1:
                high_risk_count += 1
            total_risk += abs(risk['change'])
        
        avg_risk = total_risk / len(portfolio) if portfolio else 0
        report += f"📊 平均风险: {avg_risk*100:.2f}%\n"
        report += f"⚠️ 高风险持仓: {high_risk_count} 个"
        
        return report
