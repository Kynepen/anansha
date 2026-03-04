# 安安虾 (AnAnXia) 安全审计报告

**审计日期:** 2026-03-04  
**审计范围:** https://github.com/Kynepen/anansha  
**审计类型:** 本地安全风险评估

---

## 🛡️ 总体评估

| 评估项 | 评级 | 说明 |
|--------|------|------|
| **代码安全** | 🟢 低风险 | 整体架构良好，无明显高危漏洞 |
| **配置安全** | 🟡 中风险 | 需要用户自行妥善保管API密钥 |
| **依赖安全** | 🟢 低风险 | 使用主流库，但需定期更新 |
| **数据安全** | 🟢 低风险 | 本地存储，无云端传输敏感数据 |

**综合风险等级: 🟢 低风险 (可安全使用)**

---

## ✅ 安全亮点

### 1. 配置分离设计 ✅
```
config/
├── config.example.json    # 示例配置（可提交到Git）
└── config.json            # 真实配置（已被.gitignore排除）
```
**好评:** 敏感配置被正确排除在版本控制之外

### 2. 无硬编码密钥 ✅
- 代码中没有发现硬编码的 API Key/Secret
- 所有密钥均通过配置文件传入
- 示例配置使用占位符 `YOUR_BINANCE_API_KEY`

### 3. 只读API权限设计 ✅
- 当前实现仅使用币安公共API和只读接口
- 没有下单、转账等写入操作
- 即使API密钥泄露，攻击者也无法操作资金

### 4. 本地数据处理 ✅
- 所有数据本地存储 (`data/` 目录)
- 定投计划、配置等敏感信息不上传云端
- 隐私数据完全由用户控制

---

## ⚠️ 发现的风险与建议

### 🟡 中风险 - 配置文件权限

**问题描述:**
配置文件 `config/config.json` 包含敏感信息，但代码中没有检查文件权限。

**潜在风险:**
- 其他用户/程序可能读取配置文件
- 备份时可能意外包含敏感文件

**修复建议:**
```python
# 在 _load_config 方法中添加权限检查
import os
import stat

def _load_config(self, config_path: str) -> Dict:
    # 检查文件权限
    if os.path.exists(config_path):
        mode = os.stat(config_path).st_mode
        if mode & stat.S_IRWXG or mode & stat.S_IRWXO:
            logger.warning(f"配置文件权限过于宽松，建议设置为 600: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)
```

**用户操作:**
```bash
chmod 600 config/config.json
```

---

### 🟡 中风险 - API密钥内存安全

**问题描述:**
API密钥加载后存储在内存中，可能被内存转储读取。

**潜在风险:**
- 程序崩溃时可能产生包含密钥的core dump
- 低权限进程可能读取进程内存

**缓解措施:**
- 使用只读API密钥（无法交易/提现）
- 限制IP白名单（币安后台可配置）
- 启用测试网模式进行开发测试

**建议:**
用户应在币安后台：
1. 创建 **只读API密钥**（不要启用交易/提现权限）
2. 设置 **IP白名单**
3. 启用 **测试网** 进行功能验证

---

### 🟡 中风险 - Telegram Bot Token 安全

**问题描述:**
Telegram Bot Token 同样存储在配置文件中。

**潜在风险:**
- Token泄露后他人可控制Bot发送消息
- 可能收到恶意推送

**建议:**
1. 不要将Bot Token提交到Git
2. 使用单独的Bot（非个人主账号）
3. 定期更换Bot Token

---

### 🟢 低风险 - 依赖包安全

**问题描述:**
依赖包可能存在已知漏洞。

**当前依赖:**
```
python-binance>=1.0.19
python-telegram-bot>=20.7
pandas>=2.0.0
numpy>=1.24.0
...
```

**建议:**
```bash
# 定期更新依赖
pip install --upgrade -r requirements.txt

# 使用 safety 检查依赖漏洞
pip install safety
safety check -r requirements.txt
```

---

### 🟢 低风险 - 日志安全

**问题描述:**
日志可能包含敏感信息。

**当前实现:**
使用 `loguru` 记录日志，但没有过滤敏感字段。

**建议:**
```python
# 添加日志过滤器，脱敏敏感信息
def sanitize_log(record):
    if "api_key" in record["message"]:
        record["message"] = record["message"].replace(record["extra"]["api_key"], "***")
    return record

logger.add("logs/anansha.log", filter=sanitize_log)
```

---

### 🟢 低风险 - 子进程调用

**问题描述:**
`notifier.py` 使用 `subprocess.run` 调用 `openclaw` 命令。

**代码位置:** `src/notifier.py`
```python
result = subprocess.run(
    [
        'openclaw', 'message', 'send',
        '--channel', 'telegram',
        '--to', self.chat_id.replace('telegram:', ''),
        '--text', message
    ],
    ...
)
```

**风险评估:**
- `message` 内容可能包含用户输入
- 但 `subprocess.run` 使用列表形式传入参数，不是shell字符串
- 因此不存在命令注入漏洞

**状态:** ✅ 安全

---

## 🔒 安全加固建议

### 1. 文件权限加固
```bash
# 配置文件仅所有者可读写
chmod 600 config/config.json

# 项目目录权限
chmod 700 /home/kyne/.openclaw/workspace/anansha
```

### 2. API密钥最佳实践
- ✅ 使用只读API密钥
- ✅ 设置IP白名单
- ✅ 启用测试网验证
- ✅ 定期更换密钥

### 3. 运行环境安全
```bash
# 使用虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖时验证哈希
pip install --require-hashes -r requirements.txt
```

### 4. 监控与告警
- 监控异常API调用
- 设置GitHub安全警报
- 定期审查访问日志

---

## 📋 安全检查清单

### 部署前检查
- [ ] `config/config.json` 权限设置为 600
- [ ] 币安API密钥为只读权限
- [ ] 币安API设置了IP白名单
- [ ] `.gitignore` 包含 `config/config.json`
- [ ] 使用虚拟环境运行

### 运行时检查
- [ ] 定期检查日志是否有异常
- [ ] 监控API调用频率
- [ ] 关注依赖包安全更新

---

## 🎯 审计结论

**安安虾项目整体安全状况良好，没有发现高危漏洞。**

主要风险集中在：
1. 配置文件权限管理（用户可控）
2. API密钥保管（用户可控）
3. 依赖包更新（需定期检查）

**建议用户:**
- 严格按照安全加固建议配置
- 使用只读API密钥
- 定期检查并更新依赖

**项目可安全用于生产环境。** ✅

---

## 🔗 参考资源

- [币安API安全最佳实践](https://www.binance.com/en/support/faq/security-tips-for-your-binance-account-360043074591)
- [Python安全编码指南](https://python-security.readthedocs.io/)
- [GitHub安全文档](https://docs.github.com/en/code-security)

---

*本报告由 AI 安全审计助手生成*
