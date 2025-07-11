# test_length_evaluator.py
"""Test the length evaluator."""

from llm_test_suite.evaluators.length import LengthEvaluator
from transformers import pipeline

# Create evaluator
evaluator = LengthEvaluator(min_words=5, max_words=20)

# Load model
print("Loading model...")
model = pipeline("text-generation", model="gpt2")

# Test cases
test_prompts = [
    "Write a short greeting:",
    "Explain what AI is:",
    "Count to five:",
]

print("\n" + "="*50)
print("Testing Length Evaluator")
print("="*50)

for prompt in test_prompts:
    print(f"\nPrompt: {prompt}")
    
    # Generate response
    result = model(prompt, max_new_tokens=30, temperature=0.7)
    full_response = result[0]['generated_text']
    
    # Extract just the generated part (remove prompt)
    generated_text = full_response[len(prompt):].strip()
    print(f"Response: {generated_text}")
    
    # Evaluate
    evaluation = evaluator.evaluate(generated_text)
    print(f"Evaluation: {evaluation['message']}")
    print(f"Details: {evaluation['word_count']} words, Passed: {evaluation['passed']}")