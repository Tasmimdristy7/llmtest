
class LengthEvaluator:
    
    def __init__(self, min_words=5, max_words=50):
        
        self.min_words = min_words
        self.max_words = max_words
    
    def evaluate(self, response):
        
        # Count words
        words = response.split()
        word_count = len(words)
        
        # Check if within range
        is_good_length = self.min_words <= word_count <= self.max_words
        
        # Return results
        return {
            'word_count': word_count,
            'min_words': self.min_words,
            'max_words': self.max_words,
            'passed': is_good_length,
            'message': self._get_message(word_count, is_good_length)
        }
    
    def _get_message(self, word_count, passed):
        if passed:
            return f" Good length: {word_count} words"
        elif word_count < self.min_words:
            return f" Too short: {word_count} words (minimum: {self.min_words})"
        else:
            return f" Too long: {word_count} words (maximum: {self.max_words})"