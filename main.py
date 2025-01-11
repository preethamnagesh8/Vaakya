import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from tools import pdf_tools, wordpress_tools
from handlers import blog_handler

def generate_blog_content(pdf_path):
    _ = pdf_tools.absorb_pdf_data(pdf_path)
    _ = pdf_tools.lang_graph_initiate_content_generation()


def write_blog_for_topic(topic):
    new_blog = wordpress_tools.wordpress_create_empty_blog(topic)
    blog_id = new_blog['ID']
    global_blog_id = new_blog['global_ID']
    blog_handler.generate_blog_content_by_section_and_store(topic, global_blog_id)
    blog_handler.post_generated_blog_to_wordpress(blog_id, global_blog_id)


if __name__ == "__main__":
    blog_topic = "SQL Injection"
    write_blog_for_topic(blog_topic)