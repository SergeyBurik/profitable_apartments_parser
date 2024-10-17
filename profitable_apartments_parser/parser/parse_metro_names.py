import os


def get_metro_names():
    f = open(os.path.join(os.getcwd(), "files/metro.txt"), encoding="utf-8")

    names = [l[:-1] for l in f.readlines()]
    names = sorted(set(names))

    result = dict()
    i = 1
    for name in names:
        idx = name.find("(")
        if idx != -1:
            name = name[:idx]
        result[name] = i
        i += 1
    # some metro ids may differ from source website
    result["Водный стадион"] = 29
    return result
