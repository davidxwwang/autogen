
import os
import sys

sys.path.insert(0, r'C:\Users\xwwan\Documents\GitHub\david-autogen')
print(sys.path)
from autogen.code_utils import content_str
from autogen.io.base import IOStream
from autogen.oai.openai_utils import config_list_from_json
from david_retrieve_user_proxy_agent import DavidRetrieveUserProxyAgent
from david_retrieve_assistant_agent import DavidRetrieveAsistantAgent

import sys

# https://www.chinese-future.org/articles/l24enbs4wh7da95yrtskjl2s73klr7

def get_human_input( prompt: str) -> str:
    iostream = IOStream.get_default()
    reply = iostream.input(prompt)
    return reply

os.environ['AUTOGEN_USE_DOCKER'] = 'False'
config_list = config_list_from_json(env_or_file="C:\\Users\\xwwan\\Documents\\GitHub\\david-autogen\\test\\01_david\\OAI_CONFIG_LIST")



docs_path = ['C:\\Users\\xwwan\\Documents\\GitHub\\david-autogen\\test\\01_david\\files', 
             'https://www.intron-tech.com.cn/article-1461.aspx']
retrieve_config = {'docs_path': docs_path,
                   "model": "gpt-4",
                   "get_or_create": True,
                   "embedding_model":"text-davinci-002",
                   'distance_threshold': 0.99,
                   "db_config": {
                       'metadata':{ 'hnsw:M': 32, 'hnsw:construction_ef': 30, 'hnsw:space': 'cosine' }
                    }
                   }
localRetriever = DavidRetrieveUserProxyAgent(llm_config={"config_list": config_list}, is_termination_msg= (lambda x: content_str(x.get("content")) == "TERMINATE"), retrieve_config=retrieve_config)
retrieveAssistantAgent = DavidRetrieveAsistantAgent(name = 'david', llm_config={"config_list": config_list})

# 英恒科技的boss是谁
problem = 'what is OpenAI relies on Cosmos DB to dynamically scale their ChatGPT service?'
problem = '金脉公司的G表示什么意思？'
problem = 'sidcong'
problem = get_human_input(f"请输入问题: ")

context = {
    'problem': problem, 
    'n_results': 10, 
    'search_string': ''
}
initMessage = DavidRetrieveUserProxyAgent.message_generator(localRetriever, retrieveAssistantAgent, context=context)

rst = localRetriever.initiate_chat(recipient=retrieveAssistantAgent, message=initMessage)

pass