import scrapy

class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    start_urls = [
            'https://www.zhihu.com/people/mario-super-34/activities'
                ]


    def start_requests(self):
        people_id = ['excited-vczh']
        requests = []
        for p in people_id:
            '''
            requests.append(scrapy.Request(url='https://www.zhihu.com/people/%s/activities' % p, callback = self.parse_activities))
            for i in range(1, 6):
                requests.append(scrapy.Request(url='https://www.zhihu.com/people/%s/following?page=%s' %(p, i), callback = self.parse_follow))
            for i in range(1, 6):
                requests.append(scrapy.Request(url='https://www.zhihu.com/people/%s/followers?page=%s' %(p, i), callback = self.parse_follow))
            '''
            #for i in range(1, 26):
            for i in range(1, 2):
                requests.append(scrapy.Request(url='https://www.zhihu.com/people/%s/answers?page=%s' %(p, i), callback = self.parse_answer))
        return requests

    def parse_activities(self, response):
        print('昵称：%s' % (response.css('span.ProfileHeader-name::text')[0].extract()))
        print('关注了：%s' % (response.css('div.NumberBoard-value::text')[0].extract()))
        print('关注者：%s' % (response.css('div.NumberBoard-value::text')[1].extract()))
        print('回答数：%s' % (response.css('span.Tabs-meta::text')[0].extract()))
        print('提问数：%s' % (response.css('span.Tabs-meta::text')[1].extract()))
        print('文章数：%s' % (response.css('span.Tabs-meta::text')[2].extract()))
        print('专栏数：%s' % (response.css('span.Tabs-meta::text')[3].extract()))

        for i in range(5):
            try:
                label = response.css('span.ProfileHeader-detailLabel::text')[i].extract()
                value = ''
                if label == '居住地':
                    for j in range(100):
                        try:
                            value = value + response.css('div.ProfileHeader-detailValue')[i].css('span::text')[j].extract() + ' '
                        except IndexError: break
                    print('%s %s' % (label, value))
                if label == '所在行业':
                    value = response.css('div.ProfileHeader-detailValue')[i].css('div.ProfileHeader-detailValue::text')[0].extract()
                    print('%s %s' % (label, value))
                if label == '职业经历' or label == '教育经历':
                    for j in range(100):
                        try:
                            value = value + response.css('div.ProfileHeader-detailValue')[i].css('div.ProfileHeader-field::text')[j].extract() + ' '
                        except IndexError: break
                    print('%s %s' % (label, value))
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
                    print('%s %s' % (label, value))
            except IndexError: break


    def parse_follow(self, response):
        for i in range(100):
            try:
                print(response.css('a.UserLink-link::text').extract()[i])
            except IndexError: break


    '''
    def parse_answer(self, response):
        #question text
        for i in range(20):
            print(response.css('div.List-item div.AnswerItem')[i].css('h2.ContentItem-title').xpath('./div/a//text()').extract()[0])

        #question url
        url_list = response.css('h2.ContentItem-title').xpath('./div/a/@href').extract()
        for u in url_list:
           print(response.urljoin(u))

        #answer
        for i in range(20):
            for p in response.css('div.RichContent-inner')[i].xpath('./span//text()').extract():
                print(p)


        #time
        for i in range(20):
            print(response.css('div.ContentItem-time a span::text')[2*i+1].extract())

        #upvote
        for i in range(20):
            print(response.css('div.List-item div.AnswerItem')[i].css('div.ContentItem-meta div.AnswerItem-meta div.AnswerItem-extraInfo span.Voters button::text').extract())

        #comment
        for i in range(20):
            print(response.css('div.List-item div.AnswerItem')[i].css('div.RichContent div.ContentItem-actions button::text').extract()[1])
    '''

        
    def parse_answer(self, response):
        for i in range(20):
            #question text
            print(response.css('div.List-item div.AnswerItem')[i].css('h2.ContentItem-title').xpath('./div/a//text()').extract()[0])

            #question url
            print(response.urljoin(response.css('h2.ContentItem-title').xpath('./div/a/@href').extract()[i]))

            #answer
            for p in response.css('div.RichContent-inner')[i].xpath('./span//text()').extract():
                print(p)


            #time
            print(response.css('div.ContentItem-time a span::text')[2*i+1].extract())

            #upvote
            print(response.css('div.List-item div.AnswerItem')[i].css('div.ContentItem-meta div.AnswerItem-meta div.AnswerItem-extraInfo span.Voters button::text').extract()[0])

            #comment
            print(response.css('div.List-item div.AnswerItem')[i].css('div.RichContent div.ContentItem-actions button::text').extract()[1])

        
