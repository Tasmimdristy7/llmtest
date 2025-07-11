from llm_test_suite.reporting.dashboard import DashboardGenerator
import os

# Create dashboard generator
generator = DashboardGenerator("results")

# Generate the dashboard
dashboard_path = generator.generate_dashboard()

if dashboard_path:
    # Get absolute path
    abs_path = os.path.abspath(dashboard_path)
    
    print(f"\n🎉 Dashboard ready!")
    print(f"Open in your browser: file://{abs_path}")
    
    # Try to open in browser automatically
    import webbrowser
    try:
        webbrowser.open(f"file://{abs_path}")
        print("Opening in browser...")
    except:
        print("Please open the file manually in your browser")