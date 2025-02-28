import json
import re
import nltk
from collections import defaultdict
nltk.download('punkt')

class JSONSearch:
    def __init__(self, platform):
        """Loads only the relevant JSON file based on the platform."""
        self.json_file = f"{platform.lower()}.json"
        self.data = self.load_json()

    def load_json(self):
        """Loads JSON data for the specified platform."""
        try:
            with open(self.json_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠ Error: {self.json_file} not found. Run scraper first.")
            return {}

    def tokenize_query(self, query):
        """Tokenizes the query into words."""
        words = nltk.word_tokenize(query.lower())  
        return set(words)  

    def search(self, query):
        """Searches the JSON documentation for relevant sections."""
        query_words = self.tokenize_query(query)
        scores = defaultdict(dict)

        for section_title, section_content in self.data.items():
            match_count = sum(1 for word in query_words if word in section_title.lower() or word in section_content.lower())

            if match_count > 0:
                scores[section_title] = (match_count, section_content[:500] + "...")  

        sorted_results = dict(sorted(scores.items(), key=lambda x: x[1][0], reverse=True))  

        return sorted_results if sorted_results else {"Error": "No relevant information found."}

# ✅ Standalone Testing
if __name__ == "__main__":
    searcher = JSONSearch("Lytics")  # Test with Lytics JSON
    test_query = "How do I build an audience segment in Lytics?"
    print(json.dumps(searcher.search(test_query), indent=4))
