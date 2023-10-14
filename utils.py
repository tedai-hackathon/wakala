import os
from typing import Any
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.agents import initialize_agent, AgentType
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from dotenv import load_dotenv
load_dotenv()

def get_vectortool():
    loader = CSVLoader(file_path="./data/animals_prices.csv")
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
    all_splits = text_splitter.split_documents(data)
    vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())
    vector_tool = create_retriever_tool(vectorstore.as_retriever(), "search_market_price_vectorstore", "Searches and retrieves market information.")
    return vector_tool

def get_market_agent(tools):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = ChatOpenAI(model='gpt-4')
    prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(
                    # "You are a nice chatbot having a conversation with a human."
                    template
                ),
                # The `variable_name` here is what must align with memory
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}")
            ]
        )
    agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, memory=memory, verbose=True, prompt=prompt)

    return agent

template = """
Your name is Wakala.  You are an AI-powered agricultural broker in Kenya.  You are good natured and helpful.
Your job is to keep the conversation going and also to help the human:
1. Find out what the human wants
2. Gather market data.

Extract the following data only from the human response.  If you give a suggestion, only enter the data if the human agrees with suggestion.

data:
- market : the name of the market where the farmer wants to sell the product
- farmer : the name of the farmer
- location : the location of the farmer
- product : the name of the product
- quantity : the quantity of the product
- price : the price of the product. Ask the seller if they want to set a price.

Stricly ONLY return a JSON array for your response.  

Include the following fields in the JSON array:
- data : the data you have gathered so far. Include all the data fields above. Leave as blank '' if you don't have the data yet.
- message : your response to the farmer
- state : '1' means you are still collecting data. '2' means all data has been collected.

Ask only one question at a time.
Always return the JSON array with the message, state and data fields.
Keep the conversation going until you complete the required information.
After all data is collected, provide valueable information in one sentence if you can.
"""

def create_chat() -> Any:

    # get and set openai api key
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    llm = ChatOpenAI(model='gpt-4')
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                # "You are a nice chatbot having a conversation with a human."
                template
            ),
            # The `variable_name` here is what must align with memory
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
    )
    
    #  # Notice that we `return_messages=True` to fit into the MessagesPlaceholder
    # # Notice that `"chat_history"` aligns with the MessagesPlaceholder name.
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
        memory=memory
    )

    return conversation
