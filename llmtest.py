
from transformers import pipeline, set_seed
import time
from typing import Dict, Any, List, Optional
import json
from datetime import datetime


class LLMTester:
    
    
    def __init__(self, model_name: str = "gpt2", device: str = "cpu"):
        """Initialize with a model from Hugging Face."""
        print(f"Loading model: {model_name}...")
        self.model_name = model_name
        self.device = device
        
        # Load model with explicit device setting
        self.pipeline = pipeline(
            "text-generation", 
            model=model_name,
            device=0 if device == "cuda" else -1  # -1 for CPU
        )
        
        # Set random seed for reproducibility
        set_seed(42)
        
        print("Model loaded! ✓")
        
        # Warm up the model
        self._warmup()
    
    def _warmup(self):
        """Warm up the model with a dummy generation"""
        print("Warming up model...")
        self.pipeline("Hello", max_new_tokens=5, temperature=0.1)
        print("Warmup complete! ✓")
    
    def test_completion(
        self,
        prompt: str,
        max_new_tokens: int = 50,
        temperature: float = 0.7,
        timeout: int = 15,  # Increased timeout
    ) -> Dict[str, Any]:
       
        print(f"\nTesting prompt: '{prompt}'")
        
        # Measure time
        start_time = time.time()
        
        try:
            # Generate text with explicit padding token
            result = self.pipeline(
                prompt,
                max_new_tokens=max_new_tokens,
                num_return_sequences=1,
                temperature=temperature,
                pad_token_id=self.pipeline.tokenizer.eos_token_id,
                do_sample=True,  # Enable sampling for temperature to work
            )[0]
            
            end_time = time.time()
            
            # Extract generated text
            full_text = result["generated_text"]
            completion = full_text[len(prompt):]
            
            # Enhanced checks
            checks = {
                "not_empty": len(completion.strip()) > 0,
                "no_error_in_response": "error" not in completion.lower(),
                "response_time_ok": (end_time - start_time) < timeout,
                "reasonable_length": 5 < len(completion.split()) < 100,
                "no_repetition": not self._has_excessive_repetition(completion),
            }
            
            return {
                "prompt": prompt,
                "completion": completion.strip(),
                "full_text": full_text,
                "time_taken": round(end_time - start_time, 2),
                "token_count": len(self.pipeline.tokenizer.encode(completion)),
                "checks": checks,
                "all_passed": all(checks.values()),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "prompt": prompt,
                "completion": "",
                "full_text": "",
                "time_taken": round(time.time() - start_time, 2),
                "token_count": 0,
                "checks": {"error_occurred": False},
                "all_passed": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _has_excessive_repetition(self, text: str, threshold: float = 0.5) -> bool:
        """Check if text has excessive word repetition"""
        words = text.lower().split()
        if len(words) < 10:
            return False
        
        unique_words = set(words)
        repetition_ratio = 1 - (len(unique_words) / len(words))
        return repetition_ratio > threshold
    
    def test_consistency(self, prompt: str, num_runs: int = 3) -> Dict[str, Any]:
        """Test if model gives consistent outputs for same prompt"""
        print(f"\nTesting consistency for: '{prompt}'")
        
        outputs = []
        for i in range(num_runs):
            result = self.test_completion(prompt, temperature=0.5)
            outputs.append(result["completion"])
        
        # Check similarity between outputs
        all_similar = all(
            self._are_similar(outputs[i], outputs[i+1]) 
            for i in range(len(outputs)-1)
        )
        
        return {
            "prompt": prompt,
            "outputs": outputs,
            "consistent": all_similar,
            "num_runs": num_runs
        }
    
    def _are_similar(self, text1: str, text2: str, threshold: float = 0.3) -> bool:
        """Simple similarity check based on common words"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return False
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        jaccard_similarity = len(intersection) / len(union)
        return jaccard_similarity > threshold
    
    def run_test_suite(self, include_consistency: bool = False) -> Dict[str, Any]:
        """Run comprehensive test suite"""
        test_cases = [
            {
                "prompt": "Hello, my name is",
                "expected_words": ["name", "I", "am"],
                "category": "introduction"
            },
            {
                "prompt": "The weather today is",
                "expected_words": ["sunny", "cloudy", "rain", "weather", "day"],
                "category": "description"
            },
            {
                "prompt": "def fibonacci(n):",
                "expected_words": ["return", "if", "def", "fibonacci"],
                "category": "code"
            },
            {
                "prompt": "The capital of France is",
                "expected_words": ["Paris"],
                "category": "factual"
            },
            {
                "prompt": "Once upon a time",
                "expected_words": ["there", "was", "lived", "story"],
                "category": "narrative"
            }
        ]
        
        results = []
        consistency_results = []
        
        print("\n" + "="*60)
        print("Running Comprehensive Test Suite")
        print("="*60)
        
        # Basic completion tests
        for test_case in test_cases:
            result = self.test_completion(test_case["prompt"])
            
            # Check for expected words
            completion_lower = result["completion"].lower()
            has_expected = any(
                word in completion_lower 
                for word in test_case["expected_words"]
            )
            
            result["has_expected_words"] = has_expected
            result["category"] = test_case["category"]
            results.append(result)
            
            # Print summary
            status = "✓ PASS" if result["all_passed"] else "✗ FAIL"
            print(f"{status} | {test_case['category']:10} | Time: {result['time_taken']}s | Tokens: {result['token_count']}")
            print(f"     Generated: {result['completion'][:60]}...")
        
        # Consistency tests
        if include_consistency:
            print("\n" + "-"*60)
            print("Running Consistency Tests")
            print("-"*60)
            
            for prompt in ["Hello, my name is", "The weather today is"]:
                consistency_result = self.test_consistency(prompt)
                consistency_results.append(consistency_result)
                
                status = "✓ CONSISTENT" if consistency_result["consistent"] else "✗ INCONSISTENT"
                print(f"{status} | {prompt}")
        
        # Summary
        passed = sum(1 for r in results if r["all_passed"])
        total = len(results)
        
        print(f"\n{'='*60}")
        print(f"Summary: {passed}/{total} tests passed")
        if consistency_results:
            consistent = sum(1 for r in consistency_results if r["consistent"])
            print(f"Consistency: {consistent}/{len(consistency_results)} consistent")
        print(f"{'='*60}\n")
        
        return {
            "completion_tests": results,
            "consistency_tests": consistency_results,
            "summary": {
                "total_tests": total,
                "passed": passed,
                "failed": total - passed,
                "pass_rate": f"{(passed/total)*100:.1f}%",
                "timestamp": datetime.now().isoformat()
            }
        }
    
    def save_results(self, results: Dict[str, Any], filename: str = None):
        """Save test results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"llm_test_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to: {filename}")


def main():
    """Main function with enhanced features"""
    print("Welcome to LLMTest Enhanced! 🧪")
    print("=" * 60)
    
    # Create tester
    tester = LLMTester("gpt2")
    
    # Run comprehensive tests
    results = tester.run_test_suite(include_consistency=True)
    
    # Save results
    tester.save_results(results)
    
    # Show detailed analysis
    print("\nDetailed Analysis:")
    print("-" * 60)
    
    # Category performance
    category_performance = {}
    for test in results["completion_tests"]:
        category = test["category"]
        if category not in category_performance:
            category_performance[category] = []
        category_performance[category].append(test["all_passed"])
    
    print("\nPerformance by Category:")
    for category, passes in category_performance.items():
        pass_rate = sum(passes) / len(passes) * 100
        print(f"  {category:12}: {pass_rate:.0f}% pass rate")
    
    # Failed tests details
    failures = [r for r in results["completion_tests"] if not r["all_passed"]]
    if failures:
        print("\nFailed Tests Details:")
        for fail in failures:
            print(f"  - Prompt: '{fail['prompt']}'")
            print(f"    Failed checks: {[k for k, v in fail['checks'].items() if not v]}")
            print(f"    Time taken: {fail['time_taken']}s")


if __name__ == "__main__":
    main()