import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.string import StrOutputParser
from tools import wordpress_tools

blog_structure = ["Introduction", "Detailed Explanation", "Vulnerable Code Snippet", "Mitigation and Prevention", "Remediated Code Snippet", "Key Takeaways"]
blog_content_file_path = "./data/blog_content/"

def generate_blog_content_by_section_and_store(topic, global_id):
    section_content = ""
    new_blog_content_file = blog_content_file_path + str(global_id) + ".txt"

    blog_section_content_template = """
        Write a detailed, fact-based blog section on "{section}" for the topic "{topic}". 
        - Begin with the section heading wrapped in HTML <h3> tags.
        - Be careful when writing the remaining content. If the content is code example, wrap them in 
            HTML tags - <pre><code class="language-python">. Else, wrap them in HTML tags - <p>
        - Ensure clarity, accuracy, and logical flow.
        - Avoid vague statements; focus on providing insights.

        Target audience includes both beginners and professionals. Maintain a professional yet engaging tone.
    """

    with open(new_blog_content_file, "a") as blog_file:
        for blog_section in blog_structure:
            blog_section_content_prompt_template = PromptTemplate(
                template=blog_section_content_template,
                input_variables=["section", "topic"]
            )
            
            llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
            chain = blog_section_content_prompt_template | llm | StrOutputParser()
            res = chain.invoke(input={"section": blog_section, "topic": topic})

            blog_file.write(res + "\n")

def post_generated_blog_to_wordpress(blog_id, global_blog_id):
    blog_content_file = blog_content_file_path + str(global_blog_id) + ".txt"
    blog_content = None
    with open(blog_content_file, "r") as blog_file:
        blog_content = blog_file.read()
    update_result = wordpress_tools.wordpress_update_blog_content(blog_id, blog_content)
    os.remove(blog_content_file)
    return update_result

def generate_and_update_tags_for_wordpress_blog(blog_id, topic):
    tags_content_template = """
        Create 3 or 4 most relevant tags for a blog on the topic "{topic}". Generate a comma separated string. 
    """

    tags_content_prompt_template = PromptTemplate(
        template=tags_content_template,
        input_variables=["topic"]
    )

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    chain = tags_content_prompt_template | llm | StrOutputParser()
    res = chain.invoke(input={"topic": topic})
    tag_update_result = wordpress_tools.wordpress_update_blog_tags(blog_id, res)

    return tag_update_result


def generate_and_update_title_for_wordpress_blog(blog_id, topic):
    title_template = """
        Create a unique and engaging blog title for the topic: “{topic}”. 
        The title should spark curiosity, avoid generic phrasing, and be concise (under 15 words).
    """

    title_prompt_template = PromptTemplate(
        template=title_template,
        input_variables=["topic"]
    )

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    chain = title_prompt_template | llm | StrOutputParser()
    res = chain.invoke(input={"topic": topic})
    title_update_result = wordpress_tools.wordpress_update_blog_title(blog_id, res)

    return title_update_result