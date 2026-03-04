"""
币安 Academy 学习助手模块
"""

import json
from typing import Dict, List
from datetime import datetime
from pathlib import Path
from loguru import logger


class AcademyHelper:
    """币安 Academy 学习助手"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.check_interval = config.get('check_interval', 86400)
        self.data_file = Path('data/academy_data.json')
        self.data = self._load_data()
        self.articles = self._get_default_articles()
        logger.info("Academy 学习助手初始化完成")
    
    def _load_data(self) -> Dict:
        """加载数据"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"加载 Academy 数据失败: {e}")
        return {'user_progress': {}, 'completed_articles': []}
    
    def _save_data(self):
        """保存数据"""
        try:
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"保存 Academy 数据失败: {e}")
    
    def _get_default_articles(self) -> List[Dict]:
        """获取默认文章列表"""
        return [
            {
                'id': 'beginner_crypto',
                'title': '加密货币入门指南',
                'category': 'beginner',
                'level': '初级',
                'description': '了解什么是加密货币，如何开始你的加密之旅',
                'url': 'https://academy.binance.com/zh/articles/what-is-cryptocurrency',
                'estimated_time': '15 分钟'
            },
            {
                'id': 'blockchain_basics',
                'title': '区块链技术基础',
                'category': 'technology',
                'level': '初级',
                'description': '深入了解区块链技术的工作原理',
                'url': 'https://academy.binance.com/zh/articles/what-is-blockchain-technology',
                'estimated_time': '20 分钟'
            },
            {
                'id': 'trading_basics',
                'title': '交易基础教程',
                'category': 'trading',
                'level': '初级',
                'description': '学习基本的交易概念和策略',
                'url': 'https://academy.binance.com/zh/articles/crypto-trading-guide',
                'estimated_time': '25 分钟'
            },
            {
                'id': 'defi_intro',
                'title': 'DeFi 入门',
                'category': 'defi',
                'level': '中级',
                'description': '了解去中心化金融的基本概念',
                'url': 'https://academy.binance.com/zh/articles/what-is-defi',
                'estimated_time': '20 分钟'
            },
            {
                'id': 'nft_guide',
                'title': 'NFT 完全指南',
                'category': 'nft',
                'level': '中级',
                'description': '全面了解 NFT 是什么以及如何使用',
                'url': 'https://academy.binance.com/zh/articles/what-are-nfts',
                'estimated_time': '18 分钟'
            },
            {
                'id': 'technical_analysis',
                'title': '技术分析入门',
                'category': 'trading',
                'level': '中级',
                'description': '学习如何阅读图表和技术指标',
                'url': 'https://academy.binance.com/zh/articles/technical-analysis-for-beginners',
                'estimated_time': '30 分钟'
            },
            {
                'id': 'risk_management',
                'title': '风险管理策略',
                'category': 'trading',
                'level': '高级',
                'description': '学习如何保护你的投资和管理风险',
                'url': 'https://academy.binance.com/zh/articles/crypto-risk-management',
                'estimated_time': '25 分钟'
            },
            {
                'id': 'staking_guide',
                'title': '质押收益指南',
                'category': 'earning',
                'level': '中级',
                'description': '了解如何通过质押赚取被动收益',
                'url': 'https://academy.binance.com/zh/articles/what-is-staking',
                'estimated_time': '15 分钟'
            }
        ]
    
    def get_recommendations(self, user_level: str = 'beginner', category: str = None) -> List[Dict]:
        """获取推荐文章"""
        filtered = self.articles
        
        # 按等级过滤
        if user_level:
            level_map = {
                'beginner': ['初级'],
                'intermediate': ['初级', '中级'],
                'advanced': ['初级', '中级', '高级']
            }
            allowed_levels = level_map.get(user_level, ['初级'])
            filtered = [a for a in filtered if a['level'] in allowed_levels]
        
        # 按分类过滤
        if category:
            filtered = [a for a in filtered if a['category'] == category]
        
        # 排除已完成的
        completed = self.data.get('completed_articles', [])
        filtered = [a for a in filtered if a['id'] not in completed]
        
        return filtered[:3]  # 返回前3个推荐
    
    def mark_completed(self, article_id: str) -> bool:
        """标记文章已完成"""
        if article_id not in self.data.get('completed_articles', []):
            self.data.setdefault('completed_articles', []).append(article_id)
            self._save_data()
            logger.info(f"文章完成: {article_id}")
            return True
        return False
    
    def get_progress(self) -> Dict:
        """获取学习进度"""
        completed = len(self.data.get('completed_articles', []))
        total = len(self.articles)
        progress_percent = (completed / total * 100) if total > 0 else 0
        
        return {
            'completed': completed,
            'total': total,
            'progress_percent': progress_percent
        }
    
    def get_daily_lesson(self) -> str:
        """获取每日一课"""
        recommendations = self.get_recommendations()
        
        if not recommendations:
            return "🎉 恭喜！你已经完成了所有推荐课程！"
        
        article = recommendations[0]
        
        lesson = f"""📚 *每日一课*

📖 *{article['title']}*
🏷️ 分类: {article['category'].upper()}
📊 难度: {article['level']}
⏱️ 预计阅读时间: {article['estimated_time']}

📝 {article['description']}

🔗 [点击阅读]({article['url']})

💡 提示: 阅读完成后可以标记为已完成，获得下一课推荐！"""
        
        return lesson
    
    def get_learning_path(self, goal: str = 'trading') -> str:
        """获取学习路径"""
        paths = {
            'trading': {
                'name': '交易高手之路',
                'steps': [
                    '加密货币入门指南',
                    '交易基础教程',
                    '技术分析入门',
                    '风险管理策略'
                ]
            },
            'defi': {
                'name': 'DeFi 探索者',
                'steps': [
                    '加密货币入门指南',
                    '区块链技术基础',
                    'DeFi 入门',
                    '质押收益指南'
                ]
            },
            'beginner': {
                'name': '新手指南',
                'steps': [
                    '加密货币入门指南',
                    '区块链技术基础',
                    '交易基础教程'
                ]
            }
        }
        
        path = paths.get(goal, paths['beginner'])
        
        report = f"🎯 *{path['name']}*\n\n推荐学习顺序:\n\n"
        for i, step in enumerate(path['steps'], 1):
            # 查找文章
            article = next((a for a in self.articles if a['title'] == step), None)
            if article:
                status = "✅" if article['id'] in self.data.get('completed_articles', []) else "⬜"
                report += f"{status} {i}. {step}\n"
        
        return report
    
    def get_categories(self) -> List[str]:
        """获取所有分类"""
        return list(set(a['category'] for a in self.articles))
