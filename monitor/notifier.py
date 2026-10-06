"""
告警通知模块：发送邮件告警
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import ALERT_EMAIL


def send_alert_email(title, content):
    """发送告警邮件"""
    msg = MIMEMultipart()
    msg['From'] = ALERT_EMAIL['sender']
    msg['To'] = ALERT_EMAIL['receiver']
    msg['Subject'] = f"[监控告警] {title}"

    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP_SSL(ALERT_EMAIL['smtp_server'], ALERT_EMAIL['smtp_port'])
        server.login(ALERT_EMAIL['sender'], ALERT_EMAIL['password'])
        server.sendmail(
            ALERT_EMAIL['sender'],
            ALERT_EMAIL['receiver'],
            msg.as_string()
        )
        server.quit()
        return True
    except Exception as e:
        print(f"[告警] 邮件发送失败: {e}")
        return False
