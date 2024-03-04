import fasttext

from argparse import ArgumentParser
from pathlib import Path
from json import load
from loguru import logger
from utility import milvus_collection_exists, create_milvus_collection
from vector_db import MilvusCollection
from towhee import AutoConfig, AutoPipes
from tqdm import tqdm


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('collection')
    parser.add_argument('language')
    parser.add_argument('data_path')
    args = parser.parse_args()

    data_path = Path(args.data_path)
    if not data_path.is_file():
        raise Exception(f"Dataset {data_path} does not exist.")

    collection_name = args.collection
    language = args.language

    keyword2context = {}

    # Read context-to-keywords json file and make keyword-to-contexts mapping
    with open(data_path, 'r') as f:
        data = load(f)

    logger.debug(f"Creating keyword-to-contexts mapping for {data_path}")

    for datum in data:
        for keyword in datum['keywords']:
            if keyword in keyword2context:
                keyword2context[keyword].append(datum['id'])
            else:
                keyword2context[keyword] = [datum['id']]

    logger.debug("Keyword-to-contexts mapping created")

    # Embed all keywords and insert into vector DB
    if not milvus_collection_exists(collection_name):
        create_milvus_collection(collection_name)
    collection = MilvusCollection(collection_name)
    if not collection.has_partition(language):
        collection.create_partition(language)

    logger.debug("Populating partition <" + language + "> in collection <" + collection_name + '>')

    if language == 'en':
        config = AutoConfig.load_config('sentence_embedding')
        config.model = 'average_word_embeddings_glove.6B.300d'
        sentence_embedding = AutoPipes.pipeline('sentence_embedding', config=config)

        keywords = list(keyword2context.keys())
        collection.insert([keywords,
                           [embedding.get()[0] for embedding in sentence_embedding.batch(keywords)],
                           list(keyword2context.values())], language)
    elif language == 'zh':
        ft = fasttext.load_model('../data/cc.zh.300.bin')

        for keyword, contexts in tqdm(keyword2context.keys()):
            collection.insert([[keyword],
                               [ft.get_word_vector(keyword)],
                               [contexts]], language)
    else:
        raise NotImplementedError

    logger.debug("Partition <" + language + "> in collection <" + collection_name + "> populated")
