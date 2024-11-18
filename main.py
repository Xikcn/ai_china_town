from langchain_community.llms.ollama import Ollama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import warnings
from langchain_core.prompts import ChatPromptTemplate
warnings.filterwarnings('ignore')

# RAG智能体，继承LLM和嵌入模型使用

class OllamaAgent:
    def __init__(self,model,agent_name):
        self.model = model
        self.memory = ConversationBufferMemory()
        self.llm = Ollama(model=self.model)
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory
        )
        self.agent_name  = agent_name

    # 带历史记录的chat
    def chat(self,sentence):
        response = self.conversation.run(input=sentence)
        return response

    def op_e(self,environment):
        pass


    def rag(self,question,docs):
        prompt = ChatPromptTemplate.from_template("""仅根据提供的上下文回答以下问题:
               <context>
               {context}
               </context>
               Question: {input}""")

        document_chain = prompt | self.llm
        # 根据文件内容回答问题的逻辑
        result = document_chain.invoke({
            "input": question,
            "context": docs
        })
        print(result)






if __name__ == '__main__':
    oll = OllamaAgent('qwen2.5','小明')
    while True:
        print("begin")
        p = input()
        s = oll.chat(p)
        print(s)
