from scipy import spatial
import advertools as adv
from sklearn.feature_extraction.text import TfidfVectorizer
from flask_app.Backend.DatabaseHandlers.database_handler_orchestrator import DatabaseHandlerOrchestrator
from flask_app.Backend.HebrewMorphologyEngine.morphology_engine import HebrewMorphologyEngine

hebrew_stoplist = adv.stopwords['hebrew']


class NLPProcessor:
    def __init__(self):
        self.terms = {}
        self.id_to_text_dict = {}
        self.id_to_tuple_dict = {}
        self.morphology_engine = HebrewMorphologyEngine()
        self.handler = DatabaseHandlerOrchestrator()
        self.doc_idfs = {}
        self.full_texts_dict = {}
        self.used_urls = []
        self.tfidf_dict = {}

    def get_id_to_text_dict(self):
        rows_tuple_list = self.handler.get_all_rows()
        for row in rows_tuple_list:
            self.id_to_text_dict[str(row[0])] = row[3]
            self.id_to_tuple_dict[str(row[0])] = row
        return self.id_to_text_dict, self.id_to_tuple_dict

    @classmethod
    def find_cosine_similarity(cls, doc_1, doc_2):
        return 1 - spatial.distance.cosine(doc_1, doc_2)

    def return_texts(self):
        base_words_list = []
        for text in self.id_to_text_dict.values():
            base_words_list.append(text)
        return base_words_list

    def get_url_from_id(self, _id):
        return self.id_to_tuple_dict[_id][1]

    def sklearn_vectorize(self):
        vectorizer = TfidfVectorizer(stop_words=hebrew_stoplist)
        vectors = vectorizer.fit_transform(self.return_texts())
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
                similarity = NLPProcessor.find_cosine_similarity(vector, other_vector)
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
                if similarity > 0.175:
                    top_dict[other_id] = similarity
            top_similarities_dict[_id] = top_dict

        return top_similarities_dict

    def get_url_dict(self, top_similarities_dict):
        used_urls = []
        urls_dict = {}
        for _id, top_four_dict in top_similarities_dict.items():
            top_four_url_dict = {}
            try:
                for inner_id in top_four_dict.keys():
                    url = self.get_url_from_id(inner_id)
                    if url not in used_urls:
                        top_four_url_dict[inner_id] = [url, format(top_four_dict[inner_id], ".3f")]
                urls_dict[_id] = top_four_url_dict
            except Exception as e:
                urls_dict[_id] = {}
        return urls_dict

    def present_urls_similars(self, urls_dict):
        for _id, url_dict in urls_dict.items():
            base_url = self.get_url_from_id(_id)
            if base_url not in self.used_urls:
                print(base_url + "  >>")
                url_list = []
                try:
                    for url in url_dict.values():
                        if base_url not in self.used_urls:
                            if len(url) == 0:
                                print("No similar texts")
                            else:
                                url_list.append(url)
                                self.used_urls.append(url)
                except Exception:
                    print("No similar texts")

                print(url_list)
                print("\n")

    print("\n")


if __name__ == "__main__":
    processor = NLPProcessor()
    dense_list = processor.sklearn_vectorize()
    similarity_dict = NLPProcessor.turn_vectors_to_dict(dense_list)
    top_similarities = NLPProcessor.find_top_similarities(similarity_dict)
    url_dict = processor.get_url_dict(top_similarities)
    processor.present_urls_similars(url_dict)
