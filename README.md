# LLMTest Enhanced 🧪

A Python-based testing framework for evaluating the performance, consistency, and quality of Large Language Models (LLMs) from the Hugging Face Hub.

This script provides a structured way to run a suite of tests against any `text-generation` model, check its outputs against various quality metrics, and save the results for analysis.

## Features

- **Easy Model Loading**: Load any `text-generation` model from the Hugging Face Hub by name.
- **Comprehensive Test Suite**: Comes with a predefined set of test cases across different categories (e.g., factual, code generation, narrative).
- **Detailed Quality Checks**: Each generated response is automatically checked for:
    - Non-emptiness
    - Absence of common error messages
    - Response time (timeout)
    - Reasonable length
    - Excessive repetition
- **Consistency Testing**: Evaluate if the model produces similar outputs for the same prompt over multiple runs.
- **Automatic Results Logging**: All test results are saved to a timestamped JSON file for later inspection and analysis.
- **Console Summary**: Get an immediate, easy-to-read summary of test outcomes, including category-wise performance and details on failed tests.

## Requirements

- Python 3.7+
- PyTorch
- Transformers library from Hugging Face

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    A `requirements.txt` file is provided for convenience.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Simply run the script from your terminal. By default, it uses the `gpt2` model.

```bash
python llmtest.py
```

### Expected Output

You will see a detailed log in your console as the tests run, followed by a summary.

```
Welcome to LLMTest Enhanced! 🧪
============================================================
Loading model: gpt2...
Model loaded! ✓
Warming up model...
Warmup complete! ✓

============================================================
Running Comprehensive Test Suite
============================================================
✓ PASS | introduction | Time: 1.2s | Tokens: 22
     Generated: a great guy, and I'm sure you'll find it hard to find a...
✓ PASS | description  | Time: 0.95s | Tokens: 24
     Generated: beautiful, with a high of 75 degrees and a low of 75....
...

------------------------------------------------------------
Running Consistency Tests
------------------------------------------------------------
✓ CONSISTENT | Hello, my name is
...

============================================================
Summary: 5/5 tests passed
Consistency: 2/2 consistent
============================================================

Results saved to: llm_test_results_20231027_103000.json

Detailed Analysis:
------------------------------------------------------------

Performance by Category:
  introduction: 100% pass rate
  description : 100% pass rate
  code        : 100% pass rate
  factual     : 100% pass rate
  narrative   : 100% pass rate
```

### Programmatic Usage

You can also import the `LLMTester` class into your own scripts for more customized testing.

```python
from llmtest import LLMTester

# Initialize the tester with a different model
tester = LLMTester(model_name="distilgpt2")

# Run a single, custom test
result = tester.test_completion(
    prompt="The meaning of life is",
    max_new_tokens=100,
    temperature=0.8
)
print(result)

# Run the full predefined suite
all_results = tester.run_test_suite(include_consistency=True)

# Save the results
tester.save_results(all_results, "my_custom_test_run.json")
```

## Customizing Tests

To add your own test cases, simply modify the `test_cases` list within the `run_test_suite` method in `llmtest.py`. Each test case is a dictionary with a `prompt`, a list of `expected_words`, and a `category`.

```python
# Inside the run_test_suite method in llmtest.py

test_cases = [
    # ... existing cases
    {
        "prompt": "Translate to French: I love programming.",
        "expected_words": ["j'adore", "programmer", "programmation"],
        "category": "translation"
    }
]
```