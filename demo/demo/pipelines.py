# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from .items import *

class MySQLPipeline(object):
    def open_spider(self, spider):
        self.conn = MySQLdb.connect('localhost', 'root', 'wohenhaoqi', 'Zhihu', charset='utf8mb4', use_unicode=True)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        if isinstance(item, PersonItem):
            self.cursor.execute('INSERT INTO Person VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', %s, %s, %s, %s, %s, %s)' % (item['id'], item['name'], item['place'], item['bussiness'], item['job_exp'], item['edu_exp'], item['introduce'], item['answer_num'], item['question_num'], item['article_num'], item['column_num'], item['following_num'], item['follower_num'], ))
        if isinstance(item, FollowingItem):
            self.cursor.execute('INSERT INTO Following VALUES (\'%s\', \'%s\')' % (item['person_id'], item['following_id']))
        if isinstance(item, FollowersItem):
            self.cursor.execute('INSERT INTO Followers VALUES (\'%s\', \'%s\')' % (item['person_id'], item['followers_id']))
        if isinstance(item, AnswersItem):
            self.cursor.execute('INSERT INTO Answers VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % (item['author_id'], item['question_text'], item['question_link'], item['answer_content'], item['answer_time'], item['upvote_num'], item['comment_num']))
        if isinstance(item, ArticlesItem):
            self.cursor.execute('INSERT INTO Articles VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % (item['article_id'], item['person_id'], item['article_title'], item['article_link'], item['article_content'], item['upvote_num'], item['comment_num']))
        if isinstance(item, ArticleCommentItem):
            self.cursor.execute('INSERT INTO Article_comment VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % (item['article_id'], item['comment_person_name'], item['comment_content'], item['comment_time'], item['upvote_num']))
        self.conn.commit()
        return item

