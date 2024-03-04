import sys

from towhee import AutoConfig, AutoPipes
from cohere import Client
sys.path.insert(1, '../DB')
from vector_db import MilvusCollection
from setting import METRIC_TYPE
from relational_db import SQLiteDB
from os import chdir


co = Client('Y0zL0EiA9HyasDgJxWatSJ0QtjQ14fGU5O6drzWU')

chdir('../DB')
sqlite_db = SQLiteDB('MLQA_context')
chdir('../frontend')
config = AutoConfig.load_config('sentence_embedding')
config.model = 'average_word_embeddings_glove.6B.300d'
sentence_embedding = AutoPipes.pipeline('sentence_embedding', config=config)


search_params = {
    "metric_type": METRIC_TYPE,
    "params": {
        # search for vectors with a distance greater than 0.8
        "radius": 0.8
    }
}

collection = MilvusCollection('MLQA_BART_keywords')


def streaming_bot(history):
    if history[-1][0] is None or history[-1][1] is not None:
        yield history
        return
    query = history[-1][0]
    history[-1][-1] = 'I received your query "' + query + '". Let me find an answer for you!\nRetrieving documents...'
    yield history

    search_result = collection.search(sentence_embedding(query).get(), "embedding", search_params, 3,
                                      partition_names=['en'], output_fields=["context_ids"])[0]

    contexts = []
    chdir('../DB')
    for hit in search_result:
        for context_id in hit.context_ids:
            contexts.append(sqlite_db.select(['context'], 'en', f'id = {context_id}')[0][0])
    chdir('../frontend')

    length = len(contexts)
    if length < 1:
        history[-1][-1] += f"\nI haven't found any document related to your question."
        yield history
        return
    if length < 2:
        history[-1][-1] += f'\nI found {length} document for you. Let me now try to extract the answer for your question...'
    else:
        history[-1][-1] += f'\nI found {length} documents for you. Let me now extract the answer for your question...'
    yield history

    prompt = 'Answer the question: "' + query + '" Using the following contexts:'

    for i, context in enumerate(contexts):
        prompt += f'\n{i + 1}: "' + context + '"'

    history[-1][-1] += '\n' + co.generate(prompt)[0][1:]

    for i, context in enumerate(contexts):
        history[-1][-1] += f'<details><summary>reference {i + 1}</summary>{context}</details>'
        yield history
