from typing import List, Dict, Any
from datetime import datetime
import time
from transformers import pipeline


class ModelComparator:
    """Compare multiple models on the same tests."""
    
    def __init__(self, model_names: List[str]):
        """
        Initialize with list of model names to compare.
        
        Args:
            model_names: List of Hugging Face model names
        """
        self.model_names = model_names
        self.models = {}
        self._load_models()
        
    def _load_models(self):
        """Load all models."""
        print(f"🤖 Loading {len(self.model_names)} models for comparison...")
        
        for model_name in self.model_names:
            print(f"  Loading {model_name}...", end="", flush=True)
            start_time = time.time()
            
            try:
                self.models[model_name] = pipeline(
                    "text-generation",
                    model=model_name,
                    device=-1  # CPU
                )
                load_time = time.time() - start_time
                print(f" ✓ ({load_time:.1f}s)")
            except Exception as e:
                print(f" ✗ Failed: {str(e)}")
                self.models[model_name] = None
    
    def compare_single_prompt(self, prompt: str, max_new_tokens: int = 20) -> Dict[str, Any]:
        """
        Compare all models on a single prompt.
        
        Args:
            prompt: Input prompt
            max_new_tokens: Maximum tokens to generate
            
        Returns:
            Dictionary with comparison results
        """
        results = {
            'prompt': prompt,
            'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'model_responses': {}
        }
        
        for model_name, model in self.models.items():
            if model is None:
                results['model_responses'][model_name] = {
                    'response': "Model failed to load",
                    'error': True,
                    'generation_time': 0
                }
                continue
            
            # Generate response
            start_time = time.time()
            try:
                output = model(
                    prompt,
                    max_new_tokens=max_new_tokens,
                    temperature=0.7,
                    pad_token_id=model.tokenizer.eos_token_id
                )
                generation_time = time.time() - start_time
                
                full_text = output[0]['generated_text']
                generated_only = full_text[len(prompt):].strip()
                
                results['model_responses'][model_name] = {
                    'response': generated_only,
                    'full_text': full_text,
                    'generation_time': generation_time,
                    'token_count': len(model.tokenizer.encode(generated_only)),
                    'error': False
                }
                
            except Exception as e:
                results['model_responses'][model_name] = {
                    'response': f"Generation failed: {str(e)}",
                    'error': True,
                    'generation_time': time.time() - start_time
                }
        
        return results
    
    def compare_with_evaluators(self, prompt: str, evaluators: List[Any], 
                               max_new_tokens: int = 20) -> Dict[str, Any]:
        """
        Compare models and evaluate each response.
        
        Args:
            prompt: Input prompt
            evaluators: List of evaluator instances
            max_new_tokens: Maximum tokens to generate
            
        Returns:
            Comparison results with evaluations
        """
        # First, get all model responses
        comparison = self.compare_single_prompt(prompt, max_new_tokens)
        
        # Then evaluate each response
        for model_name, model_result in comparison['model_responses'].items():
            if model_result['error']:
                continue
                
            model_result['evaluations'] = {}
            
            for evaluator in evaluators:
                evaluator_name = evaluator.__class__.__name__
                
                try:
                    # Simple evaluation (just response)
                    if hasattr(evaluator, 'evaluate') and evaluator.__class__.__name__ != 'SemanticSimilarityEvaluator':
                        eval_result = evaluator.evaluate(model_result['response'])
                        model_result['evaluations'][evaluator_name] = eval_result
                        
                except Exception as e:
                    model_result['evaluations'][evaluator_name] = {
                        'error': str(e),
                        'passed': False
                    }
        
        return comparison
    
    def run_comparison_suite(self, test_cases: List[Dict[str, Any]], 
                           evaluators: List[Any] = None) -> Dict[str, Any]:
        """
        Run complete comparison suite.
        
        Args:
            test_cases: List of test cases with prompts
            evaluators: Optional list of evaluators
            
        Returns:
            Complete comparison results
        """
        suite_results = {
            'models': self.model_names,
            'start_time': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'test_results': [],
            'summary': {}
        }
        
        print(f"\n🏁 Running comparison suite with {len(test_cases)} tests")
        print("=" * 60)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest {i}/{len(test_cases)}: {test_case.get('name', 'Unnamed')}")
            print(f"Prompt: {test_case['prompt']}")
            
            if evaluators:
                result = self.compare_with_evaluators(
                    test_case['prompt'], 
                    evaluators,
                    test_case.get('max_tokens', 20)
                )
            else:
                result = self.compare_single_prompt(
                    test_case['prompt'],
                    test_case.get('max_tokens', 20)
                )
            
            result['test_name'] = test_case.get('name', f'test_{i}')
            suite_results['test_results'].append(result)
            
            # Print responses
            for model_name, model_result in result['model_responses'].items():
                if not model_result['error']:
                    print(f"\n  {model_name}:")
                    print(f"    Response: {model_result['response'][:80]}...")
                    print(f"    Time: {model_result['generation_time']:.2f}s")
                    
                    if 'evaluations' in model_result:
                        for eval_name, eval_result in model_result['evaluations'].items():
                            status = "" if eval_result.get('passed', False) else ""
                            print(f"    {eval_name}: {status}")
        
        # Calculate summary statistics
        suite_results['summary'] = self._calculate_summary(suite_results['test_results'])
        suite_results['end_time'] = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        return suite_results
    
    def _calculate_summary(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate summary statistics."""
        summary = {
            'total_tests': len(test_results),
            'model_stats': {}
        }
        
        for model_name in self.model_names:
            stats = {
                'total_responses': 0,
                'failed_responses': 0,
                'avg_generation_time': 0,
                'total_time': 0
            }
            
            times = []
            for result in test_results:
                if model_name in result['model_responses']:
                    model_result = result['model_responses'][model_name]
                    stats['total_responses'] += 1
                    
                    if model_result['error']:
                        stats['failed_responses'] += 1
                    else:
                        times.append(model_result['generation_time'])
            
            if times:
                stats['avg_generation_time'] = sum(times) / len(times)
                stats['total_time'] = sum(times)
            
            summary['model_stats'][model_name] = stats
        
        return summary