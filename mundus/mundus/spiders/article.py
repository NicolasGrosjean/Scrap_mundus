import scrapy

MAX_PAGE = 5


def get_date(elem: str):
    return elem.replace('\t', '').replace('\n', '').split(': ')[1]


def get_view_nb(elem: str):
    return elem.replace('\t', '').replace('\n', '').split(' affichages')[0]


class MundusArticleSpider(scrapy.Spider):
    name = "mundus_article"
    start_urls = [
        'https://www.mundusbellicus.fr/'
    ]
    page_nb = 1

    def parse(self, response):
        articles = response.xpath('.//ul[@class="conversation-list article-list list-container stream-view stream-view-full-width activity-view h-clearfix"]')
        urls = articles.xpath('.//h2//a[@class="b-post__title js-post-title starter"]//@href').extract()
        titles = articles.xpath('.//h2//a[@class="b-post__title js-post-title starter"]//text()').extract()
        meta = articles.xpath('.//ul[@class="b-post__article-meta h-margin-top-xs h-margin-bottom-l"]')
        for i in range(len(meta)):
            author = meta[i].xpath('.//li//a//text()').extract_first()
            date = get_date(meta[i].xpath('.//li')[1].xpath('.//text()').extract_first())
            try:
                views = get_view_nb(meta[i].xpath('.//li')[2].xpath('.//text()').extract_first())
            except IndexError:
                views = None
            yield {'title' : titles[i], 'url' : urls[i], 'author': author, 'date': date, 'views': views}

        if self.page_nb < MAX_PAGE:
            self.page_nb += 1
            yield scrapy.Request(f'{self.start_urls[0]}/page{self.page_nb}', callback=self.parse)
