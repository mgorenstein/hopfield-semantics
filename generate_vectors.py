import gensim
import pickle
from nltk.corpus import wordnet as wn

# map between WN and DeConf keys
with open('sense_key_map.txt','r') as tsv:
    split = [line.strip().split('\t') for line in tsv]
    sense_map = {line[1]:line[0] for line in split}

# Load DeConf: https://pilehvar.github.io/deconf/
model = gensim.models.KeyedVectors.load_word2vec_format('sense-model.bin', binary=True)

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
Extract the unique set of lemma keys from a list
of hyponyms.
'''
def all_lemma_keys(hyponym_list):
    all_keys = []
    for synset in hyponym_list:
        all_keys += [lemma.key() for lemma in synset.lemmas()]
    return list(set(all_keys))

'''
Vectorize a lemma name by:
1. translating the lemma into its sense key
2. mapping the sense key into the DeConf sense_ID
3. getting the vector for the sense_ID
'''
def vectorize_one(lemma_key):
    try:
        sense_ID = sense_map[lemma_key]
        vec = model.get_vector(sense_ID)
        return vec
    except KeyError:
        return np.array([])

'''
Vectorize a list of lemma keys
'''
def vectorize_all(lemmas):
    vectors = {}
    for lemma in lemmas:
        vec = vectorize_one(lemma)
        if vec.any():
            vectors[lemma] = vec
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
        all_lemmas = all_lemma_keys(all_hyponyms)
        cat_vector = vectorize_one(syn.lemmas()[0].key())
        vectors = vectorize_all(all_lemmas)
        vector_dict[cat_name] = {'hyponym_vectors': vectors,
                                'category_vector': cat_vector}

    with open('vector_dict.pickle', 'wb') as fi:
        pickle.dump(vector_dict, fi)