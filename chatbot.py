import json
import os
import nltk
from collections import defaultdict
from nltk.tokenize import sent_tokenize
from fuzzywuzzy import fuzz  # Import fuzzywuzzy

nltk.download('punkt')

class Chatbot:
    def __init__(self):
        self.valid_platforms = ["segment", "mparticle", "lytics", "zeotap"]
        self.data_dir = "./"  # Ensure JSON files are in the same directory

    def detect_platform(self, question):
        """Detects which platform is mentioned in the question."""
        for platform in self.valid_platforms:
            if platform in question.lower():
                return platform
        return None  # If no platform is found, return None

    def tokenize_query(self, query):
        """Tokenizes the query into words."""
        words = nltk.word_tokenize(query.lower())
        return set(words)  # Remove duplicates

    def search_json(self, platform, query):
        """Searches for relevant sentences in the correct JSON file."""
        json_path = os.path.join(self.data_dir, f"{platform}.json")

        if not os.path.exists(json_path):
            return f"⚠ Error: No documentation found for {platform}. Please run the scraper first."

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        query_words = self.tokenize_query(query)
        scores = defaultdict(list)

        for section_title, section_content in data.items():
            sentences = sent_tokenize(section_content)  # Split into sentences

            for i, sentence in enumerate(sentences):
                # Use fuzzy matching to score similarity between query and sentences
                match_score = fuzz.partial_ratio(query.lower(), sentence.lower())

                if match_score > 50:  # Only consider sentences with a good match
                    next_sentence = sentences[i + 1] if i + 1 < len(sentences) else ""
                    scores[section_title].append((match_score, sentence, next_sentence))

        # Sort sections by most relevant matches
        sorted_results = sorted(scores.items(), key=lambda x: sum(s[0] for s in x[1]), reverse=True)

        if not sorted_results:
            return "No relevant information found."

        # Format and return top 3 sections
        response = []
        for section, matches in sorted_results[:3]:
            response.append(f"📌 **{section}**")
            for match in matches[:2]:  # Top 2 sentences per section
                response.append(match[1])  # Matched sentence
                if match[2]:
                    response.append(match[2])  # Add next sentence if available

        return "\n\n".join(response) if response else "I couldn't find an exact match."

    def get_answer(self, question):
        """Processes the question and returns the most relevant answer."""
        platform = self.detect_platform(question)

        if not platform:
            return "Please specify one of the platforms: Segment, mParticle, Lytics, or Zeotap."

        return self.search_json(platform, question)
