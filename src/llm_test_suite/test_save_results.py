"""Test evaluator with results saving."""

from llm_test_suite.utils.results_manager import ResultsManager
from llm_test_suite.evaluators.length import LengthEvaluator
from transformers import pipeline

# Create evaluator and results manager
evaluator = LengthEvaluator(min_words=5, max_words=20)
results_manager = ResultsManager("results")

# Load model
print("Loading model...")
model = pipeline("text-generation", model="gpt2")

# Test cases
test_cases = [
    {"name": "greeting", "prompt": "Write a short greeting:"},
    {"name": "question", "prompt": "Ask a simple question:"},
    {"name": "instruction", "prompt": "Give a simple instruction:"}
]

print("\n" + "="*50)
print("Running Tests and Saving Results")
print("="*50)

all_results = []

for test in test_cases:
    print(f"\nTest: {test['name']}")
    print(f"Prompt: {test['prompt']}")
    
    # Generate response
    result = model(test['prompt'], max_new_tokens=30, temperature=0.7)
    full_response = result[0]['generated_text']
    generated_text = full_response[len(test['prompt']):].strip()
    
    print(f"Response: {generated_text}")
    
    # Evaluate
    evaluation = evaluator.evaluate(generated_text)
    print(f"Result: {evaluation['message']}")
    
    # Add extra info
    evaluation['test_name'] = test['name']
    evaluation['prompt'] = test['prompt']
    evaluation['response'] = generated_text
    
    # Save individual result
    results_manager.save_result(f"test_{test['name']}", evaluation)
    
    all_results.append(evaluation)

print("\n" + "-"*50)
results_manager.save_multiple_results("length_evaluation", all_results)

passed = sum(1 for r in all_results if r['passed'])
print(f"\nSummary: {passed}/{len(all_results)} tests passed")
