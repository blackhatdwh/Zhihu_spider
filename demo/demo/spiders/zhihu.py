import scrapy
import json
from ..items import *

class ZhihuSpider(scrapy.Spider):
    name = "zhihu"


    def log(self, response):
        with open('log.html', 'wb') as f:
            f.write(response.body)

    def start_requests(self):
        people_id = ['excited-vczh', 'sizhuren']
        requests = []
        for p in people_id:
            requests.append(scrapy.Request(url='https://www.zhihu.com/people/%s/activities' % p, callback = self.parse_activities))
            for i in range(1, 6):
                requests.append(scrapy.Request(url='https://www.zhihu.com/people/%s/following?page=%s' %(p, i), callback = self.parse_following))
            for i in range(1, 6):
                requests.append(scrapy.Request(url='https://www.zhihu.com/people/%s/followers?page=%s' %(p, i), callback = self.parse_followers))
            for i in range(1, 26):
                requests.append(scrapy.Request(url='https://www.zhihu.com/people/%s/answers?page=%s' %(p, i), callback = self.parse_answers))
            for i in range(1, 26):
                requests.append(scrapy.Request(url='https://www.zhihu.com/people/%s/posts?page=%s' %(p, i), callback = self.parse_posts))
        return requests

    def parse_activities(self, response):
        item = PersonItem()
        item['id'] = response.url.split('/')[4].replace("'", '"')
        item['name'] = response.css('span.ProfileHeader-name::text')[0].extract().replace("'", '"')
        item['following_num'] = response.css('div.NumberBoard-value::text')[0].extract().replace("'", '"')
        item['follower_num'] = response.css('div.NumberBoard-value::text')[1].extract().replace("'", '"')
        item['answer_num'] = response.css('span.Tabs-meta::text')[0].extract().replace("'", '"')
        item['question_num'] = response.css('span.Tabs-meta::text')[1].extract().replace("'", '"')
        item['article_num'] = response.css('span.Tabs-meta::text')[2].extract().replace("'", '"')
        item['column_num'] = response.css('span.Tabs-meta::text')[3].extract().replace("'", '"')
        item['place'] = ''
        item['bussiness'] = ''
        item['job_exp'] = ''
        item['edu_exp'] = ''
        item['introduce'] = ''

        for i in range(5):
            try:
                label = response.css('span.ProfileHeader-detailLabel::text')[i].extract()
                value = ''
                if label == '居住地':
                    for j in range(100):
                        try:
                            value = value + response.css('div.ProfileHeader-detailValue')[i].css('span::text')[j].extract() + ' '
                        except IndexError: break
                    item['place'] = value.replace("'", '"')
                if label == '所在行业':
                    value = response.css('div.ProfileHeader-detailValue')[i].css('div.ProfileHeader-detailValue::text')[0].extract()
                    item['bussiness'] = value.replace("'", '"')
                if label == '职业经历':
                    for j in range(100):
                        try:
                            value = value + response.css('div.ProfileHeader-detailValue')[i].css('div.ProfileHeader-field::text')[j].extract() + ' '
                        except IndexError: break
                    item['job_exp'] = value.replace("'", '"')
                if label == '教育经历':
                    for j in range(100):
                        try:
                            value = value + response.css('div.ProfileHeader-detailValue')[i].css('div.ProfileHeader-field::text')[j].extract() + ' '
                        except IndexError: break
                    item['edu_exp'] = value.replace("'", '"')
                if label == '个人简介':
                    for j in range(100):
                        try:
                            # doesn't contain links
                            if response.css('div.ProfileHeader-detailValue')[i].xpath('node()')[j].css('a::attr(href)').extract() == []:
                                if response.css('div.ProfileHeader-detailValue')[i].xpath('node()')[j].extract() == r'<br>':
                                    value += '\n'
                                else:
                                    value = value + response.css('div.ProfileHeader-detailValue')[i].xpath('node()')[j].extract() + ' '
                            # get the link text and href
                            else:
                                value = value + response.css('div.ProfileHeader-detailValue')[i].xpath('node()')[j].css('span.visible::text')[0].extract() + '(' + response.css('div.ProfileHeader-detailValue')[i].xpath('node()')[j].css('a::attr(href)')[0].extract() + ') '
                        except IndexError: break
                    item['introduce'] = value.replace("'", '"')
            except IndexError: break
        return item


    def parse_following(self, response):
        person_id = response.url.split('/')[4].replace("'", '"')
        items = []
        for i in range(100):
            try:
                item = FollowingItem()
                item['person_id'] = person_id
                item['following_id'] = response.css('a.UserLink-link::text').extract()[i].replace("'", '"')
                items.append(item)
            except IndexError: break
        return items

    def parse_followers(self, response):
        person_id = response.url.split('/')[4].replace("'", '"')
        items = []
        for i in range(100):
            try:
                item = FollowersItem()
                item['person_id'] = person_id
                item['followers_id'] = response.css('a.UserLink-link::text').extract()[i].replace("'", '"')
                items.append(item)
            except IndexError: break
        return items


        
    def parse_answers(self, response):
        person_id = response.url.split('/')[4].replace("'", '"')
        items = []

        time_arr = response.css('div.ContentItem-time a').xpath('.//text()').extract()
        for i in range(len(time_arr)):
            try:
                if time_arr[i][0] == '编':
                    time_arr[i] += time_arr[i+1]
                    time_arr.pop(i+1)
            except IndexError: break
        for i in range(20):
            item = AnswersItem()
            item['author_id'] = person_id
            #question text
            #print(response.css('div.List-item div.AnswerItem')[i].css('h2.ContentItem-title').xpath('./div/a//text()').extract()[0])
            item['question_text'] = response.css('div.List-item div.AnswerItem')[i].css('h2.ContentItem-title').xpath('./div/a//text()').extract()[0].replace("'", '"')

            #question url
            #print(response.urljoin(response.css('h2.ContentItem-title').xpath('./div/a/@href').extract()[i]))
            item['question_link'] = response.urljoin(response.css('h2.ContentItem-title').xpath('./div/a/@href').extract()[i]).replace("'", '"')

            #answer
            item['answer_content'] = ''
            for p in response.css('div.RichContent-inner')[i].xpath('./span//text()').extract():
                item['answer_content'] += p.replace("'", '"')

            #time
            #print(response.css('div.ContentItem-time a span::text')[2*i+1].extract())
            item['answer_time'] = time_arr[i]

            #upvote
            item['upvote_num'] = 0
            try:
                #print(response.css('div.List-item div.AnswerItem')[i].css('div.ContentItem-meta div.AnswerItem-meta div.AnswerItem-extraInfo span.Voters button::text').extract()[0])
                item['upvote_num'] = response.css('div.List-item div.AnswerItem')[i].css('div.ContentItem-meta div.AnswerItem-meta div.AnswerItem-extraInfo span.Voters button::text').extract()[0].replace("'", '"')
            except IndexError: pass

            #comment
            #print(response.css('div.List-item div.AnswerItem')[i].css('div.RichContent div.ContentItem-actions button::text').extract()[1])
            item['comment_num'] = response.css('div.List-item div.AnswerItem')[i].css('div.RichContent div.ContentItem-actions button::text').extract()[1].replace("'", '"')
            items.append(item)
        return items
        
    def parse_posts(self, response):
        person_id = response.url.split('/')[4]
        items = []
        for i in range(20):
            try:
                item = ArticlesItem()
                item['person_id'] = person_id.replace("'", '"')
                #title
                #print(response.css('div.List-item div.ArticleItem')[i].css('h2.ContentItem-title a::text').extract())
                item['article_title'] = response.css('div.List-item div.ArticleItem')[i].css('h2.ContentItem-title a::text').extract()[0].replace("'", '"')

                #link
                #print(response.css('div.List-item div.ArticleItem')[i].css('h2.ContentItem-title a::attr(href)').extract())
                item['article_link'] = response.css('div.List-item div.ArticleItem')[i].css('h2.ContentItem-title a::attr(href)').extract()[0].replace("'", '"')

                #article
                item['article_content'] = ''
                for a in response.css('div.RichContent-inner')[i].xpath('./span//text()').extract():
                    item['article_content'] += a.replace("'", '"')

                #upvote
                item['upvote_num'] = 0
                try:
                    #response.css('div.List-item div.ArticleItem')[i].css('div.ContentItem-meta div span.Votes button::text').extract()
                    item['upvote_num'] = response.css('div.List-item div.ArticleItem')[i].css('div.ContentItem-meta div span.Voters button::text').extract()[0].replace("'", '"')
                except IndexError: pass

                #comment
                item['comment_num'] = response.css('div.List-item div.ArticleItem')[i].css('div.RichContent div.ContentItem-actions button::text').extract()[1].replace("'", '"')

                #article_id
                item['article_id'] = item['article_link'].split('/')[-1]
                yield item
                items.append(item)
                url = 'https://zhuanlan.zhihu.com/api/posts/%s/comments?limit=100&offset=0' % item['article_link'].split('/')[-1]
                yield scrapy.Request(url, callback= self.parse_comments)
            except IndexError: break
        #return items

    def parse_comments(self, response):
        data = json.loads(response.css('pre::text').extract()[0])
        article_id = response.url.split('/')[-2]
        items = []
        for i in range(100):
            try:
                item = ArticleCommentItem()
                item['article_id'] = article_id
                item['comment_person_name'] = data[i]['author']['name']
                item['comment_content'] = data[i]['content']
                item['comment_time'] = data[i]['createdTime']
                item['upvote_num'] = data[i]['likesCount']
                items.append(item)
            except IndexError: break
        return items
