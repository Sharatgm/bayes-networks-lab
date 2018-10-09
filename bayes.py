import fileinput
import time
import pprint

def format_nodes(line):
    # First the \n is removed and then the line is splited in the ","
    names = line.replace("\n","").split(",")

    # This will create an array of nodes
    nodes = []
    for i in range (0,len(names)):
        # Each node will be in the format {'name' = 'rain', 'probabilities' = [Array of the probabilities], 'parents' = [array of the parents] }
        nodes.append({'name': names[i], 'probabilities': [], 'parents': []})
    return nodes

def add_probability(nodes, line):
    # First it splits the line in the "=" [Description, value]
    prob = line.split("=")

    # Split the description in the |.
    #    Cases:
    #       If there is a condition ( | ):  [[Node, Condition], Value]
    #       If there is not a condition: [Description, Value]
    prob[0] = prob[0].split("|")
    if (len(prob[0]) > 1):
        # Si hubo condición

    else:
        # No hubo condición y es el nodo raíz



def main():
    # Read file
    file_input = fileinput.input()

    # Nodes are formated in the function format_nodes()
    nodes = format_nodes(file_input.readline())

    # Probabilities
    num_prob = int(file_input.readline())
    probabilities = []
    for i in range (0,num_prob):
        line = file_input.readline().replace("\n", "")
        probabilities.append(line.split("="))

    # Queries
    num_que = int(file_input.readline())
    queries = []
    for i in range(0, num_que):
        line = file_input.readline().replace("\n", "")
        queries.append(line.split("="))

    print("NODES = ", nodes)
    print("PROBABILITIES = ", probabilities)
    print("QUERIES = ", queries)


if __name__ == "__main__":
    main()
