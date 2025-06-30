from typing import List, Tuple
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np, os, dotenv

dotenv.load_dotenv()

class MongodbHelper:
    def __init__(self, uri: str, db_name: str, collection_name: str, text_field: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.text_field = text_field

    def add_document(self, document: dict) -> str:
        if self.text_field not in document:
            raise ValueError(f"Document must contain the field '{self.text_field}'")
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def get_documents(self, query: dict = {}) -> List[str]:
        docs = self.collection.find(query, {self.text_field: 1, '_id': 0})
        return [doc[self.text_field] for doc in docs if self.text_field in doc]

    def find_similar(self, input_text: str, top_x: int = 3, query: dict = {}) -> List[Tuple[str, float]]:
        docs = self.get_documents(query)
        if not docs:
            return []

        corpus = docs + [input_text]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)
        input_vec = tfidf_matrix[-1]
        doc_vecs = tfidf_matrix[:-1]

        similarities = (doc_vecs * input_vec.T).toarray().flatten()
        top_indices = np.argsort(similarities)[::-1][:top_x]
        results = [(docs[i], f" {round(float(similarities[i]), 2)*100} %") for i in top_indices]
        return results
    

# if __name__ == "__main__":
#     # Example usage:
#     # Replace the following with your actual AWS MongoDB connection details
#     #aws_uri = "mongodb+srv://<username>:<password>@<cluster-url>/test?retryWrites=true&w=majority"
#     #aws_uri = "mongodb://cesar:ditfok-gehkyp-6jEdhy@docdb-2025-06-30-10-40-37.cluster-cjkoge84yjc8.eu-west-3.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
#     aws_uri = os.getenv("MONGO_URI", "")
#     if not aws_uri:
#         raise ValueError("MONGO_URI environment variable is not set")
#     db_name = "test_db"
#     collection_name = "collection_test"
#     text_field = "content"

#     # Create an instance of MongodbHelper connected to AWS MongoDB
#     mongodb_helper = MongodbHelper(aws_uri, db_name, collection_name, text_field)

#     # If the database or collection does not exist, MongoDB will create them automatically
#     # when you first insert a document.
#     # For example:
#     sample_doc = {text_field: "Sample text for the new collection"}
#     mongodb_helper.add_document(sample_doc)
#     print("Document added successfully.")
#     res = mongodb_helper.find_similar("Sample text for the new", top_x=5)
#     print(res)