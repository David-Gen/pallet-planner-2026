import csv


def consolidate(filename):
    full_list = {}

    with open(filename, "r") as file:
        line = csv.reader(file)
        for product in line:
            if product[0] == "":
                continue
            elif product[0] not in full_list:
                full_list[product[0]] = product[1]
            else:
                quantity = int(full_list.get(product[0])) + int(product[1])
                full_list[product[0]] = quantity

    with open(filename, "w") as file:
        for key in full_list.keys():
            file.write("%s,%s\n" % (key, full_list[key]))
