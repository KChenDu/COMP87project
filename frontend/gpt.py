from os import environ
from langchain_openai.chat_models import ChatOpenAI
from data.user import OPENAI_API_KEY
from langchain.schema import HumanMessage, AIMessage
from openai import RateLimitError


environ["OPENAI_API_KEY"] = OPENAI_API_KEY  # Set your own API key and don't share it here!
llm = ChatOpenAI(temperature=1.0, model='gpt-3.5-turbo-0613')


def predict(message, history):
    history_langchain_format = [None] * (len(history) * 2 - 1)
    for i, human, ai in enumerate(history[1:]):
        history_langchain_format[i] = HumanMessage(content=human)
        history_langchain_format[i] = AIMessage(content=ai)
    history_langchain_format[-1] = HumanMessage(content=message)
    try:
        gpt_response = llm.invoke(history_langchain_format)
    except RateLimitError:
        return "You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors."
    return gpt_response.content
