from llm_test_suite.evaluators.length import LengthEvaluator
from transformers import pipeline


def main():
    evaluator = LengthEvaluator(min_words=5, max_words=20)

    print("Loading gpt2 model...")
    # Using a simple text-generation model for the test
    model = pipeline("text-generation", model="gpt2")
    print("Model loaded.")

    # A few different prompts to test against
    test_prompts = [
        "Write a short greeting:",
        "Explain what AI is in one sentence:",
        "Count to five:",
    ]

    print("\n" + "=" * 50)
    print("--- Testing Length Evaluator ---")
    print("=" * 50)

    for prompt in test_prompts:
        print(f"\n>>> Prompt: {prompt}")

        # Generate a response from the model
        # Setting pad_token_id to suppress a common warning
        output = model(
            prompt,
            max_new_tokens=30,
            temperature=0.7,
            pad_token_id=model.tokenizer.eos_token_id,
        )
        full_response = output[0]["generated_text"]

        # Isolate the newly generated text from the original prompt
        generated_text = full_response[len(prompt) :].strip()
        print(f'    Response: "{generated_text}"')

        # Use the evaluator to check the response
        evaluation = evaluator.evaluate(generated_text)
        print(f"    Evaluation: {evaluation['message']}")
        print(f"    (Words: {evaluation['word_count']}, Passed: {evaluation['passed']})")


if __name__ == "__main__":
    main()