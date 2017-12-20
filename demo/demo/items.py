# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PersonItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    place = scrapy.Field()
    bussiness = scrapy.Field()
    job_exp = scrapy.Field()
    edu_exp = scrapy.Field()
    introduce = scrapy.Field()
    answer_num = scrapy.Field()
    question_num = scrapy.Field()
    article_num = scrapy.Field()
    column_num = scrapy.Field()
    following_num = scrapy.Field()
    follower_num = scrapy.Field()

class FollowingItem(scrapy.Item):
    person_id = scrapy.Field()
    following_id = scrapy.Field()

class FollowersItem(scrapy.Item):
    person_id = scrapy.Field()
    followers_id = scrapy.Field()

class AnswersItem(scrapy.Item):
    author_id = scrapy.Field()
    question_text = scrapy.Field()
    question_link = scrapy.Field()
    answer_content = scrapy.Field()
    answer_time = scrapy.Field()
    upvote_num = scrapy.Field()
    comment_num = scrapy.Field()

class ArticlesItem(scrapy.Item):
    person_id = scrapy.Field()
    article_id = scrapy.Field()
    article_title = scrapy.Field()
    article_link = scrapy.Field()
    article_content = scrapy.Field()
    upvote_num = scrapy.Field()
    comment_num = scrapy.Field()

class ArticleCommentItem(scrapy.Item):
    article_id = scrapy.Field()
    comment_person_name = scrapy.Field()
    comment_content = scrapy.Field()
    comment_time = scrapy.Field()
    upvote_num = scrapy.Field()
