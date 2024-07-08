import requests
from json import JSONDecodeError

import spacy
from spacy.symbols import PROPN, nsubj, ORG
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForTokenClassification, pipeline
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from pydantic import BaseModel, Field


from configs import Sentiment, Ner


class Emotion(BaseModel):
    type: str = Field(description="type of emotion - neutral, positive or negative.")
    # degree: float = Field(description="degree of that emotion in range 0 to 1, 0 being weakest.")     


def extract_org_name(text: str):
    """extracts organization name from the text

    Args:
        text (str): _description_

    Yields:
        str: _description_
    """

    nlp = spacy.load("en_core_web_sm")
    for ent in nlp(text).ents:
        if ent.label == ORG:
            return ent.text # currently returning just one org

def get_sentiment_wrt_org(org: str, text: str) -> Emotion:
    """gets the sentiment from the perspective of the organization mentioned.

    Args:
        org (str): _description_
        text (str): _description_

    Returns:
        Emotion: has a type and a degree of that type
    """
    
    # assuming ollama is running 
    # prompt = "Find the sentiment of the text delimited by triple backticks"
    parser = JsonOutputParser(pydantic_object=Emotion)

    prompt = PromptTemplate.from_template(
        'Answer the user query.\n{format_instructions}\nFind the sentiment of the {text} from the perspective of {org}.\nRemove text outside JSON.',
        partial_variables={"format_instructions": parser.get_format_instructions()}
        )
    
    model = Ollama(model=Sentiment.MODEL.value)
    chain = prompt | model | parser

    success = False
    attempt = 1
    
    while not success and attempt < 3:
        try:
            _emotion = chain.invoke({"text": text, "org": org})
            success = True
        except OutputParserException:
            _emotion = chain.invoke({"text": text, "org": org})
            attempt += 1
    
    if not success:
        return "na"
       
    emotion = Emotion(type=_emotion["type"])
    
    return emotion.type


# def analyze(article_summary: str) -> Emotion:
#     """Does the sentiment analysis of the article summary

#     Args:
#         model_pipeline (HuggingFacePipeline): _description_
#         article_summary (str): _description_

#     Returns:
#         _type_: _description_
#     """
#     # pipe = pipeline("text-classification", model=Sentiment.MODEL_REPO.value)
#     # response = pipe(article_summary)[0] 
#     # sentiment, conf_score = response["label"], response["score"]
    
#     # get the names of the organizations
#     # sentiments = []
#     # for org in extract_org_names(article_summary):
#     #     sentiment = get_sentiment_wrt_org(org, article_summary)
#     #     sentiments.append(sentiment)

#     # getting the organization name in the text
#     org = extract_org_names(article_summary)
       
#     return get_sentiment_wrt_org(org, article_summary)
