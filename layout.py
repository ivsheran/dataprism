import gradio as gr

CUSTOM_CSS = """
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Mulish:wght@400;500&display=swap');

    h1 { font-family: 'JetBrains Mono', monospace !important; font-size: 32px !important; color: #F8F0E2 !important; margin-top: 24px !important; margin-bottom: 4px !important; }
    p { font-family: 'Mulish', sans-serif !important; font-size: 16px !important; color: #F8F0E2 !important; margin-bottom: 24px !important; }
    label, .label-wrap span { font-family: 'Mulish', sans-serif !important; color: #F8F0E2 !important; }
    button.lg { background-color: #191919 !important; color: #FF5992 !important; font-family: 'JetBrains Mono', monospace !important; border: 1px solid #555555 !important; }
    button.lg.secondary { background-color: transparent !important; color: #F8F0E2 !important; font-family: 'JetBrains Mono', monospace !important; border: 1px solid #555555 !important; }
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
                with gr.Column(scale=2):
                    file_input = gr.File(label="Upload your File", file_types=[".csv", ".json", ".xlsx"], type="filepath")
                with gr.Column(scale=2):
                    status = gr.Textbox(label="Status", interactive=False)

            with gr.Row():
                with gr.Column(scale=2):
                    question_input = gr.Textbox(label="Ask a question about your data", placeholder="Type your question here...", lines=3)
                with gr.Column(scale=2):
                    pass 

            with gr.Row():
                with gr.Column(scale=2):
                    submit_button = gr.Button("Submit")
                with gr.Column(scale=2):
                    pass
            
            with gr.Row():
                with gr.Column():
                    output_chart = gr.Image(label="Answer", interactive=False, visible=False)
                with gr.Column():
                    chat = gr.Chatbot(label="Chat with your data", elem_id="chatbot", visible=False, height=600)

            with gr.Row():
                clear_button = gr.Button(value="Clear Chat", visible=False)
            
            return demo, file_input, status, question_input, submit_button, output_chart, chat, clear_button

        