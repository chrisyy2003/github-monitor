import smtplib
from email.mime.text import MIMEText
import requests
from loguru import logger
import sys

# logger.add(sys.stdout, format="{time} {level} {message}", filter="my_module", level="INFO")
logger.add("app.log", rotation="10 MB")

def send_mail(password, content):
    # 向本地开发邮件服务器发送一条简单的文本信息

    # 发送者的邮箱  example.com是专门用于文档中的说明性示例的域名
    sender = '1017975501@qq.com'
    # 接收者的邮箱，接收者可以是多个，因此是一个列表
    receivers = ['1017975501@qq.com']

    # 发送到服务器的文本信息
    subject = 'Github 监控通知'
    msg = MIMEText(content)

    # msg['Subject']是发送邮件的主题
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receivers[0]


    # 发送邮件时qq邮箱，对应qq邮箱服务器域名时smtp.qq.com  对应端口时465
    with smtplib.SMTP_SSL(host='smtp.qq.com', port=465) as server:
        # 登录发送者的邮箱
        server.login(sender, password)

        # 开始发送邮件
        server.sendmail(sender, receivers, msg.as_string())
        logger.success("Successfully sent email")


    '''
    上面发送邮件部分也可以写成：
    server = smtplib.SMTP_SSL(host='smtp.qq.com', port=465) 
    server.login(sender, password)

    server.sendmail(sender, receivers, msg.as_string())
    server.quit()
    '''


def get_discussions(token, owner, name) -> list:
    # GraphQL 查询
    query = """
    query($owner: String!, $name: String!) {
    repository(owner: $owner, name: $name) {
        discussions(first: 1) {
        nodes {
            id
            title
            url
            createdAt
        }
        }
    }
    }
    """

    # GraphQL 变量
    variables = {
        "owner": owner,
        "name": name
    }

    # 发送 GraphQL 请求
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers={"Authorization": f"Bearer {token}"}
    )

    # 解析响应
    return response.json()["data"]["repository"]["discussions"]["nodes"]


