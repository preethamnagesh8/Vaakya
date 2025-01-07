import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from tools import pdf_tools


def generate_blog_content(pdf_path):
    _ = pdf_tools.absorb_pdf_data(pdf_path)
    _ = pdf_tools.lang_graph_initiate_content_generation()

if __name__ == "__main__":
    generate_blog_content("../data/raw/crypto_lock_drop_it.pdf")
    # env_var = os.getenv("OPENAI_API_KEY")