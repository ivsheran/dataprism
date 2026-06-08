import pandas as pd
from core.config_loader import ConfigLoader

class DataLoader:
    def __init__(self, config: ConfigLoader):
        self.config = config
        self.sample_rows = config.summary_sample_rows
        self.df = None

    def load_csv(self, file_path):
        self.df = pd.read_csv(file_path)
        return self.df


    def get_summary(self):
        if self.df is None:
            raise ValueError("No data loaded. Please load a dataset first.")
        
        rows, cols = self.df.shape
        summary = f"Dataset: {rows} rows, {cols} columns\n\n"
        summary += f"Columns and types:\n{self.df.dtypes}\n\n"
        summary += f"Sample rows:\n{self.df.head(self.sample_rows)}\n\n"
        summary += f"Statistics:\n{self.df.describe()}\n\n"
        return summary

