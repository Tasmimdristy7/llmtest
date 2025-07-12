import json
import os
from datetime import datetime
from pathlib import Path


class DashboardGenerator:
    
    def __init__(self, results_dir="results"):
        self.results_dir = results_dir
        
    def generate_dashboard(self):
        # Find all JSON files
        json_files = list(Path(self.results_dir).glob("*.json"))
        
        if not json_files:
            return None
        
        # Load all results
        all_results = []
        for json_file in json_files:
            with open(json_file, 'r') as f:
                data = json.load(f)
                data['filename'] = json_file.name
                all_results.append(data)
        
        # Sort by timestamp (newest first)
        all_results.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        # Generate HTML
        html = self._generate_html(all_results)
        
        # Save dashboard
        dashboard_path = os.path.join(self.results_dir, "dashboard.html")
        with open(dashboard_path, 'w') as f:
            f.write(html)
        
        print(f"✅ Dashboard generated: {dashboard_path}")
        return dashboard_path
    
    def _generate_html(self, results):
        """Generate the HTML content."""
        # Count statistics
        total_tests = len(results)
        passed_tests = sum(1 for r in results if r.get('passed', False))
        failed_tests = total_tests - passed_tests
        
        # Generate HTML
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>LLM Test Results Dashboard</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #333;
            color: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .stats {{
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-box {{
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            flex: 1;
            text-align: center;
        }}
        .stat-number {{
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .passed {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .total {{ color: #007bff; }}
        .results-table {{
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            background-color: #f8f9fa;
            padding: 12px;
            text-align: left;
            border-bottom: 2px solid #dee2e6;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #dee2e6;
        }}
        tr:hover {{
            background-color: #f8f9fa;
        }}
        .pass-badge {{
            background-color: #28a745;
            color: white;
            padding: 4px 8px;
            border-radius: 3px;
            font-size: 12px;
        }}
        .fail-badge {{
            background-color: #dc3545;
            color: white;
            padding: 4px 8px;
            border-radius: 3px;
            font-size: 12px;
        }}
        .timestamp {{
            color: #6c757d;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 LLM Test Results Dashboard</h1>
        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <div class="stat-number total">{total_tests}</div>
            <div>Total Tests</div>
        </div>
        <div class="stat-box">
            <div class="stat-number passed">{passed_tests}</div>
            <div>Passed</div>
        </div>
        <div class="stat-box">
            <div class="stat-number failed">{failed_tests}</div>
            <div>Failed</div>
        </div>
    </div>
    
    <div class="results-table">
        <table>
            <thead>
                <tr>
                    <th>Test Name</th>
                    <th>Status</th>
                    <th>Message</th>
                    <th>Timestamp</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # Add each result
        for result in results:
            status = "PASS" if result.get('passed', False) else "FAIL"
            badge_class = "pass-badge" if result.get('passed', False) else "fail-badge"
            message = result.get('message', 'No message')
            timestamp = result.get('timestamp', 'N/A')
            test_name = result.get('test_name', result.get('filename', 'Unknown'))
            
            # Extract details
            details = []
            if 'word_count' in result:
                details.append(f"Words: {result['word_count']}")
            if 'prompt' in result:
                details.append(f"Prompt: {result['prompt'][:30]}...")
            
            html += f"""
                <tr>
                    <td><strong>{test_name}</strong></td>
                    <td><span class="{badge_class}">{status}</span></td>
                    <td>{message}</td>
                    <td class="timestamp">{timestamp}</td>
                    <td>{' | '.join(details)}</td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""
        
        return html