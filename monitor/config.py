"""
监控配置文件
改成你自己的监控目标和告警邮箱
"""

# ========== 监控目标 ==========
TARGETS = [
    {
        "name": "小程序后端API",
        "url": "http://localhost/campus-phone-backend/api/phones.php?action=list",
        "timeout": 5,
        "expected_keyword": "教务处",
    },
]

# ========== 数据库监控 ==========
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",       # 改成你自己的 MySQL 密码
    "database": "campus_phone",
}

# ========== 告警配置（邮件） ==========
ALERT_EMAIL = {
    "smtp_server": "smtp.qq.com",
    "smtp_port": 465,
    "sender": "你的邮箱@qq.com",
    "password": "你的SMTP授权码",  # 注意：不是登录密码，是SMTP授权码
    "receiver": "接收告警的邮箱@qq.com",
}

# ========== 监控参数 ==========
CHECK_INTERVAL = 60          # 每隔多少秒检查一次
RESPONSE_TIME_WARNING = 2.0  # 响应超过2秒算警告
LOG_FILE = "monitor.log"      # 日志文件路径
