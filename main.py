import os
from util import *
from db.db import *


def work():
    GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')
    MAIL_TOKEN = os.getenv('MAIL_TOKEN')

    if not GITHUB_ACCESS_TOKEN or not MAIL_TOKEN:
        raise Exception('环境变量没有配置')
    
    owner = "movefuns"
    name = "web3startrek"

    new_notice = get_discussions(GITHUB_ACCESS_TOKEN, owner, name)[0]

    if not is_discussion_exists(new_notice['id']):
        logger.debug(f"新增讨论：{new_notice}")
        content = f"新增讨论：{new_notice['title']} \n链接: {new_notice['url']}"
        new_discussion(new_notice['id'], new_notice['title'], new_notice['url'])
        # send_mail(MAIL_TOKEN, content)
    else:
        # logger.debug(f'{owner}/{name} 暂无更新')
        pass
    

if __name__ == '__main__':
    from apscheduler.schedulers.blocking import BlockingScheduler
    
    scheduler = BlockingScheduler()
    scheduler.add_job(work, 'interval', seconds=60)
    scheduler.start()



