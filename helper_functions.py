import docx2txt
import pdfplumber
import streamlit as st

from openai import OpenAI
import openai

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

import time
import os


def read_docx(file):
    """Read and return text from a docx file."""
    return docx2txt.process(file)

def read_pdf(file):
    """Read and return text from a PDF file."""
    with pdfplumber.open(file) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    return '\n'.join(pages)

def handle_other_option(selected_option, key):
    if selected_option == "Other":
        return st.text_input("Specify your option", key=key)
    return selected_option



def generate_article(user_input, article_type, tone_style, target_audience, openai_api_key):
    """
    Generate an article based on the user input and the provided parameters.
    """

    openai.api_key = openai_api_key

    prompt_message = (
        f"Write a {article_type} with a {tone_style} tone for {target_audience}. "
        f"Please provide only the body of the article, without any additional instructions or content. "
        f"Based on the following notes:\n{user_input}"
    )

    # Create a chat completion request
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" based on your preference
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt_message
            }
        ]
    )

    # Extract and return the generated article
    return completion.choices[0].message.content



def generate_title(article, title_style, title_lenght, openai_api_key):
    """
    Generate a title for the provided article based on the specified style and length.
    """
    
    openai.api_key = openai_api_key

    # Compose a prompt that instructs the AI not to use quotation marks
    prompt_message = (
        f"Create a {title_style} title in about {title_lenght} words for the following article, without using quotation marks:\n{article}"
    )

    # Create a chat completion request
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" based on your preference
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt_message
            }
        ]
    )

    # Extract and return the generated title
    generated_title = completion.choices[0].message.content

    # Remove quotation marks if present
    return generated_title.strip('\"')



### Functions for further development

def stream_data(data):
    """ 'stream' the article and display it word by word"""
    for word in data.split():
        yield word + " "
        time.sleep(0.02)


def generate_image(prompt):
    """ Generate an image based on the provided prompt which is the article title."""
    client = OpenAI()

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    return image_url