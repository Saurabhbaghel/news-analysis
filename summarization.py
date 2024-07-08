
from typing import Optional

import torch.nn as nn
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import TokenTextSplitter
from langchain_core.language_models.llms import LLM

from configs import Summarization


 
    
def model(repo: str=Summarization.MODEL_REPO.value, 
          tokenizer: str | AutoTokenizer=Summarization.TOKENIZER_REPO.value, 
          task: str="summarization"):
    
    """Builds the model and returns the HF pipeline

    Returns:
        _type_: _description_
    """
    tokenizer = AutoTokenizer.from_pretrained(tokenizer) if type(tokenizer) is str else tokenizer
    model = AutoModelForSeq2SeqLM.from_pretrained(repo)
    pipe = pipeline(task, 
                    model=model, 
                    tokenizer=tokenizer, 
                    max_length=Summarization.MAX_LENGTH.value, 
                    min_length=Summarization.MIN_LENGTH.value)
    return HuggingFacePipeline(pipeline=pipe)

def get_num_tokens(tokenizer: AutoTokenizer, text):
    """Gives the number of tokens
    

    Args:
        tokenizer (AutoTokenizer): _description_
        text (_type_): _description_

    Returns:
        _type_: _description_
    """
    return len(tokenizer(text).sequence_ids())


def divide_into_chunks(text: str, 
                       tokenizer: AutoTokenizer,
                       chunk_size: int=Summarization.CHUNK_SIZE.value,
                       chunk_overlap: int=Summarization.CHUNK_OVERLAP.value):
    """Divides the text into chunks with token length <= chunk_size

    Args:
        text (str): _description_
        model_pipeline (ModelPipeline): _description_
        chunk_size (int, optional): _description_. Defaults to CHUNK_SIZE.
        chunk_overlap (int, optional): _description_. Defaults to CHUNK_OVERLAP.

    Yields:
        _type_: _description_
    """
    
    token_splitter = TokenTextSplitter.from_huggingface_tokenizer(
        tokenizer=tokenizer,
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
        )
    
    for split_text in  token_splitter.split_text(text):
        yield split_text
        
    


def summarize_chunk(text: str, model: HuggingFacePipeline) -> str:
    
    """Summarize the news article

    Args:
        article (str): _description_

    Returns:
        str: _description_
    """
    
    # template = "Summarize: {text}"
    prompt = PromptTemplate.from_template(Summarization.PROMPT_TEMPLATE.value)
    chain = prompt | model
    return chain.invoke({"text": text}) 


def summarize_news_article(news_article: str) -> str:
    """Does the summarization of the news articles

    Args:
        text (str): _description_

    Returns:
        str: _description_
    """
    # what if the number of tokens in the article > 1024
    # the article should be divided into chunks of 600 - 700 tokens
    chunk_size = Summarization.CHUNK_SIZE.value

    repo = Summarization.MODEL_REPO.value
    tokenizer_repo = Summarization.TOKENIZER_REPO.value
    
    # initializing the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_repo)
    
    # initializing the model
    model_pipeline = model(repo, tokenizer, "summarization")
    
    summary_of_chunks = news_article

    # defining an inline function to get the number of tokens of the text
    # num_tokens = lambda text: get_num_tokens(tokenizer, text)
    num_tokens = get_num_tokens(tokenizer, news_article)
    print(f"Number of tokens: {num_tokens}", end="\t")
    
    if num_tokens > chunk_size:
        # re-initializing the summary of chunks
        summary_of_chunks = ""
        for chunk in divide_into_chunks(text=news_article, tokenizer=tokenizer, chunk_size=chunk_size):
            summary_of_chunks += " " + summarize_chunk(chunk, model=model_pipeline)
            
    # getting the final summarization of the summaries of the chunks
    return summarize_chunk(summary_of_chunks, model_pipeline)
