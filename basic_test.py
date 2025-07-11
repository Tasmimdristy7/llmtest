from llm_test_suite.config import Config
from transformers import pipeline

# Test our config
config = Config()
print(f"Model: {config.target_model}")
print(f"Device: {config.target_device}")

# Test if we can load a model
print("\nLoading model...")
model = pipeline("text-generation", model=config.target_model)

# Test generation
prompt = "Hello, my name is"
result = model(prompt, max_new_tokens=10)
print(f"\nPrompt: {prompt}")
print(f"Response: {result[0]['generated_text']}")

print("setup is working!")