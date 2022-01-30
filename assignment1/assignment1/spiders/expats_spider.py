import scrapy

#create spider class
class PostsSpider(scrapy.Spider):
    name= "posts"
    start_urls= ["https://forum.singaporeexpats.com/viewforum.php?f=93"]


    #seed page is the first page of gaming forum 




    #dump records to MongoDB
    #check validity
    def parse(self,response):
        for topic in response.xpath("//*[contains(@class,'topic_read')]"):
            yield {
                'topic_title': topic.css('a.topictitle::text').get(),  #1.1 extract title of topic
                'no_replies': topic.css('dd.posts::text').get(),       #1.2 extract no. of replies
                'no_views': topic.css('dd.views::text').get() ,     #1.3 extract no. of views
            }
    
        for post_list in response.css('a.topictitle::attr(href)'):
            if post_list is not None:
                yield response.follow(post_list.get(), callback= self.parse_posts)     #2- extract posts in topic
        
    
        next_page = response.xpath('//li[@class="arrow next"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


    def parse_posts(self, response):
            for post in response.xpath("//*[contains(@id,'post_content')]"):
                yield{
                    'topic_title': response.xpath("//h2[@class='topic-title']/a/text()").get(),      #2.1 extract title of topic
                    'author':post.xpath(".//a[contains(@class,'username')]/text()").get(),         #2.2 extract author name
                    'post_content': post.css('div.content::text').getall()                              #2.3 extract post content
                }
                next_post= post.xpath('//li[@class="arrow next"]/a/@href').get()
                if next_post is not None:
                    yield  response.follow(next_post, 
                        self.parse_posts)

                
        
