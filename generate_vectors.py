import gensim
import pickle
from nltk.corpus import wordnet as wn
import numpy as np

# Load Word2Bits, 1 Bit / 1200 dims / top 400k vocab
model = gensim.models.KeyedVectors.load_word2vec_format('./models/w2b.vec', binary=False)

categories = [('animal', 'animal.n.01'),
              ('machine', 'machine.n.01'),
              ('person', 'person.n.01'),
              ('game', 'game.n.01'),
              ('fruit', 'fruit.n.01'),
              ('vegetable', 'vegetable.n.01'),
              ('clothing', 'clothing.n.01')]

'''
For a given synset, pick up all hyponyms to root
'''
def get_all_hyponyms(synset):
    hyp = lambda s:s.hyponyms()
    all_hyponyms = list(synset.closure(hyp))
    return all_hyponyms

'''
Extract the unique set of lemma names from a list
of hyponyms, but only if the lemma name's primary
sense is that of the hyponym.
'''
def all_lemma_names(hyponyms):
    all_names = []
    for synset in hyponyms:
        for name in synset.lemma_names():
            if synset == wn.synsets(name)[0]:
                all_names.append(name)
    return list(set(all_names))

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
For each category given, collect all of its hyponyms,
vectorize them and place them into a dict.
'''
def main():
    vector_dict = {}
    for category in categories:
        cat_name, cat_wordnet = category
        syn = wn.synset(cat_wordnet)
        all_hyponyms = get_all_hyponyms(syn)
        all_lemmas = all_lemma_names(all_hyponyms)
        cat_vector = vectorize_one(cat_name)
        vectors = vectorize_all(all_lemmas)
        vector_dict[cat_name] = {'hyponym_vectors': vectors,
                                'category_vector': cat_vector}

    with open('vector_dict.pickle', 'wb') as fi:
        pickle.dump(vector_dict, fi)