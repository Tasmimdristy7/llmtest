class QualityEvaluator:
    
    def __init__(self):
        pass
    
    def evaluate(self, response):
    
        checks = {
            'has_content': len(response.strip()) > 0,
            'ends_properly': response.strip()[-1] in '.!?:' if response.strip() else False,
            'no_repetition': not self._has_repetition(response),
            'reasonable_length': 10 < len(response) < 500,
            'has_capital': any(c.isupper() for c in response) if response else False,
            'no_special_chars': not any(c in response for c in ['@', '#', '$', '%', '^', '&', '*'])
        }
        
        passed_checks = sum(checks.values())
        total_checks = len(checks)
        
        all_passed = passed_checks >= 4  
        
        failed_checks = [k.replace('_', ' ') for k, v in checks.items() if not v]
        if all_passed:
            message = f" Good quality ({passed_checks}/{total_checks} checks passed)"
        else:
            message = f" Quality issues: {', '.join(failed_checks)}"
        
        return {
            'passed': all_passed,
            'checks': checks,
            'passed_checks': passed_checks,
            'total_checks': total_checks,
            'message': message,
            'quality_score': passed_checks / total_checks
        }
    
    def _has_repetition(self, text):
        """Check if text has word repetition."""
        words = text.lower().split()
        if len(words) < 3:
            return False
        
        # Check for repeated words in sequence
        for i in range(len(words) - 2):
            if words[i] == words[i + 1] == words[i + 2]:
                return True
        
        # Check for excessive repetition of any word
        if words:
            word_counts = {}
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1
            
            max_count = max(word_counts.values())
            if max_count > len(words) * 0.3:  # If any word is more than 30% of text
                return True
        
        return False