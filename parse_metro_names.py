def get_metro_names():
	f = open("files/metro.txt", encoding="utf-8")

	names = [l[:-1] for l in f.readlines() if len(l) > 1]
	names = sorted(set(names))

	result = dict()
	i = 1
	for name in names:
		idx = name.find("(")
		if idx != -1:
			name = name[:idx]
		result[name] = i
		i += 1
	return result
