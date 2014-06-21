from parser import MCMAPI, CardNotFound, ArticleNotFound
from optparse import OptionParser
import sys

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-c", "--card",
                      default="", help="Card name")

    parser.add_option("-e", "--expansion",
                      default="", help="Expansion name")

    parser.add_option("-m", "--multiple", action="store_true", help="Instead of returning first card, return all of them")

    parser.add_option("-r", "--reputation", default=2, help="Set reputation (1 = outstanding seller, 2 = very good seller, 3 = good seller)")
    parser.add_option("-i", "--input", help="Input file containing list of cards name|expansion|count")
    parser.add_option("-o", "--output", help="Output file which is generated from input file")
    parser.add_option("-n", "--condition", default="EX", help="Card Condition: NM, EX, GD, LP")
    (options, args) = parser.parse_args()

    if not len(sys.argv) > 1:
        print(parser.format_help())
        exit(0)

    api = MCMAPI()

    if options.input and options.output:
        api.generate_file(options.input, options.output, multiple=options.multiple, reputation=options.reputation, condition=options.condition)
        exit(0)

    try:
        article = api.search_card(options.card, options.expansion,
                                  multiple=options.multiple, reputation=options.reputation, condition=options.condition)
    except CardNotFound:
        print("Could not find card: {}. Make sure you've typed name and expansion correctly.")
        exit(0)
    except ArticleNotFound:
        print("Could not find article: {}. Make sure the reputation or condition is correct.")
        exit(0)

    print('Result for {}: {}'.format(options.card, article))
