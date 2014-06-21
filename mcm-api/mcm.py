from parser import MCMAPI, CardNotFound, ArticleNotFound
from optparse import OptionParser

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-c", "--card",
                      default="", help="Card name")

    parser.add_option("-e", "--expansion",
                      default="", help="Expansion name")

    parser.add_option("-m", "--multiple", action="store_true", help="multiple items allowed")

    parser.add_option("-r", "--reputation", default=2, help="Set reputation (0, 1, 2, 3)")
    (options, args) = parser.parse_args()

    api = MCMAPI()
    try:
        article = api.search_card(options.card, options.expansion,
                                  multiple=False, reputation=options.reputation)
    except CardNotFound:
        print("Could not find card: {}. Make sure you've typed name and expansion correctly.")
        exit(0)
    except ArticleNotFound:
        print("Could not find article: {}. Make sure the reputation is correct. Good Seller = 3, Very good seller = 2, Outstanding = 1, ")
        exit(0)

    print('Result for {}: {}'.format(options.card, article))
