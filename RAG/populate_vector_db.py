from argparse import ArgumentParser
from pathlib import Path
from loguru import logger
from utility import milvus_collection_exists, create_milvus_collection
from vector_db import MilvusCollection
import pickle
from tqdm import tqdm
import numpy as np
import data_preprocess



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('collection')
    parser.add_argument('language')
    parser.add_argument('embedding_data_path')
    parser.add_argument('context_data_path')
    args = parser.parse_args()

    embedding_data_path = Path(args.embedding_data_path)
    if not embedding_data_path.is_file():
        raise Exception(f"Dataset {embedding_data_path} does not exist.")
    
    context_data_path = Path(args.context_data_path)
    if not context_data_path.is_file():
        raise Exception(f"Dataset {context_data_path} does not exist.")

    collection_name = args.collection
    language = args.language


    # Read context-to-keywords json file and make keyword-to-contexts mapping
    with open(embedding_data_path, 'rb') as file:
        embeddings = pickle.load(file)
        
    logger.debug(f"Loading embeddings for {embedding_data_path}")
        
    Context_dict = data_preprocess.load_dict(context_data_path)
    data_processed = data_preprocess.preprocess(Context_dict)

    logger.debug(f"Loading context for {context_data_path}")
    


    # Embed all keywords and insert into vector DB
    if not milvus_collection_exists(collection_name):
        create_milvus_collection(collection_name)
    collection = MilvusCollection(collection_name)
    if not collection.has_partition(language):
        collection.create_partition(language)

    logger.debug("Populating partition <" + language + '> in collection <' + collection_name + '>')
    
    
    turn = 0
    for batch in tqdm(np.array_split(data_processed, (len(data_processed)/256) + 1)):
        
        id = batch['id'].tolist()
        sub_id = batch['sub_id'].tolist()
        
        data = [
            {
                'id':id[i],
                'sub_id': sub_id[i],
                'context_embedding': embeddings[turn+i]
            } for i in range(len(id))
        ]
        
        turn += len(batch)
        collection.insert(data=data,partition_name=language)

    

    logger.debug("Partition <" + language + "> in collection <" + collection_name + "> populated")
