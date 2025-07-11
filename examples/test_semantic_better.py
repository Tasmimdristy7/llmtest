import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from llm_test_suite.evaluators.semantic import SemanticSimilarityEvaluator
from llm_test_suite.utils.results_manager import ResultsManager
from transformers import pipeline

# Initialize components
print("🚀 Setting up semantic similarity test...")
evaluator = SemanticSimilarityEvaluator(similarity_threshold=0.6)  # Slightly lower threshold
results_manager = ResultsManager("results")

# Load model
print("\nLoading language model...")
model = pipeline("text-generation", model="gpt2")

# Test cases designed for GPT-2's strengths
test_cases = [
    {
        "name": "complete_sentence",
        "prompt": "The weather today is",
        "expected": "The weather is nice and sunny"
    },
    {
        "name": "story_continuation",
        "prompt": "Once upon a time, there was a",
        "expected": "Once upon a time, there was a princess"
    },
    {
        "name": "complete_phrase", 
        "prompt": "I love to eat",
        "expected": "I love to eat pizza and pasta"
    },
    {
        "name": "greeting_complete",
        "prompt": "Hello, my name is",
        "expected": "Hello, my name is John"
    },
    {
        "name": "simple_fact",
        "prompt": "The sun is very",
        "expected": "The sun is very hot and bright"
    },
    {
        "name": "opinion",
        "prompt": "Pizza tastes",
        "expected": "Pizza tastes delicious"
    }
]

print("\n" + "="*60)
print("Running Semantic Similarity Tests (Better Prompts)")
print("="*60)

all_results = []

for test in test_cases:
    print(f"\n📝 Test: {test['name']}")
    print(f"Prompt: {test['prompt']}")
    print(f"Expected meaning: {test['expected']}")
    
    # Generate response with settings that work well
    result = model(
        test['prompt'],
        max_new_tokens=10,  # Keep it short
        temperature=0.8,
        do_sample=True,
        pad_token_id=model.tokenizer.eos_token_id
    )
    
    # Extract generated text
    full_response = result[0]['generated_text']
    # For continuation, we want the FULL text including prompt
    # because we're comparing complete thoughts
    
    print(f"Generated: {full_response}")
    
    # Evaluate semantic similarity
    evaluation = evaluator.evaluate(full_response, test['expected'])
    
    print(f"Result: {evaluation['message']}")
    
    # Add test info
    evaluation['test_name'] = test['name']
    evaluation['prompt'] = test['prompt']
    evaluation['full_response'] = full_response
    
    # Save result
    results_manager.save_result(f"semantic_v2_{test['name']}", evaluation)
    all_results.append(evaluation)

# Save all results
print("\n" + "-"*60)
results_manager.save_multiple_results("semantic_similarity_v2_suite", all_results)

# Summary
passed = sum(1 for r in all_results if r['passed'])
total = len(all_results)

print(f"\n📊 Summary: {passed}/{total} tests passed")
print("\nSimilarity Scores:")
for result in all_results:
    score = result['similarity_score']
    status = "✅" if result['passed'] else "❌"
    print(f"  {status} {result['test_name']}: {score:.2f}")

# Show which types passed
if passed > 0:
    print("\n✅ Passed tests:")
    for result in all_results:
        if result['passed']:
            print(f"  - {result['test_name']}: '{result['prompt']}...'")

# Find best and worst matches
best_match = max(all_results, key=lambda x: x['similarity_score'])
worst_match = min(all_results, key=lambda x: x['similarity_score'])

print(f"\n🏆 Best match: {best_match['test_name']} (score: {best_match['similarity_score']:.2f})")
print(f"📉 Worst match: {worst_match['test_name']} (score: {worst_match['similarity_score']:.2f})")