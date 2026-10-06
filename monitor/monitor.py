"""
主监控脚本：定时检查服务健康状态，异常自动告警
用法：python monitor.py
按 Ctrl+C 停止
"""
import time
import requests
import pymysql
from datetime import datetime
from config import TARGETS, DB_CONFIG, CHECK_INTERVAL, RESPONSE_TIME_WARNING
from logger import setup_logger
from notifier import send_alert_email

logger = setup_logger()


def check_http_target(target):
    """检查 HTTP 目标是否正常"""
    name = target["name"]
    url = target["url"]
    timeout = target.get("timeout", 5)
    keyword = target.get("expected_keyword", "")

    try:
        start = time.time()
        resp = requests.get(url, timeout=timeout)
        elapsed = time.time() - start

        # 状态码检查
        if resp.status_code != 200:
            msg = f"{name} 返回异常状态码: {resp.status_code}"
            logger.error(msg)
            send_alert_email(f"{name} 异常", msg)
            return False

        # 关键词检查
        if keyword and keyword not in resp.text:
            msg = f"{name} 返回内容异常，未找到关键词: {keyword}"
            logger.error(msg)
            send_alert_email(f"{name} 内容异常", msg)
            return False

        # 响应时间检查
        if elapsed > RESPONSE_TIME_WARNING:
            logger.warning(f"{name} 响应较慢: {elapsed:.2f}s")
        else:
            logger.info(f"{name} 正常 | 状态码: {resp.status_code} | 耗时: {elapsed:.2f}s")

        return True

    except requests.exceptions.Timeout:
        msg = f"{name} 请求超时（{timeout}秒无响应）"
        logger.error(msg)
        send_alert_email(f"{name} 超时", msg)
        return False
    except requests.exceptions.ConnectionError:
        msg = f"{name} 连接失败，服务可能已停止"
        logger.error(msg)
        send_alert_email(f"{name} 连接失败", msg)
        return False
    except Exception as e:
        msg = f"{name} 检查出错: {e}"
        logger.error(msg)
        send_alert_email(f"{name} 检查出错", msg)
        return False


def check_database():
    """检查 MySQL 数据库是否连通"""
    try:
        conn = pymysql.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            connect_timeout=3
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM phones")
        count = cursor.fetchone()[0]
        conn.close()
        logger.info(f"数据库正常 | phones 表共 {count} 条记录")
        return True
    except Exception as e:
        msg = f"数据库连接失败: {e}"
        logger.error(msg)
        send_alert_email("数据库异常", msg)
        return False


def run_check():
    """执行一轮完整检查"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"========== 开始检查 [{now}] ==========")

    all_ok = True

    # 检查 HTTP 目标
    for target in TARGETS:
        if not check_http_target(target):
            all_ok = False

    # 检查数据库
    if not check_database():
        all_ok = False

    if all_ok:
        logger.info("✅ 全部检查通过\n")
    else:
        logger.warning("⚠️ 存在异常项，已发送告警邮件\n")


def main():
    logger.info("=" * 50)
    logger.info("监控告警系统启动")
    logger.info(f"监控目标数: {len(TARGETS) + 1}（HTTP + 数据库）")
    logger.info(f"检查间隔: {CHECK_INTERVAL} 秒")
    logger.info("按 Ctrl+C 停止")
    logger.info("=" * 50)

    while True:
        run_check()
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("监控已停止")
