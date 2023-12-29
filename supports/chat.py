#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/12/26 14:15
Author  : ren
"""
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate

import config  # noqa

# from langchain_core.tools import Tool
# from serpapi.baidu_search import BaiduSearch
# from langchain_community.utilities.serpapi import SerpAPIWrapper

# search = SerpAPIWrapper(
#     serpapi_api_key=config.SERP_API_KEY,
#     search_engine=BaiduSearch
# )
#
# tools = [
#     Tool(
#         name="Current Search",
#         func=search.run,
#         description="useful for when you need to answer questions about current events or the current state of the world"
#     ),
# ]
#
# SYS = "你是一个ai聊天助手. 你的名字叫做 小一. 你非常健谈,并且能够从历史聊天中提取很多信息. 如果你不知道怎么回答问题,就会说“对不起,超出我的认知了”"
# HUMAN = "{input}"

llm = ChatOpenAI(temperature=0, openai_api_key=config.OPENAI_KEY, verbose=True)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "你是一个ai聊天助手. 你的名字叫做 小一. 你非常健谈,并且能够从历史聊天中提取很多信息. 如果你不知道怎么回答问题,就会说“对不起,超出我的认知了”. 你的位置是中国深圳"),
    ("human", "你好!"),
    ("ai", "你好呀!"),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])


# prompt = prompt.partial(
#     name="Ren"
# )


class OpenAIChat:
    def __init__(self, userid):
        self.uid = userid
        self.chain = ConversationChain(
            llm=llm,
            verbose=True,
            memory=self.memory,
            prompt=prompt,
        )

    def predict(self, question):
        return self.chain.predict(input=question)
        # 如果需要搜索功能使用下面的
        # agent = ConversationalChatAgent.from_llm_and_tools(llm=llm, tools=tools, system_message=SYS)
        # agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, memory=self.memory)
        # agent_chain.verbose = True
        # agent_chain.handle_parsing_errors = True
        #
        # return agent_chain.run(question)

    @property
    def history(self):
        history = SQLChatMessageHistory(
            session_id=self.uid,
            connection_string=config.DB_URL,
            # session_id_field_name="user_id"
        )
        return history

    @property
    def memory(self):
        return ConversationBufferMemory(
            return_messages=True,
            chat_memory=self.history,
            memory_key="chat_history"
        )


if __name__ == '__main__':
    chat = OpenAIChat("xxxx-sid")
    t = chat.predict("你说的都对")
    print(t)
