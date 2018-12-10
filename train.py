import pickle
import numpy as np
from hopfieldnet.net import HopfieldNetwork
from hopfieldnet.trainers import hebbian_training
from neupy import algorithms
from collections import Counter
from random import shuffle
import distance

with open('vector_dict.pickle', 'rb') as fi:
    data = pickle.load(fi)

data = {key:val for key, val in data.items() if key in ['animal', 'fruit', 'clothing', 'vegetable']}

mapping = {idx:cat_name for (idx, cat_name) in enumerate(list(data.keys()))}

'''
For a given network output, calculate the hamming distance
between that vector and those of the input patterns to determine
the nearest pattern, and output that categories name and id
'''
def find_closest(output, input_patterns):
    distances = []
    for pattern in input_patterns:
        ham_dist = distance.hamming(output, pattern)
        distances.append(ham_dist)
    val, idx = min((val, idx) for (idx, val) in enumerate(distances))
    return idx

def make_confusion_matrix(results_df):
    vector_types = results_df['vector_type'].unique()
    results = {v_type : {'y':[], 'y_pred':[]} for v_type in vector_types}
    for i, row in results_df.iterrows():
        v_type = row['vector_type']
        category = row['category']
        num_vecs = row['num_vecs']
        mistakes = row['mistakes']
        results[v_type]['y'] += [category] * num_vecs
        total_num_mistakes = 0
        for mis_category, num in mistakes.items():
            total_num_mistakes += num
            results[v_type]['y_pred'] += [mis_category] * num
        results[v_type]['y_pred'] += [category] * (num_vecs - total_num_mistakes)
    return results


'''
Train the network on the category input patterns, then flip a number
of random bits from each pattern and determine whether the network
converges to the correct basin.
'''
def train_and_flip(data, network, num_bits):
    input_patterns = [data[cat]['category_vector'] for cat in data.keys()]

    correct = 0
    for i, pattern in enumerate(input_patterns):
        indices = list(range(len(pattern)))
        shuffle(indices)
        for x in range(num_bits):
            bit_to_flip = indices[x]
            pattern[bit_to_flip] *= -1
        output = network.run(pattern)
        idx = find_closest(output, input_patterns)
        if i == idx: correct += 1

    return correct
'''
Train the network on a set of input patterns corresponding to categories
of interest, then run the network with items in those categories and
return information about the success rate.
'''
def train_and_evaluate(data, vector_type):
    input_patterns = [data[cat][vector_type] for cat in data.keys()]
    # initialize the network
    network = HopfieldNetwork(1200)
    # train the network
    hebbian_training(network, input_patterns)

    results = []
    for i, cat in enumerate(data.keys()):
        cat_data = data[cat]
        hyp_vecs = cat_data['hyponym_vectors'].values()
        num_vecs = len(hyp_vecs)
        correct = 0
        mistakes = []
        for pattern in hyp_vecs:
            output = network.run(pattern)
            idx = find_closest(output, input_patterns)
            if i == idx: correct += 1
            else: mistakes.append(mapping[idx])
        mistakes = dict(Counter(mistakes))
        results.append({'correct': correct, 'num_vecs': num_vecs,
            'mistakes': mistakes, 'category': cat, 'vector_type': vector_type})
    return results

'''
Test how the choice of input pattern affects performance.
category_vector: vector of the category (e.g. 'animal')
high_vector: high-frequency vector of the category (e.g. 'dog')
low_vector: low-frequency vector of the category (e.g. 'armadilo')
'''
def run_vector_analysis():
    vector_types = ['category_vector', 'high_vector', 'low_vector', 'average_vector']
    results = []
    for v_type in vector_types:
        results += train_and_evaluate(data, v_type)
    return results

'''
Test how resiliant the network is to corrupted input
by flipping increasing number of bits from the training patterns.
'''
def run_flip_analysis(max_bits):
    input_patterns = [data[cat]['category_vector'] for cat in data.keys()]
    # initialize the network
    network = HopfieldNetwork(1200)
    # train the network
    hebbian_training(network, input_patterns)

    results = []
    for num_flip in range(max_bits):
        correct = train_and_flip(data, network, num_flip)
        results.append((num_flip, correct))
    return results
