from pprint import pprint
from parser import ParserQuery, Parser
from scanner import Scanner
import json

query = ParserQuery("sale", "Водный стадион", 1, min_price=3 * (10 ** 6),
                    max_price=20 * (10 ** 6), min_square=18, max_square=45)
parser = Parser(query, 1, False)
parser.start_parser()

output_file = "outputs/results_test.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(parser.data, f, ensure_ascii=False, indent=2)

scanner = Scanner(output_file, n_neighbours=5)
profit_apartments = scanner.scanner(visualize_data=True)
pprint(profit_apartments)
