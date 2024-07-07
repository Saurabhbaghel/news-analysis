import requests
from bs4 import BeautifulSoup
from pydantic import Field, BaseModel


# aliasing the BeautifulSoup as Webpage
Webpage = BeautifulSoup

class Article(BaseModel):
    
    headline: str = Field(description="Headline of the article", default=None)
    url: str = Field(description="URL of the article.", default=None)
    content: str = Field(description="Text content of the article.", default=None)



def get_the_webpage(url: str) -> Webpage:

    """_summary_

    Args:
        url (str): _description_

    Returns:
        _type_: _description_
    """
    # make the connection with the webpage
    webpage = requests.get(url).text
    # convert into soup
    soup = BeautifulSoup(webpage, "html.parser")
    return soup


def parse_news_story(soup: Webpage) -> str:

    """parses the main news text content from the webpage

    Args:
        soup (Webpage): _description_

    Returns:
        str: _description_
    """
    # found that the div class with the id: pcl-full-content contains the story
    return soup.find("div", attrs={"id": "pcl-full-content"}).text



def embedded_articles(webpage: Webpage):

    """Finds the articles in the webpage and fetches their
    urls, headlines and content

    Args:
        webpage (Webpage): _description_

    Yields:
        tuple[]: _description_
    """
    for tag in webpage.findChildren("a"):
        if "article" in tag.attrs["href"]:  # if article keyword in url then it is directs to a article.
            try:
                if tag.text:
                    url = tag.attrs["href"]
                    # get the html parsed
                    soup = get_the_webpage(url)
                    # parse the headline
                    headline = soup.h1.text
                    # parse the actual content of the news
                    content = parse_news_story(soup)
                    yield Article(headline=headline, url=url, content=content)
            except:
                continue
    
    
