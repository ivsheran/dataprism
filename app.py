import gradio as gr

from core.config_loader import ConfigLoader
from core.data_loader import DataLoader
from core.chart_tools import ChartTools
from core.visualization_agent import VisualizationAgent
from layout import GradioLayout

def _init_components():
    config = ConfigLoader()
    chart_tools = ChartTools(config)
    data_loader = DataLoader(config)
    visualization_agent = VisualizationAgent(config, chart_tools, data_loader)
    return config, chart_tools, data_loader, visualization_agent

def main():
    config, chart_tools, data_loader, visualization_agent = _init_components()
    demo, file_input, status, question_input, submit_button, output_chart, chat, clear_button = GradioLayout().create_layout()

    with demo:
        def handle_upload(file):
            if file is None:
                return "No dataset uploaded."
            try:
                data_loader.load_file(file)
                chart_tools.set_dataframe(data_loader.df)
                return "Dataset loaded successfully!"
            except Exception as e:
                return f"Error loading dataset: {str(e)}"

        file_input.upload(handle_upload, inputs=[file_input], outputs=[status])

        def handle_question(question, history):
            if history is None:
                history = []
            if question is None or question.strip() == "":
                return history, None, gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
            
            try:
                response, chart_path = visualization_agent.run(question, session_id="dataprism_session")
                history.append({"role": "user", "content": question})
                history.append({"role": "assistant", "content": response})

                if chart_path:
                    return history, chart_path, gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)
                else:
                    return history, gr.update(), gr.update(), gr.update(visible=True), gr.update(visible=True)

            except Exception as e:
                history.append({"role": "assistant", "content": f"Error: {str(e)}"})
                return history, None, gr.update(visible=False), gr.update(visible=True), gr.update(visible=True)

        submit_button.click(handle_question, inputs=[question_input, chat], outputs=[chat, output_chart, output_chart, chat, clear_button])

        def handle_clear_chat():
            history = []
            return history, "", None, gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

        clear_button.click(handle_clear_chat, inputs=[], outputs=[chat, question_input, output_chart, output_chart, chat, clear_button])
    
    demo.launch()

if __name__ == "__main__":
    main()

