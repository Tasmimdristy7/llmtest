
class Config:
    
    def __init__(self):
        # Default settings
        self.target_model = "gpt2"
        self.target_device = "cpu"
        self.output_dir = "results"
        
    def get(self, key, default=None):
        """Get configuration value."""
        return getattr(self, key, default)
