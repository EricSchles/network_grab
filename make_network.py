# How to do sytleometry?
# step 1 feature mapping
# step 2 apply distance function
# step 3 establish cut-offs
from sklearn.feature_extraction import text
from sklearn.pipeline import Pipeline
from sklearn import metrics
from app import models
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import networkx as nx



#http://scikit-learn.org/stable/modules/feature_extraction.html#customizing-the-vectorizer-classes
class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


def generate_feature_engineering():
    feature_engineering = Pipeline([
        ('vect', CountVectorizer(tokenizer=LemmaTokenizer())),
        ('tfidf', TfidfTransformer()),]
    )

    corpus = [elem.body for elem in models.AdInfo.query.all()]
    feature_engineering.fit(corpus)
    return feature_engineering


def generate_graph():
    transformer = generate_feature_engineering()
    mapped_data = {}
    G = nx.Graph()
    for elem in models.AdInfo.query.all():
        G.add_node(elem.id)
        mapped_data[elem.id] = transformer.fit_transform(elem.body)
    for first_elem in models.AdInfo.query.all():
        for second_elem in models.AdInfo.query.all():
            if first_elem.id == second_elem.id:
                continue
            similarity = metrics.jaccard_similarity_score(
                mapped_data[first_elem.id],
                mapped_data[second_elem.id]
            )
            if similarity > 0.7:
                G.add_edge(first_elem.id, second_elem.id)
    return nx.connected_component_subgraphs(G)


