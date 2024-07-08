from enum import Enum

class Misc(Enum):
    """General Configuration"""
    DIR_SAVE_DATAFRAME = "./data"

class Summarization(Enum):
    """Summarization Configuration"""
    
    MAX_LENGTH = 200
    MIN_LENGTH = 20
    MODEL_REPO = "facebook/bart-large-cnn" #"sshleifer/distilbart-cnn-12-6"
    TOKENIZER_REPO = "facebook/bart-large-cnn" # "sshleifer/distilbart-cnn-12-6"
    CHUNK_SIZE = 600
    CHUNK_OVERLAP = 10
    PROMPT_TEMPLATE = "Summarize: {text}"   # keep the variable name as text here


class Sentiment(Enum):
    """Sentiment Analysis Configuration"""
    
    MODEL_REPO = "avichr/heBERT_sentiment_analysis"
    MODEL = "llama3"
    
class Ner(Enum):
    MODEL_REPO = "dslim/bert-base-NER"
    TOKENIZER_REPO = "dslim/bert-base-NER"
