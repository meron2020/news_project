import nltk
import string
from nltk import word_tokenize
from hebrew_stopwords import hebrew_stoplist
from Parsers.ynet_parser import YnetParser
from Parsers.walla_worker import WallaParser
from DatabaseHandlers.database_handler_orchestrator import DatabaseHandlerOrchestrator

nltk.download("punkt")

ynet_parser = YnetParser("https://www.ynet.co.il/news/article/by11p0p111y")
ynet_full_text = ynet_parser.parse()

walla_parser = WallaParser("https://news.walla.co.il/item/3451256")
walla_full_text = walla_parser.parse()


class NLPProcessor:
    def __init__(self, id_to_text_dict):
        self.terms = {}
        self.handler = DatabaseHandlerOrchestrator()
        self.id_to_text_dict = id_to_text_dict
        self.full_texts_dict = {}

    def get_terms(self, text):
        stoplist = set(hebrew_stoplist)
        terms = {}
        word_list = [word for word in word_tokenize(text.lower())
                     if word not in stoplist and word not in string.punctuation]

        for word in word_list:
            terms[word] = terms.get(word, 0) + 1

        return terms

    def collect_vocabulary(self):
        for _id, full_text in self.id_to_text_dict.items():
            terms = self.get_terms(full_text)
            try:
                for term in terms.keys():
                    if term in self.terms.keys():
                        self.terms[term] = self.terms[term] + terms[term]
                    else:
                        self.terms[term] = terms[term]
            except Exception as e:
                print(e)
            self.full_texts_dict[_id] = terms

        return self.terms

    def vectorize(self):
        output = {}
        for _id in self.id_to_text_dict.keys():
            output_vector = []
            for word in self.terms.keys():
                if word in self.full_texts_dict[str(_id)].keys():
                    output_vector.append(int(self.full_texts_dict[str(_id)][word]))
                else:
                    output_vector.append(0)
            output[_id] = output_vector

        return output

    def calculate_idfs(self, full_text_list):
        doc_idfs = {}
        for term in self.terms:
            doc_count = 0
            pass
            # for doc_


processor = NLPProcessor({"1": ynet_full_text, "2": walla_full_text})
ynet_terms = processor.get_terms(ynet_full_text)
vocabulary = processor.collect_vocabulary()
vector = processor.vectorize()
print(len(ynet_terms))
print(len(vocabulary))
print(vector)