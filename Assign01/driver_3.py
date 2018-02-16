import numpy as np
import time
import sys

import resource
def max_mem():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
  
visited = set()
container = []
continer_set = set()
max_len = 0
node_expanded = 0
final_path = ""

BOARD_LIMIT = 3

class pkage(object):
    def __init__(self, dat, order_string):
        self.data = dat
        self.order_string = order_string

def decode_arg(arg_string):
    data = arg_string.split(",")
    data = np.array(data, dtype=np.int32).reshape(3,3)
    return data 

def encode(input_array):
    tmp_string = str(input_array.reshape(9).squeeze())[1:-1]
    return "".join(tmp_string.split(' '))

def decode(input_string):
    data = list(input_string)
    data = np.array(data, dtype=np.int32).reshape(3,3)
    return data 

def order_string_to_list():
    tmp_str = []
    for ele in list(final_path):
        if ele == '0':
            tmp_str.append("Up")
        elif ele == '1':
            tmp_str.append("Down")
        elif ele == '2':
            tmp_str.append("Left")
        else:
            tmp_str.append("Right")
    return tmp_str

def add_node_to_container(node):
    encoded_string = node.data
    if encoded_string not in visited and encoded_string not in continer_set:
        visited.add(encoded_string)
        continer_set.add(encoded_string)
        container.append(node)

def create_children_package_for_node(input_package):
    data = decode(input_package.data)
    zero_id_Y, zero_id_X = np.where(data==0)
    zero_id_Y = zero_id_Y[0]
    zero_id_X = zero_id_X[0]
    #print(zero_id_X, zero_id_Y)
    pkgs = [None, None, None, None]
    add_to_container = [False, False, False, False]

# is able to move up
    if zero_id_Y >= 1 and zero_id_Y < BOARD_LIMIT:
        tempd = data.copy()
        tempd[zero_id_Y][zero_id_X]=tempd[zero_id_Y-1][zero_id_X]
        tempd[zero_id_Y-1][zero_id_X]=0
        encoded_string = encode(tempd)
        pkgs[0] = pkage(encoded_string, input_package.order_string+'0')
        add_to_container[0] = True
# is able to move down
    if zero_id_Y >= 0 and zero_id_Y < BOARD_LIMIT-1:
        tempd = data.copy()
        tempd[zero_id_Y][zero_id_X]=tempd[zero_id_Y+1][zero_id_X]
        tempd[zero_id_Y+1][zero_id_X]=0
        encoded_string = encode(tempd)
        pkgs[1] = pkage(encoded_string, input_package.order_string+'1')
        add_to_container[1] = True
# is able to move left
    if zero_id_X >= 1 and zero_id_X < BOARD_LIMIT:
        tempd = data.copy()
        tempd[zero_id_Y][zero_id_X]=tempd[zero_id_Y][zero_id_X-1]
        tempd[zero_id_Y][zero_id_X-1]=0
        encoded_string = encode(tempd)
        pkgs[2] = pkage(encoded_string, input_package.order_string+'2')
        add_to_container[2] = True
# is able to move down
    if zero_id_X >= 0 and zero_id_X < BOARD_LIMIT-1:
        tempd = data.copy()
        tempd[zero_id_Y][zero_id_X]=tempd[zero_id_Y][zero_id_X+1]
        tempd[zero_id_Y][zero_id_X+1]=0
        encoded_string = encode(tempd)
        pkgs[3] = pkage(encoded_string, input_package.order_string+'3')
        add_to_container[3] = True

    if mode == 'bfs':
        for idx, itm in enumerate(add_to_container):
            if itm:
                add_node_to_container(pkgs[idx])
    elif mode == 'dfs':
        for idx, itm in enumerate(list(reversed(add_to_container))):
            if itm:
                r_pkgs = list(reversed(pkgs))
                add_node_to_container(r_pkgs[idx])
                #print("add {}".format(r_pkgs[idx].data))
    else:
# priority queue!!
        for idx, itm in enumerate(add_to_container):
            if itm:
                add_node_to_container(pkgs[idx])
    return

start_time = time.time()
mode = ""
inputdata = ""
try:
    mode = sys.argv[1]
    inputdata = sys.argv[2]
except:
    print("Usage: python3 {} [dfs/bfs] [9,8,7,6,5,4,3,2,1,0]".format(__file__))
    exit()

add_node_to_container(pkage(encode(decode_arg(inputdata)), ""))

while (len(container) != 0):
    node = None
    if mode == 'bfs':
        node = container.pop(0)
        #print("expand", node.data)
    elif mode == 'dfs':
        node = container.pop()
        #print("expand", node.data)
    else:
        node = container.pop()

    if len(node.order_string) > max_len:
        max_len = len(node.order_string)

    continer_set.remove(node.data)
    #print("executing: {}".format(node.order_string))
    if node.data == "012345678":
        final_path = node.order_string
        break
    create_children_package_for_node(node)
    node_expanded += 1

with open("output.txt", "w") as f:
    f.write("final_path: {}\n".format(order_string_to_list()))
    f.write("cost_of_path: {}\n".format(len(final_path)))
    f.write("nodes_expanded: {}\n".format(node_expanded))
    f.write("search_depth: {}\n".format(len(final_path)))
    f.write("max_search_depth: {}\n".format(max_len))
    f.write("running_time: {}\n".format((time.time()-start_time)))
    f.write("max_ram_usage: {}\n".format(max_mem()))

with open("output.txt", "r") as f:
    print(f.read())

