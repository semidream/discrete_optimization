from functools import reduce
from pyscipopt import Model

def opt_model():
    item_count, capacity = 4,11
    items = [(8, 4), (10, 5), (15, 8), (4, 3)]
    model = Model()
    x_list = []
    for i in range(item_count):
        x_i = model.addVar('x_{}'.format(i), vtype="BINARY")
        x_list.append(x_i)

    model.setObjective(coeffs=reduce(lambda x, y: x+y, [x_i*items[i][0] for i, x_i in enumerate(x_list)], 0), sense='maximize')
    for i in range(item_count):
        model.addCons(cons=reduce(lambda x, y: x+y, [x_i*items[i][1] for i, x_i in enumerate(x_list)], 0) <= capacity)

    model.optimize()

    print(model.getVars())

if __name__ == '__main__':
    opt_model()