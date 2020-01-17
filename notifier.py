#!/usr/bin/env python3
# coding=utf-8
"""
@Desc: A utility to monitor if there is a new comment for valine based blog system
@author: sharp G.
@created: 20200116
"""

import leancloud
#from apscheduler.schedulers.blocking import BlockingScheduler
from core import helper, config

class Misc(object):
    def data_persistence(self, obj_id):
        helper.dir_check()
        temp_data = 'tmp/obj_id'
        with open(temp_data, 'w') as f:
            f.write(obj_id)


class Query(object):
    @property
    def get_query_obj(self):
        leancloud.init(config.leancloud_appid, config.leancloud_appkey)
        query = leancloud.Query('Comment')
        # 获取最新发布的
        query.add_descending('createdAt')
        query.limit(1)
        return query

    def main(self):
        misc=Misc()
        logger=helper.logger_getter()
        first_recent_comment = self.get_query_obj.find()[0]
        comment_content = first_recent_comment.get('comment')
        comment_id = first_recent_comment.get('objectId')
        if not helper.file_check('tmp/obj_id'):    
            misc.data_persistence(comment_id)
            logger.debug('First run and persistent the object id...')
        else:
            last_comment_id=open('tmp/obj_id')
            with open('tmp/obj_id') as f:
                last_comment_text = f.read().strip()
                if last_comment_text != comment_id:
                    helper.mail_send(subject='你的博客有了一个新评论！', mail_body=comment_content)
                    # 有了新的评论，要及时把新的id持久化
                    misc.data_persistence(comment_id)
                    logger.debug('Successfully sent the e-mail.')
                else:
                    logger.debug('There has no new comment for now.')


if __name__ == '__main__':
    q=Query()
    q.main()
    #scheduler = BlockingScheduler()
    #scheduler.add_job(q.main, 'interval', seconds=config.interval)
    #scheduler.start()
