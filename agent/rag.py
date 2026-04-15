
from langchain_community.document_loaders  import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from utils.utility import load_apiKey
from model import LlmModel
import os

class Embedding:

    def create_embedding(self):
        load_apiKey()
        embedding=OpenAIEmbeddings(model='text-embedding-3-small')
        return embedding

class VectorDb:

    #retrieval_qa, retrieval, RetrievalQAWithSourcesChain
    def read_files(self):
        """This method read files form docs from resources folder nad return the list of docs."""
        docs=[]
        resources= os.path.abspath("resources")
        for f in os.listdir(resources):
            file=os.path.join(resources,f)
            docs.append(file)
        print (docs)
        return docs
        

    #need to check why append method not work.
    def chunkAll(self)-> list[Document]:
            """This will chunk all listed docs."""
            documents_after_load=[]
            
            resources= os.path.abspath("resources")
            document_loader = PyPDFDirectoryLoader(resources)
            documents_after_load = document_loader.load()
            print("length of docs loaded.",len(documents_after_load))

            split=RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
            splitted_docs=split.split_documents(documents_after_load)
            #final_doc=split.create_documents(splitted_docs)
            # print(splitted_docs)
            return splitted_docs
    
    def getChromaDBInstance(self)-> Chroma:
         embedding=Embedding().create_embedding()
         docs=self.chunkAll()
         ch_db=Chroma(embedding_function=embedding,persist_directory='./qa_db').from_documents(docs,embedding,persist_directory='./qa_db')
         print("Creation of db in progress..")
         return ch_db
         

    
class RagStuff:

    context="spacex starship. NeTflix Architecture"
    rule="Asssume you are an assistant which search info from docs.You have to check the {context} and answer {input}"
        
    template=ChatPromptTemplate.from_template("""
                                                Asssume you are an assistant which search info from docs. 
                                                You have to provide answer from asked {input} with given <context>{context}</context>
                                                """)
    print("input variables are:",template.input_variables)

    def tryRag(self):
        userinput= input("enter your topic to search from documets..")
        retriever = VectorDb().getChromaDBInstance().as_retriever()
        doc_chain=create_stuff_documents_chain(LlmModel().get_llm(),self.template)
        retieval_chain= create_retrieval_chain(retriever,doc_chain)
        response=retieval_chain.invoke({"input":userinput,"context":self.context})
        print(response.get('answer')) 
         
         
    
    
        





        