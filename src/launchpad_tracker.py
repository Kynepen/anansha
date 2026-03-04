"""
Launchpad/Launchpool 追踪模块
"""

import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
from loguru import logger


class LaunchpadTracker:
    """Launchpad/Launchpool 追踪器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.check_interval = config.get('check_interval', 3600)
        self.data_file = Path('data/launchpad_data.json')
        self.projects = self._load_data()
        logger.info("Launchpad 追踪器初始化完成")
    
    def _load_data(self) -> Dict:
        """加载数据"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"加载 Launchpad 数据失败: {e}")
        return {'tracked': [], 'history': []}
    
    def _save_data(self):
        """保存数据"""
        try:
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.projects, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"保存 Launchpad 数据失败: {e}")
    
    def add_project(self, project: Dict) -> bool:
        """添加项目追踪"""
        try:
            project_id = project.get('id') or project.get('name', '')
            self.projects['tracked'].append({
                'id': project_id,
                'name': project.get('name'),
                'symbol': project.get('symbol'),
                'type': project.get('type', 'launchpad'),  # launchpad or launchpool
                'sale_start': project.get('sale_start'),
                'sale_end': project.get('sale_end'),
                'total_supply': project.get('total_supply'),
                'sale_price': project.get('sale_price'),
                'platform': project.get('platform', 'binance'),
                'added_at': datetime.now().isoformat(),
                'status': 'upcoming'
            })
            self._save_data()
            logger.info(f"添加项目追踪: {project.get('name')}")
            return True
        except Exception as e:
            logger.error(f"添加项目失败: {e}")
            return False
    
    def check_upcoming(self) -> List[Dict]:
        """检查即将开始的项目"""
        upcoming = []
        now = datetime.now()
        
        for project in self.projects['tracked']:
            if project.get('status') != 'upcoming':
                continue
            
            sale_start = project.get('sale_start')
            if sale_start:
                try:
                    start_time = datetime.fromisoformat(sale_start)
                    hours_until = (start_time - now).total_seconds() / 3600
                    
                    # 24小时内开始
                    if 0 < hours_until <= 24:
                        project['hours_until'] = hours_until
                        upcoming.append(project)
                except:
                    pass
        
        return upcoming
    
    def get_active_projects(self) -> List[Dict]:
        """获取进行中项目"""
        return [p for p in self.projects['tracked'] if p.get('status') == 'active']
    
    def get_upcoming_summary(self) -> str:
        """获取即将开始的项目摘要"""
        upcoming = self.check_upcoming()
        
        if not upcoming:
            return "🚀 未来24小时内暂无新项目"
        
        summary = "🚀 *即将开始的项目*\n\n"
        
        for project in upcoming:
            summary += f"📌 *{project['name']}* ({project['symbol']})\n"
            summary += f"⏰ 开始时间: {project['hours_until']:.1f} 小时后\n"
            summary += f"💰 销售价: {project.get('sale_price', 'TBA')}\n"
            summary += f"🎯 类型: {'Launchpad' if project['type'] == 'launchpad' else 'Launchpool'}\n\n"
        
        return summary
    
    def format_project_info(self, project: Dict) -> str:
        """格式化项目信息"""
        info = f"""📌 *{project.get('name', 'Unknown')}* ({project.get('symbol', '')})

🎯 类型: {'Launchpad' if project.get('type') == 'launchpad' else 'Launchpool'}
⏰ 开始: {project.get('sale_start', 'TBA')}
⏰ 结束: {project.get('sale_end', 'TBA')}
💰 销售价: {project.get('sale_price', 'TBA')}
🪙 总量: {project.get('total_supply', 'TBA')}
📊 平台: {project.get('platform', 'Binance').capitalize()}
"""
        return info
    
    def simulate_return(self, investment: float, sale_price: float, listing_price: float) -> Dict:
        """模拟收益"""
        coins = investment / sale_price
        value_at_listing = coins * listing_price
        profit = value_at_listing - investment
        roi = (profit / investment) * 100 if investment > 0 else 0
        
        return {
            'investment': investment,
            'coins_received': coins,
            'sale_price': sale_price,
            'listing_price': listing_price,
            'value_at_listing': value_at_listing,
            'profit': profit,
            'roi': roi
        }
    
    def get_roi_simulation_report(self, project: Dict, scenarios: List[float] = None) -> str:
        """获取收益模拟报告"""
        if scenarios is None:
            scenarios = [1.5, 2.0, 3.0, 5.0, 10.0]  # 不同倍数
        
        sale_price = project.get('sale_price', 0)
        if not sale_price:
            return "无法模拟：缺少销售价"
        
        report = f"📊 *{project.get('name')} 收益模拟*\n"
        report += f"💰 投入: 1000 USDT\n"
        report += f"🎯 发行价: ${sale_price}\n\n"
        
        for multiplier in scenarios:
            listing_price = sale_price * multiplier
            result = self.simulate_return(1000, sale_price, listing_price)
            report += f"🚀 {multiplier}x 开盘: +{result['profit']:.2f} USDT ({result['roi']:+.0f}%)\n"
        
        return report
