from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from pathlib import Path
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_openai import ChatOpenAI
from dotenv import dotenv_values
from langchain_openai import OpenAIEmbeddings

config = dotenv_values(".env")
openai_api_key= config['OPENAI_API_KEY']


model = ChatOpenAI(
    model_name="gpt-3.5-turbo-0125",
    streaming=True,
    temperature=0, 
    api_key=openai_api_key
)


embedding = OpenAIEmbeddings(api_key=openai_api_key)

#ingest pdf
def pdf_to_retriever(file_path: str):
    # Extract file name from file path
    # Initialize the embedding function
    embedding_function = embedding
    # Delete files created 2 minutes ago in the directory
    # force_delete_files_created_1_day_ago(str("./user_uploaded_pdf_retriever"))
    # Construct the persist directory path
    persist_directory = Path(f"./data/pdf_retriever")
    if persist_directory.exists():
        print(f"Loading Chroma database from disk (Directory: {persist_directory})...")
        # Load from disk
        # db = Chroma(persist_directory=str(persist_directory), embedding_function=embedding_function)
        db = FAISS.load_local(str(persist_directory), embedding_function)
        print("Database loaded successfully!")
    else:
        print(f"Loading, chunking, and indexing the contents of the PDF: {file_path}...")
        loader = PyPDFDirectoryLoader(file_path)
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)

        print(f"Persist directory '{persist_directory}' does not exist. Creating and saving to disk...")
        # Create the persist directory and save to disk
        persist_directory.mkdir(parents=True, exist_ok=True)
        # db = Chroma.from_documents(texts, embedding_function, persist_directory=str(persist_directory))
        db =FAISS.from_documents(texts, embedding_function)
        db.save_local(str(persist_directory))
        print("Database saved to disk and loaded successfully!")

    return db


if __name__ == "__main__":
  #run this file only once  
  pdf_to_retriever("./data/pdf")