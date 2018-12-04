import pickle
from hopfieldnet.net import HopfieldNetwork
from hopfieldnet.trainers import hebbian_training

# get ze data
with open('vector_dict.pickle', 'rb') as fi:
    data = pickle.load(fi)

input_patterns = [data[cat]['category_vector'] for cat in data.keys()]

# initialize the network
network = HopfieldNetwork(1200)
# train the network
hebbian_training(network, input_patterns)
