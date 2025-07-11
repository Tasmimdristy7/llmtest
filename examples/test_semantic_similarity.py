import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # Add this to fix the warning

from llm_test_suite.evaluators.semantic import SemanticSimilarityEvaluator
from llm_test_suite.utils.results_manager import ResultsManager
from transformers import pipeline

# Initialize components
print("🚀 Setting up semantic similarity test...")
evaluator = SemanticSimilarityEvaluator(similarity_threshold=0.7)
results_manager = ResultsManager("results")

# Load model
print("\nLoading language model...")
model = pipeline("text-generation", model="gpt2")

# Test cases with expected answers
test_cases = [
    {
        "name": "capital_france",
        "prompt": "What is the capital of France?",
        "expected": "The capital of France is Paris"
    },
    {
        "name": "sky_color",
        "prompt": "What color is the sky?",
        "expected": "The sky is blue"
    },
    {
        "name": "math_simple",
        "prompt": "What is 2 + 2?",
        "expected": "2 + 2 equals 4"
    },
    {
        "name": "greeting",
        "prompt": "How do you say hello in Spanish?",
        "expected": "Hello in Spanish is Hola"
    }
]

print("\n" + "="*60)
print("Running Semantic Similarity Tests")
print("="*60)

all_results = []

for test in test_cases:
    print(f"\n📝 Test: {test['name']}")
    print(f"Prompt: {test['prompt']}")
    print(f"Expected: {test['expected']}")
    
    # Generate response
    result = model(
        test['prompt'],
        max_new_tokens=20,
        temperature=0.7,
        pad_token_id=model.tokenizer.eos_token_id
    )
    
    # Extract generated text
    full_response = result[0]['generated_text']
    generated_text = full_response[len(test['prompt']):].strip()
    
    print(f"Generated: {generated_text}")
    
    # Evaluate semantic similarity
    evaluation = evaluator.evaluate(generated_text, test['expected'])
    
    print(f"Result: {evaluation['message']}")
    
    # Add test info
    evaluation['test_name'] = test['name']
    evaluation['prompt'] = test['prompt']
    
    # Save result
    results_manager.save_result(f"semantic_{test['name']}", evaluation)
    all_results.append(evaluation)

# Save all results
print("\n" + "-"*60)
results_manager.save_multiple_results("semantic_similarity_suite", all_results)

# Summary
passed = sum(1 for r in all_results if r['passed'])
total = len(all_results)

print(f"\n Summary: {passed}/{total} tests passed")
print("\nSimilarity Scores:")
for result in all_results:
    score = result['similarity_score']
    status = "" if result['passed'] else "❌"
    print(f"  {status} {result['test_name']}: {score:.2f}")

# Find best and worst matches
best_match = max(all_results, key=lambda x: x['similarity_score'])
worst_match = min(all_results, key=lambda x: x['similarity_score'])

print(f"\n🏆 Best match: {best_match['test_name']} (score: {best_match['similarity_score']:.2f})")
print(f"📉 Worst match: {worst_match['test_name']} (score: {worst_match['similarity_score']:.2f})")