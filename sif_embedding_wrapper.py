import pandas as pd
import numpy as np
import csv
import sys
sys.path.append("SIF/src")
import data_io
import SIF_embedding
import utils

MAX_WORDS = 300

def sentences2idx(texts, words):
  """
  Take in data, output array of word indices that can be fed into the algorithms.
  :param texts: List of texts
  :return: x1, m1. x1[i, :] is the word indices in sentence i, m1[i,:] is the mask for sentence i (0 means no word at the location)
  """
  seq = []
  for t in texts:
    # Doing some cleaning of the text
    stopwords = utils.get_stopwords()
    text = t.strip().strip('"')
    text_clean = utils.clean_text(text)
    s = [w for w in text_clean.split(" ") if w not in stopwords]
    s = s[0:MAX_WORDS]
    seq.append(data_io.getSeq(' '.join(s), words))
  x1, m1 = data_io.prepare_data(seq)
  return x1, m1

def getWordmapWord2Vec(wordfile):
  word_embedding_df = pd.read_table(wordfile, delim_whitespace=True, index_col=0, header=None, quoting=csv.QUOTE_NONE, skiprows=1)
  words = {}
  word_embedding = np.zeros(
    shape=(word_embedding_df.shape[0], word_embedding_df.shape[1]))
  n = 0
  for row in word_embedding_df.itertuples():
    words[row[0]] = n
    word_embedding[n] = row[1:]
    n += 1
  return (words, word_embedding)

def sentences2vecs(sentences, We, words, weight4ind):
  x, m = sentences2idx(sentences, words)
  w = data_io.seq2weight(x, m, weight4ind)
  return SIF_embedding.get_weighted_average(We, x, w)

def load_embeddings(wordfile, weightfile, weightpara=5e-4, word2vec=False):
  if word2vec:
    (words, We) = getWordmapWord2Vec(wordfile)
  else:
    (words, We) = data_io.getWordmap(wordfile)
  word2weight = data_io.getWordWeight(weightfile, weightpara)  # word2weight['str'] is the weight for the word 'str'
  weight4ind = data_io.getWeight(words, word2weight)  # weight4ind[i] is the weight for the i-th word
  return words, We, weight4ind