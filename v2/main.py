__author__ = 'mark'

from app.v2.handler.handler import ApiRequestHandler
from lxml import html
from google.appengine.api import urlfetch
import time

class Parser(ApiRequestHandler):
    reviews = {}

    def get(self):
        url = self.request.get('url').strip()
        self.followPagination(url)

    def followPagination(self, url):
        try:
            self.log.info('Getting url {}...'.format(url))
            res = urlfetch.fetch(url)
            if res.status_code == 200:
                parsed = html.fromstring(res.content)
                reviews_divs = parsed.find_class('review--with-sidebar')
                for review_div in reviews_divs:
                    review_id = review_div.get('data-review-id')
                    if review_id is not None:
                        user = {}
                        author = review_div.find('meta')
                        if author.get('itemprop') == 'author':
                            user['name'] = author.get('content')

                        image_url = review_div.find_class('photo-box-img')[0].get('src')
                        if image_url is not None:
                            user['image_url'] = image_url

                        user_id = review_div.find_class('manage-following-add')[0].get('rel')
                        if user_id is not None:
                            user['id'] = user_id

                        rating = review_div.find_class('rating-very-large')[0].find('meta')
                        if rating.get('itemprop') == 'ratingValue':
                            rating = int(float(rating.get('content')))

                        date = review_div.find_class('rating-qualifier')[0].find('meta')
                        if date.get('itemprop') == 'datePublished':
                            date = date.get('content')

                        excerpt = review_div.find_class('review-content')[0].find('p')
                        if excerpt.get('itemprop') == 'description':
                            excerpt = excerpt.text_content()

                        self.reviews[review_id] = {
                            'user': user,
                            'rating': rating,
                            'excerpt': excerpt,
                            'time_created': time.mktime(time.strptime(date, "%Y-%m-%d")),
                            'id': review_id
                        }

                self.log.info('Got url {}'.format(url))
                next_page_url = parsed.find_class('page-option prev-next next')
                if next_page_url is not None and len(next_page_url):
                    next_page_url = next_page_url[0].get('href')
                    self.followPagination(next_page_url)
                else:
                    return self.render_api_json(obj=self.reviews.values())

        except urlfetch.Error, e:
            return self.render_api_json(obj={'status': 'failed', 'message': 'Sorry, i cant get this url {}, my error is {}: {}'.format(url, urlfetch.Error, e)})
