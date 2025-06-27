import os
import dotenv
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

dotenv.load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="llama3-8b-8192", api_key=api_key)
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)