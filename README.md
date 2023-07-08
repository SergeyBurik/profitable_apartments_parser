# profitable_apartments_parser

## How it works
This project includes `parser` module for collecting real estate data in Moscow region using `bs4` and `selenium`. <br>
Scanner uses `n-nearest-neighbors method` to find profitable apartments in given area.
First, for each apartment, sort neighbours by distance `d(x, y)`:
$$d(x,y) = \sqrt{(x_0-y_0)^2+(x_1-y_1)^2}$$
`x - given apartment coordinates` and `y - possible nearest neighbour coordinates` <br>
Then, sort apartments profitability by metric function:
$$M(x, y) = \frac{1}{n} \sum_{i=0}^n (y_i)  - x $$
`x - given apartment price` and `y - set of prices of neighboring houses` <br>
The larger the value of `M(x, y)`, the more profitable the apartment.

## Getting started
Python version > 3.7 <br>
Install requirements and run main.py
```bash
pip install -r requirements.txt
python main.py
```
## How to use
To parse data by query, use Parser class
```python
query = ParserQuery(
  "sale", "metro name", bedrooms=1,
  min_price=3 * (10 ** 6), max_price=20 * (10 ** 6),
  min_square=18, max_square=45
)
parser = Parser(query, pages=3)
parser.start_parser()
```
to save parsed data to json:
```python
output_file = "outputs/results_test.json"
with open(output_file, 'w', encoding='utf-8') as f:
	json.dump(parser.data, f, ensure_ascii=False, indent=2)
```
to run Scanner:
```python
scanner = Scanner(output_file, n_neighbours=5)
profit_apartments = scanner.scanner(visualize_data=True)
print(profit_apartments)
```

## Data visualization 
x-axis: longitude; y-axis:latitude <br>
Different colors show groups of neighbours <br>
Query: 1 bedroom apartments, n_neighbours=5, metro station: "Vodny stadion"
![d1](https://github.com/SergeyBurik/profitable_apartments_parser/assets/40773987/31fbf870-a699-4573-9239-8791ab919137)

