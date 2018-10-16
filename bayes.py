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

def get_probability(nodes, expression):
    value = 1
    #print("------------\nExpression = ", expression)
    for item in expression:
        # Get node
        node = nodes[item[1:]]
        # Save the value of the node to add it to the beginning of the expression later
        main = copy.deepcopy(item)
        formated_p = []

        # Delete unnecesary values and format the expression:
        for parent in node['parents']:
            for element in expression:
                if(parent == element[1:]):
                    formated_p.append(element)


        # Add the main value to the beginning of the expression
        formated_p = [main] + formated_p
        #print("formated_p =", formated_p)

        # Search for the probability in cpt and get the value
        for probability in node['probabilities']:
            if(probability[0:-1] == formated_p):
                value = value * probability[-1]
                #print("Value = ", probability[-1])
    #print("value =", value)
    return value

def get_ancestors(query, nodes, ancestors, fixed):
    if(len(fixed) == 0):
        for element in query:
            fixed.append(element[1:])

    if(len(query) == 0):
        return ancestors
    else:
        parents = copy.deepcopy(nodes[query[0][1:]]['parents'])
        for parent in parents:
            if (parent not in ancestors and parent not in fixed):
                 ancestors.append(parent)
        print("Ancestors =", ancestors)
        return get_ancestors(query[1:], nodes, ancestors, fixed)

def probability_algorithm(query, nodes):

    # Get ancestors of the first node in the query
    print("QUERY = ", query)
    ancestors_numerator = get_ancestors(query[0], nodes, [], [])

    #print("Acestors numerator = ", ancestors_numerator)
    # Enumerate the ancestors
    enumerate_numerator = all_combinations(ancestors_numerator)

    numerator = 0
    for item in enumerate_numerator:
        item = query[0] + item
        numerator += get_probability(nodes, item)

    if(len(query[1]) > 0):
        ancestors_denominator = get_ancestors(query[1], nodes, [], [])
        enumerate_denominator = all_combinations(ancestors_denominator)

        denominator = 0
        for item in enumerate_denominator:
            item = query[1] + item
            denominator += get_probability(nodes, item)

        answer = numerator/denominator
    else:
        answer = numerator

    #print("Answer = ", answer)
    return answer

def all_combinations(probabilitesArray):
    num_combinations = 2 ** len(probabilitesArray) #exponent
    combinations=[]
    for j in range (0,num_combinations):
        combinations.append(copy.deepcopy(probabilitesArray))
    half_true_half_false(probabilitesArray, 0, int(num_combinations/2), combinations, '+', 0)
    half_true_half_false(probabilitesArray, int(num_combinations/2), num_combinations, combinations, '-', 0)
    return combinations
    #print(combinations)

def half_true_half_false(probabilitesArray,  inicio, fin, combinations, sign, i):
    if( i<len(probabilitesArray) ):
        letter = copy.deepcopy(probabilitesArray[i])
        for j in range (inicio,fin):
            combinations[j][i]= sign+letter
        half_true_half_false(probabilitesArray, inicio, inicio+int((fin-inicio)/2), combinations, '+', i+1)
        half_true_half_false(probabilitesArray, inicio+int((fin-inicio)/2), fin, combinations, '-', i+1)

def main():
    file_input = fileinput.input()

    # Nodes are formated in the function format_nodes()
    nodes = format_nodes(file_input.readline())

    # Probabilities -----------------------------------------------------------------------------
    num_prob = int(file_input.readline())
    probabilities = []
    for i in range (0,num_prob):
        line = file_input.readline().replace("\n", "")
        add_probability(nodes, line)
    # Calculate the rest of the table
    add_additional_probabilities(nodes)


    # Saving parents -----------------------------------------------------------------------------
    for node in nodes:
        parents = nodes[node]['probabilities'][0][1:len(nodes[node]['probabilities'][0])-1]
        for i in range(0,len(parents)):
            parents[i] = parents[i][1:]
        nodes[node]['parents'] = parents
    print("\n")
    pp.pprint(nodes)

    # Queries -------------------------------------------------------------------------------------
    num_que = int(file_input.readline())
    queries = []
    for i in range(0, num_que):
        line = file_input.readline().replace("\n", "")
        if('|' in line):
            condition = [line.split('|')[1]]
        else:
            condition = []
        query = [line.replace('|',',').split(',') , condition]
        queries.append(query)


    answers = []
    # Algorithm -----------------------------------------------------------------------------------
    for query in queries:
        answers.append(probability_algorithm(query, nodes))

    for answer in answers:
        print(answer)


if __name__ == "__main__":
    main()
