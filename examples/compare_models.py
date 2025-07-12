# examples/compare_models.py

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from llm_test_suite.comparisons.model_comparator import ModelComparator
from llm_test_suite.evaluators.length import LengthEvaluator
from llm_test_suite.evaluators.quality import QualityEvaluator
from llm_test_suite.utils.results_manager import ResultsManager

# Models to compare (you can add more)
models_to_compare = [
    "gpt2",           # 124M parameters
    "distilgpt2",     # 82M parameters (smaller, faster)
    # "gpt2-medium",  # 355M parameters (uncomment if you have space)
]

# Initialize comparator
print(" Model Comparison Tool")
print("=" * 60)
comparator = ModelComparator(models_to_compare)

# Initialize evaluators
evaluators = [
    LengthEvaluator(min_words=5, max_words=30),
    QualityEvaluator()
]

# Define test cases
test_cases = [
    {
        'name': 'greeting',
        'prompt': 'Hello, my name is',
        'max_tokens': 15
    },
    {
        'name': 'story',
        'prompt': 'Once upon a time in a small village',
        'max_tokens': 25
    },
    {
        'name': 'question',
        'prompt': 'The meaning of life is',
        'max_tokens': 20
    },
    {
        'name': 'completion',
        'prompt': 'Artificial intelligence will',
        'max_tokens': 20
    },
    {
        'name': 'description',
        'prompt': 'The ocean is',
        'max_tokens': 15
    }
]

# Run comparison
results = comparator.run_comparison_suite(test_cases, evaluators)

# Print detailed summary
print("\n" + "=" * 60)
print(" COMPARISON SUMMARY")
print("=" * 60)

# Model performance summary
print("\n🏎️  Performance Metrics:")
for model_name, stats in results['summary']['model_stats'].items():
    print(f"\n{model_name}:")
    print(f"  • Average generation time: {stats['avg_generation_time']:.3f}s")
    print(f"  • Total time: {stats['total_time']:.2f}s")
    print(f"  • Failed responses: {stats['failed_responses']}/{stats['total_responses']}")

# Find best responses for each test
print("\n Best Responses by Test:")
for test_result in results['test_results']:
    print(f"\n{test_result['test_name']}:")
    print(f"Prompt: '{test_result['prompt']}'")
    
    # Find model with best evaluations
    best_model = None
    best_score = -1
    
    for model_name, model_result in test_result['model_responses'].items():
        if model_result['error'] or 'evaluations' not in model_result:
            continue
            
        # Count passed evaluations
        passed_count = sum(
            1 for eval_result in model_result['evaluations'].values()
            if eval_result.get('passed', False)
        )
        
        if passed_count > best_score:
            best_score = passed_count
            best_model = model_name
    
    if best_model:
        print(f"  Best: {best_model} ({best_score}/{len(evaluators)} passed)")
        print(f"  Response: '{test_result['model_responses'][best_model]['response'][:60]}...'")

# Quality comparison
print("\n📈 Quality Comparison:")
model_quality_scores = {model: [] for model in models_to_compare}

for test_result in results['test_results']:
    for model_name, model_result in test_result['model_responses'].items():
        if not model_result['error'] and 'evaluations' in model_result:
            # Count passed evaluations as quality score
            passed = sum(
                1 for eval_result in model_result['evaluations'].values()
                if eval_result.get('passed', False)
            )
            model_quality_scores[model_name].append(passed)

print("\nAverage quality scores (higher is better):")
for model_name, scores in model_quality_scores.items():
    if scores:
        avg_score = sum(scores) / len(scores)
        print(f"  {model_name}: {avg_score:.2f}/{len(evaluators)}")

# Save results
results_manager = ResultsManager("results")
results_manager.save_multiple_results("model_comparison", results['test_results'])

print("\n Comparison complete! Results saved to results/")

# Speed ranking
print("\n⚡ Speed Ranking (fastest to slowest):")
speed_ranking = sorted(
    results['summary']['model_stats'].items(),
    key=lambda x: x[1]['avg_generation_time']
)
for i, (model_name, stats) in enumerate(speed_ranking, 1):
    print(f"  {i}. {model_name}: {stats['avg_generation_time']:.3f}s per response")