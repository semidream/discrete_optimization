from functools import reduce
from pyscipopt import Model
import time
from collections import namedtuple

Item = namedtuple("Item", ['index', 'value', 'weight'])

def opt_model(item_count, capacity, items):
    record_time = time.time()
    model = Model()
    x_list = []
    for i in range(item_count):
        x_i = model.addVar('x_{}'.format(i), vtype="BINARY")
        x_list.append(x_i)

    print("After var init, used seconds: {}".format(time.time() - record_time))
    model.setObjective(coeffs=reduce(lambda x, y: x+y, [x_i*items[i][1] for i, x_i in enumerate(x_list)], 0), sense='maximize')
    print("before con add, used seconds: {}".format(time.time() - record_time))
    for i in range(item_count):
        model.addCons(cons=reduce(lambda x, y: x+y, [x_i*items[i][2] for i, x_i in enumerate(x_list)], 0) <= capacity)

    print("Start to optimize the problem. Build mode used seconds: {}".format(time.time() - record_time))
    model.optimize()
    res = [int(model.getVal(x_i)) for x_i in x_list]
    is_opt = int((model.getStatus() == 'optimal'))
    print("The obj is: {}".format(model.getObjVal()))
    return res, is_opt


def test_opt_model(file_location=None):
    if file_location is not None:
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
            # parse the input
        lines = input_data.split('\n')
        firstLine = lines[0].split()
        item_count = int(firstLine[0])
        capacity = int(firstLine[1])

        items = []

        for i in range(1, item_count+1):
            line = lines[i]
            parts = line.split()
            items.append(Item(i-1, int(parts[0]), int(parts[1])))
    else:
        item_count, capacity = 4, 11
        items = [(0, 8, 4), (1, 10, 5), (2, 15, 8), (3, 4, 3)]
    res, _ = opt_model(item_count, capacity, items)
    return res

if __name__ == '__main__':
    print(test_opt_model('./data/ks_19_0'))
