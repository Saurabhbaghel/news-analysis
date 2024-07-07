from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline

import configs

def analyze(article_summary: str):
    """Does the sentiment analysis of the article summary

    Args:
        model_pipeline (HuggingFacePipeline): _description_
        article_summary (str): _description_

    Returns:
        _type_: _description_
    """
    pipe = pipeline("text-classification", model=configs.Sentiment.MODEL_REPO.value)
    response = pipe(article_summary)[0] 
    sentiment, conf_score = response["label"], response["score"]
    
    return sentiment, round(conf_score, 3)
