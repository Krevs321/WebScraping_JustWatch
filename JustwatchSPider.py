import scrapy
import json

class JustwatchSPider(scrapy.Spider):
    name = 'jwspider'
    start_urls = ['https://www.justwatch.com/uk/movies']

    def parse(self, response):
        for link in response.css('div.title-list-grid__item a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_movie)

    def parse_movie(self, response):
        for film in response.css('div.title-info.visible-xs.visible-sm'):
            genres = film.css('div.detail-infos__value span::text').getall()
            popravljeni = []
            for genre in genres:
                if genre != ', ':
                    popravljeni.append(genre.strip())
            try:
                yield {
                    'name': response.css('div.title-block__container div.title-block h1::text').get().strip(),
                    'leto': response.css('div.title-block__container div.title-block span::text').get().replace('(','').replace(')','').strip(),
                    'rating': film.css('div.jw-scoring-listing__rating a.jw-scoring-listing__rating--no-link::text').get().strip(),
                    'genres': popravljeni,
                    'cas_trajanja': film.css('div.detail-infos div.detail-infos__value::text').getall()[0],
                    'age_rating': film.css('div.detail-infos div.detail-infos__value::text').getall()[1],
                    'director': film.css('div.detail-infos__value a.title-credit-name::text').get().strip()
                }
            except:
                yield {
                    'name': response.css('div.title-block__container div.title-block h1::text').get().strip(),
                    'leto': response.css('div.title-block__container div.title-block span::text').get().replace('(','').replace(')', '').strip(),
                    'rating': film.css('div.jw-scoring-listing__rating a.jw-scoring-listing__rating--no-link::text').get().strip(),
                    'genres': popravljeni,
                    'director': 'NIMA GLAVNEGA DIREKTORJA'
                }