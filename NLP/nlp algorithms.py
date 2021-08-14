from scipy import spatial
import advertools as adv
from sklearn.feature_extraction.text import TfidfVectorizer
from DatabaseHandlers.database_handler_orchestrator import DatabaseHandlerOrchestrator
from HebrewMorphologyEngine.morphology_engine import HebrewMorphologyEngine

hebrew_stoplist = adv.stopwords['hebrew']


class NLPProcessor:
    def __init__(self):
        self.terms = {}
        self.morphology_engine = HebrewMorphologyEngine()
        self.handler = DatabaseHandlerOrchestrator()
        self.id_to_text_dict = {}
        self.doc_idfs = {}
        self.full_texts_dict = {}
        self.tfidf_dict = {}
        self.id_to_tuple_dict = {}

    @classmethod
    def find_cosine_similarity(cls, doc_1, doc_2):
        return 1 - spatial.distance.cosine(doc_1, doc_2)

    def get_id_to_text_dict(self):
        rows_tuple_list = self.handler.get_all_rows()
        for row in rows_tuple_list:
            self.id_to_text_dict[str(row[0])] = row[3]
            self.id_to_tuple_dict[str(row[0])] = row
        return self.id_to_text_dict

    def return_texts(self):
        base_words_list = []
        for text in self.id_to_text_dict.values():
            try:
                base_words = self.morphology_engine.morph_engine_base_words(text)
                base_words_list.append(base_words)
            except Exception as E:
                print(E)
        return base_words_list

    def get_url_from_id(self, _id):
        return self.id_to_tuple_dict[_id][1]

    def sklearn_vectorize(self):
        self.get_id_to_text_dict()
        vectorizer = TfidfVectorizer(stop_words=hebrew_stoplist)
        vectors = vectorizer.fit_transform(processor.return_texts())
        feature_names = vectorizer.get_feature_names()
        dense = vectors.todense()
        dense_list = dense.tolist()

        return dense_list

    @classmethod
    def turn_vectors_to_dict(cls, denseList):
        vector_dict = {}

        for vector in denseList:
            vector_dict[str(denseList.index(vector) + 1)] = vector

        cosine_similarity_dict = {}

        for _id, vector in vector_dict.items():
            vector_similarity_dict = {}
            for other_id, other_vector in vector_dict.items():
                similarity = processor.find_cosine_similarity(vector, other_vector)
                if similarity != 1:
                    vector_similarity_dict[other_id] = similarity
            cosine_similarity_dict[_id] = vector_similarity_dict

        return cosine_similarity_dict

    @classmethod
    def find_top_similarities(cls, cosine_similarity_dict):
        top_similarities_dict = {}
        for _id, vector_similarity_dict in cosine_similarity_dict.items():
            top_dict = {}
            for other_id, similarity in vector_similarity_dict.items():
                if similarity > 0.125:
                    top_dict[other_id] = similarity
            top_similarities_dict[_id] = top_dict

        return top_similarities_dict

    @classmethod
    def get_url_dict(cls, top_similarities_dict):
        used_urls = []
        urls_dict = {}
        for _id, top_four_dict in top_similarities_dict.items():
            top_four_url_dict = {}
            try:
                for inner_id in top_four_dict.keys():
                    url = processor.get_url_from_id(inner_id)
                    if url not in used_urls:
                        top_four_url_dict[inner_id] = url
                urls_dict[_id] = top_four_url_dict
            except Exception as e:
                urls_dict[_id] = {}
        return urls_dict

    @classmethod
    def present_urls_similars(cls, urls_dict):
        for _id, url_dict in urls_dict.items():
            print(processor.get_url_from_id(_id))
            print("\n")
            try:
                for url in url_dict.values():
                    if len(url) == 0:
                        print("No similar texts")
                    else:
                        print(url)
            except Exception:
                print("No similar texts")
            print("\n\n\n")


processor = NLPProcessor()
dense_list = processor.sklearn_vectorize()
similarity_dict = NLPProcessor.turn_vectors_to_dict(dense_list)
top_similarities = NLPProcessor.find_top_similarities(similarity_dict)
url_dict = NLPProcessor.get_url_dict(top_similarities)
NLPProcessor.present_urls_similars(url_dict)
