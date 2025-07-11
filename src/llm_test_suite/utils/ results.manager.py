# src/llm_test_suite/utils/results_manager.py
"""Simple results manager to save test results."""

import json
import os
from datetime import datetime


class ResultsManager:
    """Handles saving test results to files."""
    
    def __init__(self, results_dir="results"):
        """
        Initialize results manager.
        
        Args:
            results_dir: Where to save results
        """
        self.results_dir = results_dir
        # Create directory if it doesn't exist
        os.makedirs(results_dir, exist_ok=True)
    
    def save_result(self, test_name, evaluation_result):
        """
        Save a single test result.
        
        Args:
            test_name: Name of the test
            evaluation_result: Dictionary with test results
        """
        # Create timestamp for unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create filename
        filename = f"{test_name}_{timestamp}.json"
        filepath = os.path.join(self.results_dir, filename)
        
        # Add timestamp to results
        evaluation_result['timestamp'] = timestamp
        evaluation_result['test_name'] = test_name
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(evaluation_result, f, indent=2)
        
        print(f"✅ Results saved to: {filepath}")
        return filepath
    
    def save_multiple_results(self, test_name, all_results):
        """
        Save multiple test results in one file.
        
        Args:
            test_name: Name of the test suite
            all_results: List of result dictionaries
        """
        # Create timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create filename
        filename = f"{test_name}_suite_{timestamp}.json"
        filepath = os.path.join(self.results_dir, filename)
        
        # Create summary
        summary = {
            'test_name': test_name,
            'timestamp': timestamp,
            'total_tests': len(all_results),
            'passed': sum(1 for r in all_results if r.get('passed', False)),
            'failed': sum(1 for r in all_results if not r.get('passed', True)),
            'results': all_results
        }
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f" Test suite results saved to: {filepath}")
        return filepath