import gradio as gr

from gradio import Row
# from gpt import predict


def respond(message, chat_history):
    bot_message = "I'm sorry, I don't understand."
    chat_history.append((message, bot_message))
    return None, chat_history


with gr.Blocks() as demo:
    with Row():
        height = 150
        gr.Image('ucl-logo.webp', height=height, show_label=False, show_download_button=False, scale=3)
        gr.Image('dog.webp', height=height, show_label=False, show_download_button=False, scale=1)
    with gr.Group():
        chatbot = gr.Chatbot(height=600)
        with Row():
            msg = gr.Textbox(scale=4)
            with gr.Column(scale=1):
                submit_button = gr.Button('Submit', variant='primary')
                clear_button = gr.ClearButton(msg)
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    submit_button.click(respond, [msg, chatbot], [msg, chatbot])


if __name__ == '__main__':
    '''
    gr.ChatInterface(predict,
                     chatbot=gr.Chatbot([(None, "Hi! How can I help you?")]),
                     examples=["Hello.", "Hello!", "How are you?"],
                     title='XOR Assistant',
                     description="Type your question and get response from the chatbot based on cross-lingual knowledge base!",
                     retry_btn=None,
                     undo_btn=None).launch()
    '''
    demo.launch()
