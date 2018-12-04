import pickle
from hopfieldnet.net import HopfieldNetwork
from hopfieldnet.trainers import hebbian_training
from scipy.spatial import distance

# get ze data
with open('vector_dict.pickle', 'rb') as fi:
    data = pickle.load(fi)

def find_closest(output, input_patterns):
    distances = []
    for pattern in input_patterns:
        euc_dist = distance.euclidean(output, pattern)
        distances.append(euc_dist)
    val, idx = min((val, idx) for (idx, val) in enumerate(distances))
    return idx

input_patterns = [data[cat]['category_vector'] for cat in data.keys()]

# initialize the network
network = HopfieldNetwork(1200)
# train the network
hebbian_training(network, input_patterns)

for i, pattern in enumerate(input_patterns):
    output = network.run(pattern)
    closest = find_closest(output, input_patterns)
    print(i, closest)