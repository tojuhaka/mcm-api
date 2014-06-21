from lxml import etree
import urllib3
import urllib
import configparser
import os


class CardNotFound(Exception):
    pass


class ArticleNotFound(Exception):
    pass


def _get_text(node):
    try:
        return node[0].text
    except IndexError:
        return ""


class MCMParser:
    @staticmethod
    def parse_cards(tree):
        result = []
        for pr in tree.findall('product'):
            result.append({
                'name': _get_text(pr.xpath('name/productName')),
                'id': _get_text(pr.xpath('idProduct')),
                'metaid': _get_text(pr.xpath('idMetaproduct')),
                'expansion': _get_text(pr.xpath('expansion')),
                'sell': _get_text(pr.xpath('priceGuide/SELL')),
                'low': _get_text(pr.xpath('priceGuide/LOW')),
                'avg': _get_text(pr.xpath('priceGuide/AVG')),
                'img': _get_text(pr.xpath('image')),
            })
        return result

    @staticmethod
    def parse_articles(tree, reputation, condition):
        result = []
        for pr in tree.xpath('article[condition="{}" and \
                             seller[reputation<={}]]'.format(condition,
                                                             reputation)):
            if pr.xpath('isAltered/text()="false"') and \
                    pr.xpath('isSigned/text()="false"') and \
                    pr.xpath('isFoil/text()="false"') and \
                    pr.xpath('isPlayset/text()="false"') and \
                    pr.xpath('language/idLanguage/text()="1"'):

                    result.append({
                        'id': _get_text(pr.xpath('idProduct')),
                        'price': _get_text(pr.xpath('price'))
                    })
        return result


class MCMAPI:
    _config = configparser.ConfigParser()

    def __init__(self):
        self._load_config()
        self.http = urllib3.PoolManager()

    def _load_config(self):
        try:
            self._config.read(['config.cfg', os.path.expanduser('~/.mkm.cfg')])
        except KeyError:
            print('Configuration file could not be found. Check readme.')
        self.domain = self._config['MKM']['domain']
        self.user = self._config['MKM']['user']
        self.apikey = self._config['MKM']['apikey']
        self.condition = self._config['MKM']['condition']
        self.reputation = self._config['MKM'].get('reputation', 2)
        self.multi = self._config['MKM'].get('multiple', False)

    def _get_card_xml(self, query):
        url = urllib.parse.quote("/{}/{}/products/{}/1/1/true".format(self.user, self.apikey, query))
        response = self.http.request('GET', "{}{}".format(self.domain, url))
        tree = etree.fromstring(response.data)
        return tree

    def _get_article_xml(self, product_id):
        url = "/{}/{}/articles/{}".format(self.user,
                                          self.apikey, product_id)
        response = self.http.request('GET', "{}{}".format(self.domain, url))
        tree = etree.fromstring(response.data)
        return tree

    def get_card_type(self, query, expansion):
        tree = self._get_card_xml(query)
        cards = MCMParser.parse_cards(tree)

        try:
            return next(filter(
                lambda card: card['expansion'].lower() == expansion.lower(),
                cards))
        except StopIteration:
            raise CardNotFound("Card not found: {}".format(query))

    def get_article(self, product_id):
        tree = self._get_article_xml(product_id)
        articles = MCMParser.parse_articles(tree,
                                            self.reputation, self.condition)

        if self.multi:
            return articles
        else:
            try:
                return articles[0]
            except IndexError:
                raise ArticleNotFound("Article not found: {}".format(product_id))

    def search_card(self, query, expansion, **kwargs):
        self.condition = kwargs.setdefault('condition', 'EX')
        self.reputation = kwargs.setdefault('reputation', 2)
        self.multi = kwargs.setdefault('multiple', False)

        card = self.get_card_type(query, expansion)
        result = self.get_article(card['id'])
        self._load_config()
        return result

    def _format_mtgsuomi(self, name, price, expansion, count):
        return "{}x [card]{}[/card] ({}) {}e\n".format(count, name.title(),
                                                       expansion, price)

    def generate_file(self, input, output, **kwargs):
        input_file = open(input, 'r')
        output_file = open(output, 'w')
        for line in input_file.readlines():
            name, expansion, count = line.split('|')
            count = count.strip()
            result = self.search_card(name, expansion, **kwargs)
            print("{}: {}".format(name.title(), result['price']))
            output_file.write(self._format_mtgsuomi(name,
                                                    result['price'],
                                                    expansion,
                                                    count))

        input_file.close()
        output_file.close()
