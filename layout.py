import gradio as gr

CUSTOM_CSS = """
    button[role="tab"] { color: #F8F0E2 !important; font-family: 'JetBrains Mono', monospace !important; background-color: transparent !important; font-size: 15px !important; padding: 10px 20px !important; }
    button[role="tab"]:hover { color: #FF5992 !important; }
    button[role="tab"][aria-selected="true"] { border-bottom: 2px solid #FF5992 !important; color: #FF5992 !important; }
    button.lg { background-color: #191919 !important; color: #FF5992 !important; font-family: 'JetBrains Mono', monospace !important; border: 1px solid #555555 !important; }
    button.lg.secondary { background-color: transparent !important; color: #F8F0E2 !important; border: 1px solid #555555 !important; font-family: 'JetBrains Mono', monospace !important; }
    label, .label-wrap span { color: #F8F0E2 !important; font-family: 'Mulish', sans-serif !important; }
    .tabs { margin-top: 16px !important; }
"""

class GradioLayout:
    def __init__(self, title: str = "DataPrism", description: str = "", theme: str = "default"):
        self.title = title
        self.description = description
        self.theme = theme

    def create_layout(self):
        with gr.Blocks(css=CUSTOM_CSS) as demo:
            gr.Markdown(f"# {self.title}")
            gr.Markdown("Visuallize your data with natual language prompts.")

            with gr.Row():
                file_input = gr.File(
                    label="Upload your File",
                    file_types=[".csv", ".json", ".xlsx"], 
                    type="filepath"
                    )
                status = gr.Textbox(label="Status", interactive=False)

            with gr.Row():
                question_input = gr.Textbox(label="Ask a question about your data", placeholder="Type your question here...")
                submit_button = gr.Button("Submit")
            
            with gr.Row():
                with gr.Column():
                    output_chart = gr.Image(label="Answer", interactive=False, visible=False)
                with gr.Column():
                    chat = gr.Chatbot(label="Chat with your data", elem_id="chatbot", visible=False)

            with gr.Row():
                clear_button = gr.Button(value="Clear Chat", visible=False)
            
            return demo, file_input, status, question_input, submit_button, output_chart, chat, clear_button

        