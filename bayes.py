import copy
import fileinput
import time
import pprint as pp

def format_nodes(line):
    # Create the nodes given their names
    names = line.replace("\n","").split(",")

    nodes = {}
    for i in range (0,len(names)):
        nodes[names[i]] = {'probabilities': [], 'parents': []}
    return nodes

def add_probability(nodes, line):
    # Add each probability to the CPT of each node
    prob = line.replace('|',' ').replace(',',' ').replace('=',' ').split()
    name = prob[0][1:]
    prob[len(prob)-1] = float( prob[len(prob)-1] )
    nodes[name]['probabilities'].append(prob)
    return nodes


def add_additional_probabilities(nodes):
    for node in nodes:
        probabilities = nodes[node]['probabilities']
        for probability in probabilities:
            actual_sign = probability[0][0]
            # decide which will be the next sign
            if(actual_sign == '+'):
                new_sign='-'
            elif(actual_sign == '-'):
                new_sign='+'
            #copy the probability
            new_probability = copy.deepcopy(probability)
            #replace the sign (keep the rest of the word)
            new_probability[0] = new_sign+probability[0][1:]
            #calculate the complement of the probability
            new_probability[len(new_probability)-1] = round(1-probability[len(new_probability)-1],2)
            # add the new probability only if it doesn't exist already
            if(new_probability not in probabilities):
                probabilities.append(new_probability)

def main():
    file_input = fileinput.input()

    # Nodes are formated in the function format_nodes()
    nodes = format_nodes(file_input.readline())

    # Probabilities
    num_prob = int(file_input.readline())
    probabilities = []
    for i in range (0,num_prob):
        line = file_input.readline().replace("\n", "")
        add_probability(nodes, line)
    # Saving parents
    for node in nodes:
        parents = nodes[node]['probabilities'][0][1:len(nodes[node]['probabilities'][0])-1]
        for i in range(0,len(parents)):
            parents[i] = parents[i][1:]
        nodes[node]['parents'] = parents
    print("\n")
    pp.pprint(nodes)
    # Test is a float
    # print(nodes['GrassWet']['probabilities'][0][3]+nodes['GrassWet']['probabilities'][1][3])
    # Queries
    num_que = int(file_input.readline())
    queries = []
    for i in range(0, num_que):
        line = file_input.readline().replace("\n", "")
        queries.append(line.split("="))
    #calculate the rest of the table
    add_additional_probabilities(nodes)
if __name__ == "__main__":
    main()
