import gensim
import pickle
import random
import numpy as np
from data.data import categories

# Load Word2Bits, 1 Bit / 1200 dims / top 400k vocab
model = gensim.models.KeyedVectors.load_word2vec_format('./models/w2b.vec', binary=False)

'''
Vectorize a lemma name, if it's in the vocab
'''
def vectorize_one(lemma_name):
    try:
        vec = model.get_vector(lemma_name)
        return vec * 3 # multiply so vals are {-1, 1}
    except KeyError:
        return np.array([])

'''
Vectorize a list of lemma names
'''
def vectorize_all(lemma_names):
    vectors = {}
    for name in lemma_names:
        vec = vectorize_one(name)
        if vec.any():
            vectors[name] = vec
    return vectors

'''
For each dimension, find the most common bit,
or choose randomly if the sum along that dimension is 0.
'''
def calculate_average(vectors):
    combo = np.array(vectors)
    summed = np.sum(combo, axis=0)
    summed[summed<0] = -1.
    summed[summed>0] = 1.
    summed[summed==0] = random.choice([-1., 1.])
    return summed

'''
For each category given, collect all of its hyponyms,
vectorize them and place them into a dict.
'''
def main():
    vector_dict = {}
    for category, data in categories.items():
        examples = data['examples']
        cat_vector = vectorize_one(category)
        low_vec = vectorize_one(data['low_freq'])
        high_vec = vectorize_one(data['high_freq'])
        vectors = vectorize_all(examples)
        average_vec = calculate_average(list(vectors.values()))
        vector_dict[category] = {'hyponym_vectors': vectors,
                                'category_vector': cat_vector,
                                'average_vector': average_vec,
                                'high_vector': high_vec,
                                'low_vector': low_vec}

    with open('./data/vector_dict.pickle', 'wb') as fi:
        pickle.dump(vector_dict, fi)