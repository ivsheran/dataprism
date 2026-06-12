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
        
        @tool
        def pie_chart(category_column: str, value_column: str) -> str:
            """Use when user wants to show the proportion of different categories. Example: 'Show me a pie chart of market share by technology.'"""
            plt.figure(figsize=(8, 8))
            data = df.groupby(category_column)[value_column].sum().reset_index()
            plt.pie(data[value_column], labels=data[category_column], autopct='%1.1f%%', startangle=140)
            plt.title(f'Pie Chart of {value_column} by {category_column}')
            plt.tight_layout()
            plt.savefig(f"{self.config.output_folder_path}pie_chart_{category_column}_{value_column}.png")
            plt.close()

            return f"{self.config.output_folder_path}pie_chart_{category_column}_{value_column}.png"
        
        @tool
        def scatter_plot(x_col: str, y_col: str) -> str:
            """Use when user wants to show the relationship between two numeric variables. Example: 'Show me a chart showing correlation between sales and advertising spend.'"""
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=df, x=x_col, y=y_col)
            plt.title(f'Correlation of {y_col} vs. {x_col}')
            plt.tight_layout()
            plt.savefig(f"{self.config.output_folder_path}scatter_plot_{x_col}_{y_col}.png")
            plt.close()

            return f"{self.config.output_folder_path}scatter_plot_{x_col}_{y_col}.png"
        
        @tool
        def histogram(column: str) -> str:
            """Use when user wants to show the distribution of a single numeric variable. Example: 'Show distribution of salaries.'"""
            plt.figure(figsize=(10, 6))
            sns.histplot(data=df, x=column, kde=True)
            plt.title(f'Histogram of {column}')
            plt.tight_layout()
            plt.savefig(f"{self.config.output_folder_path}histogram_{column}.png")
            plt.close()

            return f"{self.config.output_folder_path}histogram_{column}.png"
        
        @tool
        def box_plot(x_col: str, y_col: str) -> str:
            """Use when user wants to show the distribution, spread, and outliers of a numeric variable. Example: 'Show me median sales by region.'"""
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=df, x=x_col, y=y_col)
            plt.title(f'Box Plot of {y_col} by {x_col}')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"{self.config.output_folder_path}box_plot_{x_col}_{y_col}.png")
            plt.close()

            return f"{self.config.output_folder_path}box_plot_{x_col}_{y_col}.png"
        
        @tool
        def heatmap() -> str:
            """Use when user wants to see correlations between all numeric variables in the dataset. Example: 'Show me a heatmap of correlations.'"""
            plt.figure(figsize=(10, 8))
            sns.heatmap(df.select_dtypes(include='number').corr(), annot=True)
            plt.title('Correlation Heatmap')
            plt.tight_layout()
            plt.savefig(f"{self.config.output_folder_path}heatmap.png")
            plt.close()

            return f"{self.config.output_folder_path}heatmap.png"
        
        @tool
        def grouped_bar_chart(category_column: str, value_columns: list[str]) -> str:
             """Use when user wants to compare two related metrics side by side across categories. Example: 'Compare sales and profit by region.'"""
             plt.figure(figsize=(10, 6))
             sns.barplot(data=df, x=category_column, y=value_columns[0], hue=value_columns[1])
             plt.title(f'{value_columns[0]} and {value_columns[1]} by {category_column}')
             plt.xticks(rotation=45)
             plt.tight_layout()
             plt.savefig(f"{self.config.output_folder_path}grouped_bar_chart_{category_column}_{value_columns[0]}_{value_columns[1]}.png")
             plt.close()
             
             return f"{self.config.output_folder_path}grouped_bar_chart_{category_column}_{value_columns[0]}_{value_columns[1]}.png"
        
        return [bar_chart, line_chart, pie_chart, scatter_plot, histogram, box_plot, heatmap, grouped_bar_chart] 
    