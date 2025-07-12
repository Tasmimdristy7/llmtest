import re
class SentenceEvaluator:

    
    def __init__(self, max_sentences=2):
     
        self.max_sentences = max_sentences
    
    def evaluate(self, response):
       
        sentences = re.split(r'[.!?]+', response)
       
        sentences = [s.strip() for s in sentences if s.strip()]
        
        sentence_count = len(sentences)
        passed = sentence_count <= self.max_sentences
        
        if passed:
            message = f" Good: {sentence_count} sentence(s)"
        else:
            message = f" Too many sentences: {sentence_count} (max: {self.max_sentences})"
        
        # Also get first sentence
        first_sentence = sentences[0] if sentences else ""
        
        return {
            'sentence_count': sentence_count,
            'max_sentences': self.max_sentences,
            'passed': passed,
            'message': message,
            'first_sentence': first_sentence,
            'sentences': sentences
        }