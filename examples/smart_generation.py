# examples/smart_generation.py
"""Example of better text generation control."""

from transformers import pipeline, set_seed

# Set seed for reproducibility
set_seed(42)

# Load model
print("Loading model...")
model = pipeline("text-generation", model="gpt2")

# Different strategies for controlling output length

print("\n1. Using max_new_tokens (what we've been doing):")
result = model("Hello, my name is", max_new_tokens=10)
print(f"Output: {result[0]['generated_text']}")

print("\n2. Using early stopping:")
result = model(
    "Hello, my name is", 
    max_new_tokens=20,
    num_return_sequences=1,
    temperature=0.7,
    early_stopping=True,  # Stop at first end token
    pad_token_id=model.tokenizer.eos_token_id
)
print(f"Output: {result[0]['generated_text']}")

print("\n3. Using do_sample=False for more predictable output:")
result = model(
    "The capital of France is",
    max_new_tokens=5,
    do_sample=False,  # Greedy decoding - more predictable
    pad_token_id=model.tokenizer.eos_token_id
)
print(f"Output: {result[0]['generated_text']}")

print("\n4. Post-processing - cut at first sentence:")
result = model("Tell me a story about", max_new_tokens=50)
full_text = result[0]['generated_text']
# Extract only generated part
generated = full_text[len("Tell me a story about"):].strip()
# Cut at first period
first_sentence = generated.split('.')[0] + '.' if '.' in generated else generated
print(f"Full output: {generated}")
print(f"First sentence only: {first_sentence}")
print(f"Word count: {len(first_sentence.split())} words")

print("\n5. Using specific prompts that encourage short responses:")
short_prompts = [
    "Answer in one word: What color is grass?",
    "Complete with 3 words: The dog is",
    "Yes or no: Is the sky blue?"
]

for prompt in short_prompts:
    result = model(prompt, max_new_tokens=10, temperature=0.5)
    response = result[0]['generated_text'][len(prompt):].strip()
    print(f"\nPrompt: {prompt}")
    print(f"Response: {response}")