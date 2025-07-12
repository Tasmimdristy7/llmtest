from llm_test_suite.evaluators.length import LengthEvaluator
from llm_test_suite.utils.results_manager import ResultsManager
from transformers import pipeline

evaluator = LengthEvaluator(min_words=3, max_words=30)  # Increased max to 30
results_manager = ResultsManager("results")

print("Loading model...")
model = pipeline("text-generation", model="gpt2")

# Test cases with better prompts
test_cases = [
    {
        "name": "greeting",
        "prompt": "Say hello:",  # Shorter prompt
    },
    {
        "name": "question", 
        "prompt": "What color is the sky?",  # Specific question
    },
    {
        "name": "instruction",
        "prompt": "How to tie shoes: Step 1:",  # Clear format
    }
]

print("\n" + "="*50)
print("Running Tests and Saving Results") 
print("="*50)

# Store all results
all_results = []

for test in test_cases:
    print(f"\nTest: {test['name']}")
    print(f"Prompt: {test['prompt']}")
    
    # Generate response with FEWER tokens
    result = model(
        test['prompt'], 
        max_new_tokens=15,  # Reduced from 30 to 15
        temperature=0.7,
        pad_token_id=model.tokenizer.eos_token_id  # Suppress warning
    )
    full_response = result[0]['generated_text']
    generated_text = full_response[len(test['prompt']):].strip()
    
    print(f"Response: {generated_text}")
    
    # Evaluate
    evaluation = evaluator.evaluate(generated_text)
    print(f"Result: {evaluation['message']}")
    
    # Add extra info to evaluation
    evaluation['test_name'] = test['name']
    evaluation['prompt'] = test['prompt']
    evaluation['response'] = generated_text
    results_manager.save_result(f"test_{test['name']}", evaluation)
    
    all_results.append(evaluation)

print("\n" + "-"*50)
results_manager.save_multiple_results("length_evaluation", all_results)

passed = sum(1 for r in all_results if r['passed'])
print(f"\nSummary: {passed}/{len(all_results)} tests passed")