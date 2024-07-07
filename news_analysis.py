import os

import pandas as pd

import parsing
import sentiment_analysis
import summarization
import configs

def main():
    
    urls = []
    headlines = []
    contents = []
    summaries = []
    sentiments = []
        
    # get the news articles
    news_website = "https://indianexpress.com/section/cities/delhi/"

    # get the news webpage
    webpage = parsing.get_the_webpage(url=news_website)    
    # find the embedded articles in the webpage
    for article in parsing.embedded_articles(webpage):
        # for each embedded news article
        # we will get store its url, headline, content, summary and sentiment
        urls.append(article.url)
        headlines.append(article.headline)
        contents.append(article.content)
        # get the sumamry of the content
        summary = summarization.summarize_news_article(article.content)
        summaries.append(summary)
        # get the sentiment of the summary
        sentiment, conf_score = sentiment_analysis.analyze(summary)
        sentiments.append(sentiment)
        
    # create a dataframe
    df = pd.DataFrame({
        "url": urls,
        "headline": headlines,
        "summary": summaries,
        "sentiment": sentiments
    })
    
    # save the df
    file_name = "news-articles.csv"
    df.to_csv(os.path.join(configs.Misc.DIR_SAVE_DATAFRAME.value, file_name), index=False)
    
    
if __name__ == "__main__":
    main()
    print("Dataframe saved.")
