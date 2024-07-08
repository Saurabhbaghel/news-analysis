import os
import time
import warnings
import argparse

import pandas as pd
from tqdm import tqdm

import parsing
import sentiment_analysis
import summarization
import news_database
import configs


warnings.filterwarnings("ignore")



def main(args):
    print("\n{:^50}".format("**Process Started**\n"))
    
    create_database = args.create_database
    db_name = args.db_name
    table_name = args.table_name
        
    # get the news articles
    news_website = "https://indianexpress.com/section/cities/delhi/"

    # get the news webpage
    webpage = parsing.get_the_webpage(url=news_website)    
    
    rows = []
    try:
        # find the embedded articles in the webpage
        for article_count, article in enumerate(parsing.embedded_articles(webpage), start=1):
            if args.debug:
                if article_count == 10 : break   # for debugging
            
            print(f"Article No. {article_count}", end="\t")
            
            start = time.time()        
            # for each embedded news article
            # we will get store its url, headline, content, summary and sentiment
            # get the sumamry of the content
            summary = summarization.summarize_news_article(article.content)
            
            # get the name of the organization mentioned
            org = sentiment_analysis.extract_org_name(summary)
            sentiment = "na"    #initializing sentiment
            
            if org:
                if len(org) != 0:
                    # get the sentiment of the summary
                    sentiment = sentiment_analysis.get_sentiment_wrt_org(org, summary)
            
            row = {
                "url": article.url,
                "headline": article.headline,
                "content": article.content,
                "summary": summary,
                "org": org,
                "sentiment": sentiment,
                # "degree_of_sentiment": sentiment_degree
            }  
            
            rows.append(row)
            end = time.time()
            
            time_taken = round(end-start, 2)
            print(f"Time Taken: {time_taken} seconds.", end="\n")

            article_count += 1
    except GeneratorExit:
        print("Processed all the articles.\n")
            
    rows = tuple(rows)
    
    if create_database:
        # storing data into the database
        news_database.store_data_in_db(db_name, table_name, data=rows)
        print(f"Saved into database: {db_name}, table: {table_name}.")    
    else:  
        print("Creating a csv.")    
        # create a dataframe
        df = pd.DataFrame(rows)
        # save the df
        csv_path = os.path.join(configs.Misc.DIR_SAVE_DATAFRAME.value, table_name+".csv")
        df.to_csv(csv_path, index=False)
        print(f"CSV saved: {csv_path}")

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to do sentiment analysis of News articles from a website.")
    parser.add_argument("--create-database", default=False, help="Whether to create a DB or not. If not given then a csv would be created. Default: False")
    parser.add_argument("--db-name", default="News.db", help="Name of the database if it is to be created. Default=News.db")
    parser.add_argument("--table-name", default="Articles", help="Name of the table. If DB is not to be created this will the name of the csv. Default=Article")
    parser.add_argument("--debug", default=False, help="Debugging. Will do for first 10 articles. Default=False")
    
    args = parser.parse_args()
    
    main(args)
    
    print("Dataframe saved.")
