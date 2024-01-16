import gradio as gr

from gpt import predict


if __name__ == '__main__':
    gr.ChatInterface(predict,
                     chatbot=gr.Chatbot([(None, "Hi! How can I help you?")]),
                     examples=["Hello.", "Hello!", "How are you?"],
                     title='XOR Assistant',
                     description="Type your question and get response from the chatbot based on cross-lingual knowledge base!",
                     retry_btn=None,
                     undo_btn=None).launch()
