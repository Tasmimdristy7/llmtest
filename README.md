# LLM Test Suite - AI Testing Framework

This is a comprehensive testing framework for Large Language Models (LLMs). It provides automated evaluation of AI model outputs across multiple dimensions:

Response quality and coherence
Semantic accuracy and meaning preservation
Performance metrics and benchmarking
Cross-model comparison capabilities

The framework is designed to solve the real problem of evaluating LLM outputs systematically rather than manually checking each response.


When working with LLMs, there's no standard way to:

Systematically evaluate if responses are good or bad
Compare different models objectively
Track model performance over time
Detect when models give incorrect or inappropriate answers

I created this framework to:

Automate LLM evaluation with multiple criteria
Provide consistent, reproducible testing
Enable data-driven model selection
Create a reusable testing infrastructure for AI applications

Project Evolution
Starting Point

Given: llmtest.py - a monolithic testing script
Challenge: Transform it into a modular, extensible framework
Goal: Create a professional testing suite for LLM evaluation

Development Phases
Phase 1: Analysis and Understanding

Analyzed the original llmtest.py structure
Identified core testing patterns
Recognized need for modularity

Phase 2: Architecture Design

Designed modular architecture
Separated concerns (evaluators, runners, reporting)
Created extensible interfaces

Phase 3: Implementation

Evaluators System: Built pluggable evaluation modules
Results Management: Created persistent storage system
Reporting Engine: Developed visual dashboards
Semantic Analysis: Integrated NLP-based evaluation
Comparison Tools: Built multi-model testing capabilities

Complete Setup Guide
Prerequisites

Python 3.8 or newer
4GB free disk space (for AI models)
Internet connection (to download models)
Terminal/Command Prompt basic knowledge

Step 1: Get the Code
bash# Clone from GitHub (replace YOUR_USERNAME)
git clone https://github.com/YOUR_USERNAME/llm-test-suite.git
cd llm-test-suite

# Or download and extract ZIP file
Step 2: Set Up Python Environment
bash# Create virtual environment (isolated Python)
python -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# You should see (venv) in your terminal
Step 3: Install Dependencies
bash# Install required packages
pip install -r requirements.txt

# This installs:
 - transformers (for AI models)
- torch (for calculations)
 - sentence-transformers (for semantic testing)
 - numpy, scikit-learn (for math operations)

Step 4: Install Project in Development Mode

bash# This lets Python find your code
pip install -e .

Step 5: Verify Installation
bash# Run the basic test
python basic_test.py

# You should see:
 Model: gpt2
 Loading model...
Response: Hello, my name is John...
Basic setup is working!
Step 6: Run Your First Real Test
bash# Test with results saving
python examples/test_save_results.py

# Check results folder
ls results/
# You'll see JSON files with test results

Project Structure Explained

```text
llm-test-suite/
├── llmtest.py                  # ORIGINAL: Monolithic test file (starting point)
├── basic_test.py               #  First simple test to verify setup
│
├── src/llm_test_suite/         # New modular package
│   ├── __init__.py             # Marks as Python package
│   ├── config.py               # Global config: model names, paths
│   ├── models.py               # Data classes: TestResult, Metric, etc.
│   ├── exceptions.py           # Custom error types
│
│   ├── evaluators/             # Evaluate model outputs
│   │   ├── length.py           # Check word/char length
│   │   ├── quality.py          # Check punctuation, repetition, format
│   │   ├── semantic.py         # Semantic similarity checks
│   │   └── sentence.py         # Sentence counting
│
│   ├── utils/                  # Utility helpers
│   │   └── results_manager.py  # Save/load results with timestamps
│
│   ├── runners/                #  Test orchestrators
│   │   └── simple_runner.py    # Combine evaluators to run a suite
│
│   ├── reporting/              # Reporting tools
│   │   └── dashboard.py        # Generate HTML dashboards
│
│   └── comparisons/            #  Compare multiple models
│       └── model_comparator.py # Cross-model testing
│
├── examples/                   # Example scripts
│   ├── test_save_results.py    # Run test & save JSON results
│   ├── test_semantic_similarity.py # Check semantic similarity
│   ├── compare_models.py       # Compare several models
│   └── generate_dashboard.py   # Build visual HTML report
│
├── results/                    # Saved test outputs (JSON, HTML)
├── requirements.txt            # Dependency list
├── setup.py                    # Installable Python package
└── README.md                   # Project overview & docs



How Everything Works
The Testing Flow
1. Load AI Model (GPT-2)
      ↓
2. Give it a prompt ("Write a greeting")
      ↓
3. Get response ("Hello! How are you?")
      ↓
4. Evaluate response:
   - Length: Is it 5-20 words? ✓
   - Quality: Has punctuation? ✓
   - Meaning: Matches expected? ✓
      ↓
5. Save results to JSON file
      ↓
6. Generate HTML dashboard
Core Concepts
Evaluators
Each evaluator checks one aspect:
python# Length Evaluator
evaluator = LengthEvaluator(min_words=5, max_words=20)
result = evaluator.evaluate("This is my response")
# Returns: {"passed": True, "word_count": 4}

# Quality Evaluator  
evaluator = QualityEvaluator()
result = evaluator.evaluate("This is good text.")
# Checks: punctuation, capitals, repetition, etc.

# Semantic Evaluator
evaluator = SemanticSimilarityEvaluator()
result = evaluator.evaluate(
    response="Paris is the capital",
    expected="The capital is Paris"
)
# Returns: {"similarity_score": 0.95, "passed": True}
Results Manager
Saves everything with timestamps:
pythonmanager = ResultsManager("results")
manager.save_result("test_name", evaluation_data)
# Creates: results/test_name_20240115_143022.json
Test Runner
Combines multiple evaluators:
pythonrunner = SimpleTestRunner([length_eval, quality_eval])
results = runner.run_test(prompt, response)
# Runs all evaluators and combines results
Problems I Faced and Solutions
Problem 1: "ModuleNotFoundError: No module named 'llm_test_suite'"
Cause: Python couldn't find my code
What I tried first: Adding sys.path.insert(0, 'src')
Better solution:
bashpip install -e .
Why this works: Installs your package in "editable" mode
Problem 2: "TypeError: Object of type bool_ is not JSON serializable"
Cause: NumPy types can't be saved to JSON
Where: In semantic.py when saving results
Solution:
python# Convert NumPy types to Python types
'passed': bool(passed),
'score': float(similarity_score)
Problem 3: GPT-2 Always Generates Too Much Text
Cause: Default settings generate 50+ tokens
Symptoms: All length tests failed
Solutions:

Reduce max_new_tokens from 50 to 15
Adjust evaluator thresholds (max_words: 30 instead of 20)
Use prompts that encourage short answers

Problem 4: "The current process just got forked" Warning
Cause: Tokenizers library parallel processing issue
Solution: Add to top of scripts:
pythonimport os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
Problem 5: Semantic Tests All Failed
Cause: GPT-2 doesn't answer questions well
Example:

Prompt: "What is the capital of France?"
Expected: "The capital of France is Paris"
Got: "France has a very important role..."
Solutions:


Use completion prompts instead of questions
Lower similarity threshold (0.6 instead of 0.8)
Use better models for factual tasks

Problem 6: Browser Can't Open Dashboard
Cause: file:// path issues
Error: "This site can't be reached"
Solution: Use absolute path:
pythonimport os
abs_path = os.path.abspath("results/dashboard.html")
webbrowser.open(f"file://{abs_path}")
Problem 7: Imports Not Recognized in VS Code
Cause: Pylance doesn't know about project structure
Visual: Red squiggly lines under imports
Solution: Create .vscode/settings.json:
json{
    "python.analysis.extraPaths": ["./src"]
}
Usage Examples
Basic Length Test
pythonfrom llm_test_suite.evaluators.length import LengthEvaluator
from transformers import pipeline

# Load model
model = pipeline("text-generation", model="gpt2")

# Create evaluator
evaluator = LengthEvaluator(min_words=5, max_words=20)

# Generate and evaluate
result = model("Hello, my name is", max_new_tokens=15)
evaluation = evaluator.evaluate(result[0]['generated_text'])

print(evaluation['message'])  # "Good length: 12 words"
Running Complete Test Suite
bash# Run multiple tests and save results
python examples/test_save_results.py

# Compare different models
python examples/compare_models.py

# Generate visual dashboard
python examples/generate_dashboard.py

# Open dashboard in browser
open results/dashboard.html  # Mac
start results/dashboard.html # Windows
Test Results and Outputs
JSON Result File
json{
  "test_id": "test_greeting",
  "test_type": "length",
  "prompt": "Write a greeting:",
  "response": "Hello! How are you today?",
  "metrics": {
    "word_count": 5,
    "min_words": 3,
    "max_words": 20,
    "passed": true
  },
  "timestamp": "20240115_143022",
  "duration": 0.523
}
Console Output
Running Tests and Saving Results
==================================================
Test: greeting
Prompt: Write a short greeting:
Response: Hello! How are you doing today?
Result: ✓ Good length: 6 words
Results saved to: results/test_greeting_20240115.json

Summary: 2/3 tests passed
Dashboard HTML
LLM Test Results Dashboard
Generated: 2024-01-15 14:30:00

Statistics:
- Total Tests: 15
- Passed: 12 (80%)
- Failed: 3 (20%)

[Interactive table with all results]
Model Comparison
Comparing: gpt2 vs distilgpt2

Test: Generate greeting
- gpt2: "Hello! How are you?" (0.31s)
- distilgpt2: "Hello there!" (0.19s)
Winner: distilgpt2 (faster)

Overall:
- gpt2: Better quality, slower
- distilgpt2: Lower quality, 40% faster
What I Learned
Technical Skills Developed

AI/LLM Testing: Understanding evaluation metrics and methodologies
Software Architecture: Modular design and separation of concerns
NLP Techniques: Semantic similarity and text analysis
Framework Development: Building reusable, extensible systems
Data Visualization: Creating meaningful reports and dashboards

Key Achievements

Transformed monolithic code into modular framework
Implemented multiple evaluation strategies
Created automated testing pipeline
Built visual reporting system
Enabled objective model comparison

