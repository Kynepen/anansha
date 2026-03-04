"""
定投助手模块 - 智能定投策略
"""

import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
from loguru import logger

from .binance_client import BinanceClient


class DCAHelper:
    """定投助手"""
    
    def __init__(self, binance_client: BinanceClient, config: Dict):
        self.client = binance_client
        self.config = config
        self.default_amount = config.get('default_amount', 100)
        self.default_frequency = config.get('default_frequency', 'weekly')
        self.plans_file = Path('data/dca_plans.json')
        self.plans = self._load_plans()
        logger.info("定投助手初始化完成")
    
    def _load_plans(self) -> Dict:
        """加载定投计划"""
        if self.plans_file.exists():
            try:
                with open(self.plans_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"加载定投计划失败: {e}")
        return {}
    
    def _save_plans(self):
        """保存定投计划"""
        try:
            self.plans_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.plans_file, 'w', encoding='utf-8') as f:
                json.dump(self.plans, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"保存定投计划失败: {e}")
    
    def create_plan(self, symbol: str, amount: float, frequency: str = 'weekly', 
                   start_date: Optional[str] = None) -> Dict:
        """创建定投计划"""
        plan_id = f"{symbol}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        if start_date is None:
            start_date = datetime.now().isoformat()
        
        plan = {
            'id': plan_id,
            'symbol': symbol,
            'amount': amount,
            'frequency': frequency,  # daily, weekly, biweekly, monthly
            'start_date': start_date,
            'next_invest_date': start_date,
            'total_invested': 0,
            'total_coins': 0,
            'investments': [],
            'created_at': datetime.now().isoformat(),
            'active': True
        }
        
        self.plans[plan_id] = plan
        self._save_plans()
        
        logger.info(f"创建定投计划: {plan_id}")
        return plan
    
    def get_plan(self, plan_id: str) -> Optional[Dict]:
        """获取定投计划"""
        return self.plans.get(plan_id)
    
    def list_plans(self) -> List[Dict]:
        """列出所有定投计划"""
        return [plan for plan in self.plans.values() if plan['active']]
    
    def record_investment(self, plan_id: str, price: float, amount: float = None):
        """记录定投"""
        plan = self.plans.get(plan_id)
        if not plan:
            logger.error(f"定投计划不存在: {plan_id}")
            return None
        
        if amount is None:
            amount = plan['amount']
        
        coins_bought = amount / price
        
        investment = {
            'date': datetime.now().isoformat(),
            'price': price,
            'amount': amount,
            'coins': coins_bought
        }
        
        plan['investments'].append(investment)
        plan['total_invested'] += amount
        plan['total_coins'] += coins_bought
        
        # 更新下次投资日期
        plan['next_invest_date'] = self._calculate_next_date(
            plan['frequency'], 
            datetime.now()
        ).isoformat()
        
        self._save_plans()
        logger.info(f"记录定投: {plan_id} 投入 {amount} USDT 买入 {coins_bought:.6f} {plan['symbol']}")
        return investment
    
    def _calculate_next_date(self, frequency: str, from_date: datetime) -> datetime:
        """计算下次投资日期"""
        if frequency == 'daily':
            return from_date + timedelta(days=1)
        elif frequency == 'weekly':
            return from_date + timedelta(weeks=1)
        elif frequency == 'biweekly':
            return from_date + timedelta(weeks=2)
        elif frequency == 'monthly':
            # 简单处理：加30天
            return from_date + timedelta(days=30)
        else:
            return from_date + timedelta(weeks=1)
    
    def get_plan_report(self, plan_id: str) -> str:
        """获取定投报告"""
        plan = self.plans.get(plan_id)
        if not plan:
            return "定投计划不存在"
        
        current_price = self.client.get_ticker_price(plan['symbol'])
        if current_price is None:
            current_price = 0
        
        total_value = plan['total_coins'] * current_price
        profit_loss = total_value - plan['total_invested']
        profit_percent = (profit_loss / plan['total_invested'] * 100) if plan['total_invested'] > 0 else 0
        
        report = f"""💰 *定投计划报告*

📊 币种: {plan['symbol']}
💵 每次投入: {plan['amount']} USDT
📅 频率: {plan['frequency']}
🔄 投资次数: {len(plan['investments'])}

📈 累计投入: {plan['total_invested']:.2f} USDT
🪙 持有数量: {plan['total_coins']:.6f}
💰 当前价值: {total_value:.2f} USDT
📊 盈亏: {profit_loss:+.2f} USDT ({profit_percent:+.2f}%)
"""
        
        if plan['investments']:
            avg_price = plan['total_invested'] / plan['total_coins'] if plan['total_coins'] > 0 else 0
            report += f"📊 均价: ${avg_price:,.2f}\n"
            report += f"💵 现价: ${current_price:,.2f}\n"
        
        return report
    
    def get_all_plans_summary(self) -> str:
        """获取所有定投计划摘要"""
        active_plans = self.list_plans()
        
        if not active_plans:
            return "暂无定投计划"
        
        summary = "📋 *定投计划总览*\n\n"
        total_invested = 0
        total_value = 0
        
        for plan in active_plans:
            current_price = self.client.get_ticker_price(plan['symbol']) or 0
            value = plan['total_coins'] * current_price
            total_invested += plan['total_invested']
            total_value += value
            
            summary += f"• {plan['symbol']}: 投入 {plan['total_invested']:.2f} USDT | 现值 {value:.2f} USDT\n"
        
        total_pnl = total_value - total_invested
        total_pnl_percent = (total_pnl / total_invested * 100) if total_invested > 0 else 0
        
        summary += f"\n💰 总投入: {total_invested:.2f} USDT\n"
        summary += f"💵 总现值: {total_value:.2f} USDT\n"
        summary += f"📊 总盈亏: {total_pnl:+.2f} USDT ({total_pnl_percent:+.2f}%)"
        
        return summary
    
    def delete_plan(self, plan_id: str) -> bool:
        """删除定投计划"""
        if plan_id in self.plans:
            self.plans[plan_id]['active'] = False
            self._save_plans()
            logger.info(f"删除定投计划: {plan_id}")
            return True
        return False
