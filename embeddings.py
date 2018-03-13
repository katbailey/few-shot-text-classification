import sys
sys.path.append("SIF/src")
import data_io
import SIF_embedding
import utils

EMBEDDING_DIM = 300
MAX_WORDS = 300

# vectorizer = emb.Vectorizer(glove_path, freq_path, 300)
# r = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)
#
# class TestConfig():
#   def __init__(self, config_dict):
#     self.config = config_dict
#   def get(self, key, dflt=None):
#     if not key in self.config:
#       return dflt
#     return self.config[key]
#
# data_dir = "/Users/katherine.bailey/DataSci/data/simile_accuracy"
# account_id = "kat-testing"
# config_dict = {"ACCOUNT_IDS": [account_id], "CACHE_BACKEND": "memory"}
# my_config = TestConfig(config_dict)
# mycache = cache.MemoryCacheStore(None)
# mystorage = storage.MemoryStore(config_dict)
# bm = emb.BatchManager(my_config, mycache, mystorage, vectorizer)
# cm = clsfr.ClassifierManager(mycache, mystorage, bm)
#
# def create_classifier(bm, cm, account_id, batch_id, categories):
#     batch_df = pd.read_csv("%s/%s.csv" % (data_dir, batch_id))
#     docs = batch_df.to_dict(orient="records")
#     docs = [{"doc_id": str(d["doc_id"]), "text": str(d["text"])} for d in docs]
#     bm.add_docs(account_id, batch_id, docs)
#     batch = bm.get(account_id, batch_id)
#     classifier = cm.create(account_id, batch, categories)
#     return classifier
#
# categories = ["autos", "baseball"]
# batch_id = "_".join(categories)
# classifier = create_classifier(bm, cm, account_id, batch_id, categories)
# truth_df = pd.read_csv("%s/%s_truth.csv" % (data_dir, batch_id))
# truth_dict = {str(rec["doc_id"]): rec["gt"] for rec in truth_df.to_dict(orient="records")}
# def get_accuracy_score(predictions, truth_dict):
#   scores = []
#   for k, v in predictions.items():
#     if v["category"] == truth_dict[k]:
#       scores.append(1)
#     else:
#       scores.append(0)
#   if len(scores) == 0:
#     return 0.0
#   return sum(scores) / float(len(scores))
#
#
# classifier.reset()
# for i, c in enumerate(categories):
#   classifier.classify(best_pair[c], c)
# predictions = classifier.get_predictions()
# best_acc = get_accuracy_score(predictions, truth_dict)
# best_acc

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
    print(s)
    seq.append(data_io.getSeq(' '.join(s), words))
  x1, m1 = data_io.prepare_data(seq)
  return x1, m1


def load_embeddings(wordfile, weightfile, weightpara=5e-4):
  # load word vectors
  (words, We) = data_io.getWordmap(wordfile)
  # load word weights
  word2weight = data_io.getWordWeight(weightfile, weightpara)  # word2weight['str'] is the weight for the word 'str'
  weight4ind = data_io.getWeight(words, word2weight)  # weight4ind[i] is the weight for the i-th word
  return words, We, weight4ind