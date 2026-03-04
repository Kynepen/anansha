"""
币安 API 客户端封装
"""

import asyncio
from typing import Optional, Dict, List
from binance.client import Client
from binance.streams import BinanceSocketManager
from loguru import logger


class BinanceClient:
    """币安 API 客户端"""
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.bsm = None
        self.socket_manager = None
        logger.info(f"币安客户端初始化完成 (测试网: {testnet})")
    
    def get_ticker_price(self, symbol: str) -> Optional[float]:
        """获取最新价格"""
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            logger.error(f"获取 {symbol} 价格失败: {e}")
            return None
    
    def get_24h_stats(self, symbol: str) -> Optional[Dict]:
        """获取24小时统计"""
        try:
            stats = self.client.get_ticker(symbol=symbol)
            return {
                'symbol': stats['symbol'],
                'price_change': float(stats['priceChange']),
                'price_change_percent': float(stats['priceChangePercent']),
                'weighted_avg_price': float(stats['weightedAvgPrice']),
                'prev_close_price': float(stats['prevClosePrice']),
                'last_price': float(stats['lastPrice']),
                'bid_price': float(stats['bidPrice']),
                'ask_price': float(stats['askPrice']),
                'open_price': float(stats['openPrice']),
                'high_price': float(stats['highPrice']),
                'low_price': float(stats['lowPrice']),
                'volume': float(stats['volume']),
                'quote_volume': float(stats['quoteVolume']),
                'open_time': stats['openTime'],
                'close_time': stats['closeTime'],
                'count': stats['count']
            }
        except Exception as e:
            logger.error(f"获取 {symbol} 24h 统计失败: {e}")
            return None
    
    def get_klines(self, symbol: str, interval: str = '1h', limit: int = 100) -> List[Dict]:
        """获取K线数据"""
        try:
            klines = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
            return [
                {
                    'open_time': k[0],
                    'open': float(k[1]),
                    'high': float(k[2]),
                    'low': float(k[3]),
                    'close': float(k[4]),
                    'volume': float(k[5]),
                    'close_time': k[6],
                    'quote_volume': float(k[7]),
                    'trades': k[8]
                }
                for k in klines
            ]
        except Exception as e:
            logger.error(f"获取 {symbol} K线失败: {e}")
            return []
    
    def get_account(self) -> Optional[Dict]:
        """获取账户信息"""
        try:
            account = self.client.get_account()
            return account
        except Exception as e:
            logger.error(f"获取账户信息失败: {e}")
            return None
    
    def get_symbol_info(self, symbol: str) -> Optional[Dict]:
        """获取交易对信息"""
        try:
            info = self.client.get_symbol_info(symbol)
            return info
        except Exception as e:
            logger.error(f"获取 {symbol} 信息失败: {e}")
            return None
    
    def get_all_tickers(self) -> List[Dict]:
        """获取所有交易对价格"""
        try:
            tickers = self.client.get_all_tickers()
            return [{ 'symbol': t['symbol'], 'price': float(t['price']) } for t in tickers]
        except Exception as e:
            logger.error(f"获取所有价格失败: {e}")
            return []
    
    def get_top_gainers(self, limit: int = 10) -> List[Dict]:
        """获取涨幅榜"""
        try:
            tickers = self.client.get_ticker()
            sorted_tickers = sorted(
                [t for t in tickers if t['symbol'].endswith('USDT')],
                key=lambda x: float(x['priceChangePercent']),
                reverse=True
            )
            return [
                {
                    'symbol': t['symbol'],
                    'price_change_percent': float(t['priceChangePercent']),
                    'last_price': float(t['lastPrice']),
                    'volume': float(t['volume'])
                }
                for t in sorted_tickers[:limit]
            ]
        except Exception as e:
            logger.error(f"获取涨幅榜失败: {e}")
            return []
    
    def get_top_losers(self, limit: int = 10) -> List[Dict]:
        """获取跌幅榜"""
        try:
            tickers = self.client.get_ticker()
            sorted_tickers = sorted(
                [t for t in tickers if t['symbol'].endswith('USDT')],
                key=lambda x: float(x['priceChangePercent'])
            )
            return [
                {
                    'symbol': t['symbol'],
                    'price_change_percent': float(t['priceChangePercent']),
                    'last_price': float(t['lastPrice']),
                    'volume': float(t['volume'])
                }
                for t in sorted_tickers[:limit]
            ]
        except Exception as e:
            logger.error(f"获取跌幅榜失败: {e}")
            return []
    
    def test_connection(self) -> bool:
        """测试连接"""
        try:
            ping = self.client.ping()
            server_time = self.client.get_server_time()
            logger.info(f"币安连接正常，服务器时间: {server_time['serverTime']}")
            return True
        except Exception as e:
            logger.error(f"币安连接失败: {e}")
            return False
