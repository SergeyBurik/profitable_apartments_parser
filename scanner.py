import json
import matplotlib.pyplot as plt
from pprint import pprint
from random import uniform


class Scanner:
	def __init__(self, data_filename, n_neighbours):
		self.data_filename = data_filename
		self.n_neighbours = n_neighbours

	def scanner(self, visualize_data=False):
		f = open(self.data_filename, encoding="utf-8")
		content = f.read()
		data = json.loads(content)
		data = sorted(data, key=lambda x: x["coordinates"])

		avg_area_price = 0
		result = []
		differences = []
		for apartment in range(len(data)):
			avg_neigh_price = 0

			neighbours = self.find_neighbours(data[apartment], data)
			for n in neighbours:
				avg_neigh_price += n["price"]
			avg_neigh_price /= self.n_neighbours

			if data[apartment]["price"] < avg_neigh_price:
				# append apartment data and difference between average prices of neighbours and apartment price
				result.append([data[apartment], avg_neigh_price - data[apartment]["price"]])
			avg_area_price += data[apartment]["price"]
			differences.append([data[apartment], neighbours])
		avg_area_price /= len(data)

		for el in result:
			# append difference between average price in search area and apartment price (profitability)
			el.append(avg_area_price - el[0]["price"])

		# sort data by apartment profitability
		result = sorted(result, key=lambda x: x[1], reverse=True)

		if visualize_data:
			self.visualize_n_neighbours(differences)
		return result

	def find_neighbours(self, apartment, data):
		neighbours = []
		for el in data:
			distance = (apartment["coordinates"][0] - el["coordinates"][0]) ** 2 + \
			           (apartment["coordinates"][1] - el["coordinates"][1]) ** 2
			neighbours.append([el, distance ** 0.5])
		neighbours = sorted(neighbours, key=lambda x: x[1])
		return [el[0] for el in neighbours[:self.n_neighbours]]

	def find_neighbours_optimized(self, apartment, data):
		data = sorted(data, key=lambda x: ((apartment["coordinates"][0] - x["coordinates"][0]) ** 2 +
		                                   (apartment["coordinates"][1] - x["coordinates"][1]) ** 2) ** 0.5)

		neighbours = data[:self.n_neighbours]
		return neighbours

	@staticmethod
	def visualize_n_neighbours(differences):
		colors = ["b", "g", "r", "c", "m", "y", "k"]
		colors_i = 0
		for diff in differences:
			color = colors[colors_i % len(colors)]
			colors_i += 1

			el_coord = diff[0]["coordinates"]
			for i in range(len(diff[1])):
				diff_coord = diff[1][i]["coordinates"]

				# add small number to coordinates so that lines on plot do not overlap
				d = uniform(0.003, 0.005)
				plt.plot([el_coord[0] + d, diff_coord[0] + d], [el_coord[1] + d, diff_coord[1] + d], "-ro", color=color)
		plt.show()
