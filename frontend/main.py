import gradio as gr

from gradio import Group, Row, Image
from utils import disable_submit_button, submit, enable_submit_button
from bots import streaming_bot as bot


with open('sources/style.css') as file:
    css = file.read()


with gr.Blocks(css=css) as demo:
    with Group():
        with Row():
            height = 150
            Image('sources/UCL-logo.webp', height=height, show_label=False, show_download_button=False, scale=3)
            Image('sources/mix.png', height=height, show_label=False, show_download_button=False, scale=1)

    with Group():
        chatbot = gr.Chatbot([(None, "Hi! How can I help you?")], height=600)
        with Row():
            message = gr.Textbox(placeholder="Type your question here...", label='Question:', scale=4)
            with gr.Column(scale=1):
                submit_button = gr.Button('Submit', variant='primary')
                gr.ClearButton(message)

    message.submit(disable_submit_button, outputs=submit_button, queue=False) \
        .then(submit, [message, chatbot], [message, chatbot], queue=False) \
        .then(bot, chatbot, chatbot) \
        .then(enable_submit_button, outputs=submit_button, queue=False)
    submit_button.click(disable_submit_button, outputs=submit_button, queue=False) \
        .then(submit, [message, chatbot], [message, chatbot], queue=False) \
        .then(bot, chatbot, chatbot) \
        .then(enable_submit_button, outputs=submit_button, queue=False)


if __name__ == '__main__':
    demo.queue().launch()
