import os
import platform

import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image

import re
from bs4 import BeautifulSoup
from bs4.element import Comment

from collections import Counter
from string import punctuation

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

from selenium import webdriver
from selenium.webdriver.chrome.options import Options 

class Scraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
        }

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'chromedriver')

        chrome_options = Options()  
        chrome_options.add_argument("--headless")

        self.browser = browser=webdriver.Chrome(executable_path=filename, options=chrome_options)
    def is_visible(self, element):
        if element.parent.name in ['style', 'script', 'head']:
            return False
        if isinstance(element, Comment):
            return False
        if re.match(r"[\n]+",str(element)):
            return False
        
        return True
    
    def get(self):
        browser = self.browser
        
        """
        Goes to the link and scrapes the HTML
        I didn't wanna use requests library because some websites out there
        aren't serverside rendered.

        So, it's gonna be a better idea to use a headless browser.
        """
        
        browser.get(self.url)

        # get the html data
        html = browser.page_source        

        # close the browser since we no longer need it.
        browser.close()

        # load the html data.
        soup = BeautifulSoup(html, "lxml")

        # get all the texts that are "visible", and not in script, style tags etc.
        visible_text = filter(self.is_visible, soup.findAll(text=True))
        
        # join by ","
        text = u",".join(t.strip() for t in visible_text)

        # strip spaces from left & right.
        text = text.lstrip().rstrip()

        # have the cleared ready-to-use texts as an array.
        text = text.split(',')

        # ignore the stopwords
        ignore = set(STOPWORDS)

        # prepare the words
        words = (x.rstrip(punctuation).lower() for y in text for x in y.split())

        # create a counter object with the words that are not stopwords 
        c = Counter(word for word in words if word not in ignore)

        # get the most common words
        self.most_common_words = c.most_common()

        print("Most common words were: \n", self.most_common_words)
        
    # Creates a Tag Cloud
    def tagcloud(self):
        comment_words = ''

        for val in self.most_common_words: 
            val = str(val[0]) # ('value', 15)
            
            comment_words += val + " "

        # Generate a word cloud image
        mask = np.array(Image.open("morty.png"))

        wordcloud = WordCloud(width = 800, height = 800, 
                    background_color = 'black', 
                    mask=mask,
                    min_font_size = 10).generate(comment_words) 
    
        # create coloring from image
        image_colors = ImageColorGenerator(mask)
        
        plt.figure(figsize=[7,7])
        plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
        plt.axis("off")

        # store to file
        plt.savefig("mortytc.png", format="png")

        plt.show()

        print("Check mortytc.png")
        return False

        

url = input("Enter URL:")
scraper = Scraper(url)
scraper.get()

while True:
    wannaTagCloud = input("Do you want to create a tag cloud [Y/n]: ")
    if wannaTagCloud != '' and wannaTagCloud[0].lower() in ["y", "e"]: # yes or evet
        scraper.tagcloud()
        break
    else:
        print("""
        
   _| |
 _| | |
| | | |
| | | | __
| | | |/  \\
|       /\ \\
|      /  \/    Understandable, have a good day.
|      \  /\\
|       \/ /
 \        /
  |     /
  |    |
        
        """)
        break