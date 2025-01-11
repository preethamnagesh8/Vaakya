import os
import requests

wordpress_api_token = os.environ.get("WORDPRESS_API_KEY")
create_blog_post_url = os.environ.get("WORDPRESS_NEW_BLOG_URL")
edit_blog_post_url = os.environ.get("WORDPRESS_EDIT_BLOG_URL")

def wordpress_update_blog_content(blog_id, blog_content):
    data = {
        "content": blog_content
    }

    headers = {
        "Authorization": f"Bearer {wordpress_api_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(edit_blog_post_url.format(blog_id=blog_id), json=data, headers=headers)
    return response.json()

def wordpress_update_blog_title(blog_id, blog_title):
    data = {
        "title": blog_title
    }
    headers = {
        "Authorization": f"Bearer {wordpress_api_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(edit_blog_post_url.format(blog_id=blog_id), json=data, headers=headers)
    return response.json()


def wordpress_update_blog_tags(blog_id, blog_tags_list_str):
    data = {
        "tags": blog_tags_list_str
    }
    headers = {
        "Authorization": f"Bearer {wordpress_api_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(edit_blog_post_url.format(blog_id=blog_id), json=data, headers=headers)
    return response.json()


def wordpress_create_empty_blog(blog_title):
    data = {
            "title": blog_title,
            "content": ""
    }
    headers = {
        "Authorization": f"Bearer {wordpress_api_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(create_blog_post_url, json=data, headers=headers)
    return response.json()