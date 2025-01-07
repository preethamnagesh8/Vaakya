from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain import hub
from langchain_openai import ChatOpenAI

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = InMemoryVectorStore(embeddings)
prompt = hub.pull("rlm/rag-prompt")
llm = ChatOpenAI(model="gpt-4o")

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

def load_docs_into_document_loaders(path_to_pdf):
    loader = PyMuPDFLoader(path_to_pdf)
    docs = loader.load()
    # print (docs)
    return docs

def split_docs_into_chunks(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # chunk size (characters)
        chunk_overlap=200,  # chunk overlap (characters)
        add_start_index=True,  # track index in original document
    )
    all_splits = text_splitter.split_documents(docs)
    return all_splits

def index_split_chunks(split_chunks):
    _ = vector_store.add_documents(documents=split_chunks)

def absorb_pdf_data(path_to_pdf):
    docs = load_docs_into_document_loaders(path_to_pdf=path_to_pdf)
    splits = split_docs_into_chunks(docs=docs)

def retrieve_relevant_docs(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}

def generate_answer_for_question(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}

def lang_graph_initiate_content_generation():
    graph_builder = StateGraph(State).add_sequence([retrieve_relevant_docs, generate_answer_for_question])
    graph_builder.add_edge(START, "retrieve_relevant_docs")
    graph = graph_builder.compile()
    response = graph.invoke({"question": "Explain the process of detecting ransomware"})
    print(response["answer"])