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
    # Get node

    node = nodes[expression[0][1:]]

    # An array to save que items in the same order as cpt
    formated_p = [expression[0]]

    # Delete unnecesary values and format:
    for i in range(0, len(node['parents'])):
        for j in range(1, len(expression)):
            if(node['parents'][i] == expression[j][1:]):
                formated_p.append(expression[j])

    # Search for the probability in cpt and get the value
    for i in range(0,len(node['probabilities'])):
        if(node['probabilities'][i][:-1] == formated_p):
            value = node['probabilities'][i][-1]

    return value

def enumerate():
    return [['+Rain','+Sprinkler'], ['+Rain','-Sprinkler'], ['-Rain', '+Sprinkler'], ['-Rain', '-Sprinkler']]

def probability_algorithm(query, nodes):
    # Enumerate the query

    # For each enumerated probability, get the rest of the components:
        # Example: Enumerated = ['+GrassWet', '+Rain', '-Sprinkler']  Missing components: ['+Rain', '-Sprinkler', '+GrassWet'] and ['-Sprinkler', '+GrassWet', '+Rain']

    # The content of the query expanded would be:
        #[[['+GrassWet', '+Rain', '-Sprinkler'],['+Rain', '-Sprinkler', '+GrassWet'],['-Sprinkler', '+GrassWet', '+Rain']], [ Other arrays of queries], [Arrays of queries]]
    expanded_query = [[['+GrassWet', '+Rain', '-Sprinkler'],['+Rain', '-Sprinkler', '+GrassWet'],['-Sprinkler', '+GrassWet', '+Rain']], [['+GrassWet', '-Rain', '-Sprinkler'],['-Rain', '-Sprinkler', '+GrassWet'],['-Sprinkler', '+GrassWet', '-Rain']]]
    pp.pprint(expanded_query)
    value = 1
    answer = 0
    for i in range(0, len(expanded_query)):
        for j in range(0,len(expanded_query[i])):
            value = value * get_probability(nodes, expanded_query[i][j])
            print("Value = ", value)
        answer += value
        print("Answer = ", answer)

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

def rotate_array(combinations):
    expanded = []
    for combination in combinations:
        aux = []
        for j in range (0, len(combination)):
            aux.append(combination)
        for i in  range (0, len(aux)):
            new_array = []
            for element in  aux[i]:
                query = element
                aux[i].remove(query)
                aux[i].insert(0,query)
                new_array.append(copy.deepcopy(aux[i]))
        expanded.append(copy.deepcopy(new_array))
    #print(expanded)

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
        queries.append(line.replace('|',' ').replace(',',' ').replace('=',' ').split())


    answers = []
    # Algorithm -----------------------------------------------------------------------------------
    #for query in queries:
        #answers.append(probability_algorithm(query, nodes))
    answers.append(probability_algorithm(1, nodes))
    print("ANSWERS =", answers)

    #merge conflicts
    #queries.append(line.split("="))
    #calculate the rest of the table
    combinations = all_combinations(["S", "M", "T"])
    rotate_array(combinations)

if __name__ == "__main__":
    main()
