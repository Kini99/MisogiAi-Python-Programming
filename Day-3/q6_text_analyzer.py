from collections import Counter
import string

class TextAnalyzer:
    def __init__(self, text):
        self.text = text.lower()  # case-insensitive analysis

    def get_character_frequencies(self, include_spaces=False):
        filtered_text = self.text if include_spaces else self.text.replace(" ", "")
        return dict(Counter(filtered_text))

    def get_word_frequencies(self, min_length=3):
        words = self.text.split()
        filtered_words = [word.strip(string.punctuation) for word in words if len(word.strip(string.punctuation)) >= min_length]
        return dict(Counter(filtered_words))

    def get_sentence_length_distribution(self):
        sentences = self.text.split('.')
        sentence_lengths = [len(sentence.strip().split()) for sentence in sentences if sentence.strip()]
        return {
            'count': len(sentence_lengths),
            'average': sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0,
            'longest': max(sentence_lengths) if sentence_lengths else 0,
            'shortest': min(sentence_lengths) if sentence_lengths else 0
        }

    def find_common_words(self, n=5, exclude_common=True):
        common_words = set([
            'the', 'and', 'of', 'to', 'in', 'a', 'is', 'it', 'that', 'for', 'on', 'with',
            'as', 'was', 'at', 'by', 'an', 'be', 'this', 'have', 'from', 'or', 'are',
            'but', 'not', 'they', 'you', 'he', 'she', 'we', 'his', 'her', 'has', 'had', 'them'
        ])
        words = self.text.split()
        filtered = [
            word.strip(string.punctuation) for word in words
            if word.strip(string.punctuation) and (not exclude_common or word not in common_words)
        ]
        return Counter(filtered).most_common(n)

    def reading_statistics(self):
        words = self.text.split()
        sentences = self.text.split('.')
        sentence_count = sum(1 for s in sentences if s.strip())
        word_count = len([word for word in words if word.strip(string.punctuation)])
        avg_word_length = sum(len(word.strip(string.punctuation)) for word in words if word.strip(string.punctuation)) / word_count if word_count else 0
        return {
            'character_count': len(self.text),
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_word_length': round(avg_word_length, 2),
            'reading_time': round(word_count / 200, 2)  # assuming 200 WPM
        }

    def compare_with_text(self, other_text):
        other = TextAnalyzer(other_text)
        own_words = set(self.text.split())
        other_words = set(other_text.split())

        common = own_words & other_words
        unique_self = own_words - other_words
        unique_other = other_words - own_words
        similarity = round(len(common) / len(own_words | other_words), 2) if (own_words | other_words) else 0

        return {
            'common_words': list(common),
            'similarity_score': similarity,
            'unique.to.first': list(unique_self),
            'unique.to.second': list(unique_other)
        }

# Test input implementation
sample_text = """
Python is a high-level, interpreted programming language with dynamic semantics.
Its high-level built-in data structures, combined with dynamic typing and dynamic
binding, make it very attractive for Rapid Application Development. Python is simple to learn.
Python's syntax emphasizes readability and reduces the cost of program maintenance.
"""

analyzer = TextAnalyzer(sample_text)

print("Character frequencies (top 5):", analyzer.get_character_frequencies())
print("Word frequency (top 5):", analyzer.get_word_frequencies(min_length=5))
print("Sentence stats:", analyzer.get_sentence_length_distribution())
print("Top uncommon words:", analyzer.find_common_words(5))
print("Reading stats:", analyzer.reading_statistics())

compare_text = "Python is a programming language. Java is object-oriented and platform independent."
comparison = analyzer.compare_with_text(compare_text)
print("Comparison:", comparison)
