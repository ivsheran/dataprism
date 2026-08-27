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
            agg_df = df.groupby(x_col)[y_col].sum().reset_index()
            sns.barplot(data=agg_df, x=x_col, y=y_col)
            plt.title(f'Bar Chart of {y_col} by {x_col}')
            plt.xticks(rotation=45)
            plt.ticklabel_format(style='plain', axis='y')
            plt.tight_layout()
            filepath = f"{self.config.output_folder_path}bar_chart_{x_col}_{y_col}.png"
            plt.savefig(filepath)
            plt.close()
            
            return f"Chart saved to {filepath}\n\nData plotted:\n{agg_df.to_string(index=False)}"

        @tool
        def line_chart(x_col: str, y_col: str) -> str:
            """Use when user wants to show trends over time or continuous data. Example: 'Show me a line chart of sales over time.'"""
            plt.figure(figsize=(10, 6))
            agg_df = df.groupby(x_col)[y_col].sum().reset_index()
            sns.lineplot(data=agg_df, x=x_col, y=y_col)
            plt.title(f'Line Chart of {y_col} over {x_col}')
            plt.ticklabel_format(style='plain', axis='y')
            plt.tight_layout()
            filepath = f"{self.config.output_folder_path}line_chart_{x_col}_{y_col}.png"
            plt.savefig(filepath)
            plt.close()

            return f"Chart saved to {filepath}\n\nData plotted:\n{agg_df.to_string(index=False)}"
        
        @tool
        def pie_chart(category_column: str, value_column: str) -> str:
            """Use when user wants to show the proportion of different categories. Example: 'Show me a pie chart of market share by technology.'"""
            plt.figure(figsize=(8, 8))
            data = df.groupby(category_column)[value_column].sum().reset_index()
            plt.pie(data[value_column], labels=data[category_column], autopct='%1.1f%%', startangle=140)
            plt.title(f'Pie Chart of {value_column} by {category_column}')
            plt.tight_layout()
            filepath = f"{self.config.output_folder_path}pie_chart_{category_column}_{value_column}.png"
            plt.savefig(filepath)
            plt.close()

            return f"Chart saved to {filepath}\n\nData plotted:\n{data.to_string(index=False)}"
        
        @tool
        def scatter_plot(x_col: str, y_col: str) -> str:
            """Use when user wants to show the relationship between two numeric variables. Example: 'Show me a chart showing correlation between sales and advertising spend.'"""
            plt.figure(figsize=(10, 6))
            corr_coeff = df[x_col].corr(df[y_col])           
            sns.scatterplot(data=df, x=x_col, y=y_col)
            plt.title(f'Correlation of {y_col} vs. {x_col}')
            plt.ticklabel_format(style='plain', axis='y')
            plt.tight_layout()
            filepath = f"{self.config.output_folder_path}scatter_plot_{x_col}_{y_col}.png"
            plt.savefig(filepath)
            plt.close()

            return f"Chart saved to {filepath}\n\nCorrelation coefficient: {corr_coeff:.2f}"
        
        @tool
        def histogram(column: str) -> str:
            """Use when user wants to show the distribution of a single numeric variable. Example: 'Show distribution of salaries.'"""
            plt.figure(figsize=(10, 6))
            distrib = df[column].describe()
            sns.histplot(data=df, x=column, kde=True)
            plt.title(f'Histogram of {column}')
            plt.tight_layout()
            filepath = f"{self.config.output_folder_path}histogram_{column}.png"
            plt.savefig(filepath)
            plt.close()

            return f"Chart saved to {filepath}\n\nDescriptive statistics:\n{distrib.to_string()}"
        
        @tool
        def box_plot(x_col: str, y_col: str) -> str:
            """Use when user wants to show the distribution, spread, and outliers of a numeric variable. Example: 'Show me median sales by region.'"""
            plt.figure(figsize=(10, 6))
            distrib_by_group = df.groupby(x_col)[y_col].describe()
            sns.boxplot(data=df, x=x_col, y=y_col)
            plt.title(f'Box Plot of {y_col} by {x_col}')
            plt.xticks(rotation=45)
            plt.ticklabel_format(style='plain', axis='y')
            plt.tight_layout()
            filepath = f"{self.config.output_folder_path}box_plot_{x_col}_{y_col}.png"
            plt.savefig(filepath)
            plt.close()

            return f"Chart saved to {filepath}\n\nDescriptive statistics by group:\n{distrib_by_group.to_string()}"
        
        @tool
        def heatmap() -> str:
            """Use when user wants to see correlations between all numeric variables in the dataset. Example: 'Show me a heatmap of correlations.'"""
            plt.figure(figsize=(10, 8))
            corr_matrix = df.select_dtypes(include='number').corr()
            sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True, square=True)
            plt.title('Correlation Heatmap')
            plt.tight_layout()
            filepath = f"{self.config.output_folder_path}heatmap.png"
            plt.savefig(filepath)
            plt.close()

            return f"Chart saved to {filepath}\n\nCorrelation matrix:\n{corr_matrix.to_string()}"
        
        @tool
        def grouped_bar_chart(category_column: str, value_columns: list[str]) -> str:
             """Use when user wants to compare two related metrics side by side across categories. Example: 'Compare sales and profit by region.'"""
             plt.figure(figsize=(10, 6))
             group_cat = df.groupby(category_column)[value_columns].sum().reset_index()
             melted = group_cat.melt(id_vars=category_column, value_vars=value_columns, var_name='Metric', value_name='Value')
             sns.barplot(data=melted, x=category_column, y='Value', hue='Metric')
             plt.title(f'{value_columns[0]} and {value_columns[1]} by {category_column}')
             plt.xticks(rotation=45)
             plt.tight_layout()
             filepath = f"{self.config.output_folder_path}grouped_bar_chart_{category_column}_{value_columns[0]}_{value_columns[1]}.png"
             plt.savefig(filepath)
             plt.close()

             return f"Chart saved to {filepath}\n\nData plotted:\n{group_cat.to_string()}"
        
        @tool
        def aggregate_data(group_by_column: str, metric_column: str, agg_func: str) -> str:
            """Group the dataset by group_by_column and aggregate the metric_column using a specified aggregation function (sum, mean, median, max, min). 
            Example: 'Aggregate sales by region using sum.'
            Return exact values sorted from highest to lowest. 
            Use this tool to answer any question about totals, comparisons, aggregates or rankings by category - do not estimate from memory."""
            if group_by_column not in df.columns:
                return f"Invalid group_by_column: {group_by_column}. Valid columns are: {', '.join(df.columns)}."
            if metric_column not in df.columns:
                return f"Invalid metric_column: {metric_column}. Valid columns are: {', '.join(df.columns)}."
            if agg_func not in ['sum', 'mean', 'median', 'max', 'min']:
                return f"Invalid aggregation function: {agg_func}. Please use one of the following: sum, mean, median, max, min."

            result = df.groupby(group_by_column)[metric_column].agg(agg_func).reset_index().sort_values(by=metric_column, ascending=False)
            return f"Aggregated data:\n{result.to_string(index=False)}"
        
        return [bar_chart, line_chart, pie_chart, scatter_plot, histogram, box_plot, heatmap, grouped_bar_chart, aggregate_data] 
    