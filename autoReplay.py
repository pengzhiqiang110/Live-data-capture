import os.path
import time, shutil
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

import logging
# import sys
# from db import Bot
# import db

# terminal 环境中执行： export OPENAI_API_KEY=sk-xxxx

logger = logging.getLogger('autoReplay')

class AutoRelay(object):
    # 获取当前时间戳
    # timestamp = int(time.time())
    
    def __init__(self, bot = None):
        path_doc_list = ["data/shopname-botid/text", "storage/shopname-botid"]
        if bot != None:
            path_doc_list = bot.get_live_doc_path()
        self.path_text = path_doc_list[0]
        self.path_vector = path_doc_list[1]
        self.tone = "你是一名带货直播间的智能客服,用可爱简洁的语气，严格根据上下文内容回答客户问题，如果上下文没有，信息不够的话,选择模糊回答。回答字数限制在100个字以内"
        self.query_engine = None
        self.bot = bot
        self.update_doc_index()

    def getAutoReplay(self, query):
        response = self.query_engine.query(''.join([query,', ',self.tone]))
        # 确保 response 是字符串类型
        if not isinstance(response, str):
            # 将其转换为字符串
            logging.debug("自动回复: %s", str(response))
        return str(response)

    def newVector(self):
        # load the documents and create the index
        documents = SimpleDirectoryReader(self.path_text).load_data()
        index = VectorStoreIndex.from_documents(documents)
        # store it for later
        index.storage_context.persist(persist_dir=self.path_vector)
        # create the query engine
        self.query_engine = index.as_query_engine()


    def update_doc_index(self):
        # bot live_doc 内容写入 path_text
        path_text =''.join([self.path_text,'/live_doc.txt'])
        # 如果path_text上一级目录不存在，则创建
        if not os.path.exists(os.path.dirname(path_text)):
            os.makedirs(os.path.dirname(path_text))
        if self.bot != None:
            with open(path_text, "w") as f:
                f.write(self.bot.get_live_doc())
        # 如果path_vector下没有文件，则创建新的索引
        self.newVector()
        # if not os.path.exists(self.path_vector):
        #     self.newVector()
        # else:
        #     # load the existing index
        #     storage_context = StorageContext.from_defaults(persist_dir=self.path_vector)
        #     index = load_index_from_storage(storage_context)
        #     # create the query engine
        #     self.query_engine = index.as_query_engine(similarity_top_k=2)
        # self.deleteVector()

    def deleteVector(self):
        # load the existing index
        if not os.path.exists(self.path_vector):
            return
        else:
            # 删除path_vector下的文件
            shutil.rmtree(self.path_vector)
            logging.INFO("删除path_vector下的文件")


if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = "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"
    autoRelay = AutoRelay()
    autoRelay.getAutoReplay("买1送四是什么")
    autoRelay.getAutoReplay("影响我购买的因素有哪些")
    autoRelay.deleteVector()

    if not os.path.exists("./storage/shopname-botid"):
        # load the documents and create the index
        documents = SimpleDirectoryReader("./data/shopname-botid/text").load_data()
        index = VectorStoreIndex.from_documents(documents)
        # store it for later
        index.storage_context.persist()
    else:
        # load the existing index
        storage_context = StorageContext.from_defaults(persist_dir="./storage/shopname-botid")
        index = load_index_from_storage(storage_context)

    # either way we can now query the index
    query_engine = index.as_query_engine()
    response = query_engine.query("买1送四是什么")
    print(response)

