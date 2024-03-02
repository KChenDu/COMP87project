import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd

def load_dict(file_context):
    with open(file_context, 'r') as f:
        dict = json.load(f)
    return dict


def load_context(Context_dict):
    context = []
    context_id = []
    for data in Context_dict:
        context.append(data['context'])
        context_id.append(data['id'])
    return context,context_id

def load_query(Query_dict):
    query = []
    query_context_id = []
    for data in Query_dict:
        query.append(data['title']+':'+data['question'])
        query_context_id.append(data['context_id'])
    return query,query_context_id



def preprocess(data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 512,
        chunk_overlap  = 64,
        length_function = len
    )
    data_split = []
    sub_context_id = 0
    for i in range(len(data)):
        texts = text_splitter.split_text(data[i]['context'])
        for text in texts:
            dic = {}
            dic['id'] = sub_context_id
            dic['sub_id'] = i
            dic['context'] = text
            sub_context_id+=1
            data_split.append(dic)
        
    return pd.DataFrame(data_split)