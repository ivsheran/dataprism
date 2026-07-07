import pandas as pd
import os
from core.config_loader import ConfigLoader

class DataLoader:
    def __init__(self, config: ConfigLoader):
        self.config = config
        self.sample_rows = config.summary_sample_rows
        self.df = None

    def load_file(self, file_path):
        _, ext = os.path.splitext(file_path)
        if ext.lower() == ".csv":
            self.df = pd.read_csv(file_path)
        elif ext.lower() == ".json":
            self.df = pd.read_json(file_path)
        elif ext.lower() == ".xlsx":
            self.df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}. Please upload a CSV, JSON, or XLSX file.")
        return self.df    
    
    def get_summary(self):
        if self.df is None:
            raise ValueError("No data loaded. Please load a dataset first.")
    
        pd.options.display.float_format = '{:,.2f}'.format
    
        rows, cols = self.df.shape
        summary = f"Dataset: {rows} rows, {cols} columns\n\n"
        summary += f"Columns and types:\n{self.df.dtypes}\n\n"
        summary += f"Sample rows:\n{self.df.head(self.sample_rows)}\n\n"
        summary += f"Statistics:\n{self.df.describe()}\n\n"
    
        num_cols = self.config.metric_columns
    
        cat_cols = [col for col in self.df.select_dtypes(include='object').columns
                if self.df[col].nunique() < 20]
    
        for cat_col in cat_cols:
            agg = self.df.groupby(cat_col)[num_cols].sum().round(2)
            total = agg.sum()
            summary += f"\n{cat_col} breakdown (sum, sorted by value):\n"
            summary += f"{agg.sort_values(by=num_cols[0], ascending=False)}\n"
            summary += f"Total: {total.to_dict()}\n"
    
        return summary