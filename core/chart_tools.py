import seaborn as sns
import matplotlib.pyplot as plt
from .config_loader import ConfigLoader
from langchain.tools import tool


class ChartTools:
    def __init__(self, config: ConfigLoader):
        self.config = config
        self.df=None

    def set_dataframe(self, df):
        self.df = df

    def get_tools(self):
        df=self.df

        @tool
        def bar_chart(x_col: str, y_col: str) -> str:
            """Use when user wants to compare values across categories such as regions, products, types. Example: 'Show me a bar chart of sales by region.'"""
            plt.figure(figsize=(10, 6))
            sns.barplot(data=df, x=x_col, y=y_col)
            plt.title(f'Bar Chart of {y_col} by {x_col}')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"{self.config.output_folder_path}bar_chart_{x_col}_{y_col}.png")
            plt.close()
            
            return f"{self.config.output_folder_path}bar_chart_{x_col}_{y_col}.png"
    

        @tool
        def line_chart(x_col: str, y_col: str) -> str:
            """Use when user wants to show trends over time or continuous data. Example: 'Show me a line chart of sales over time.'"""
            plt.figure(figsize=(10, 6))
            sns.lineplot(data=df, x=x_col, y=y_col)
            plt.title(f'Line Chart of {y_col} over {x_col}')
            plt.tight_layout()
            plt.savefig(f"{self.config.output_folder_path}line_chart_{x_col}_{y_col}.png")
            plt.close()

            return f"{self.config.output_folder_path}line_chart_{x_col}_{y_col}.png"

        return [bar_chart, line_chart] 
        


