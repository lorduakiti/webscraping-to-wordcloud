# COLECTING INFORMATION ON COVID FROM BRAZILIAN WEBSITE G1 AND SHOWING AS A WORD CLOUD
# Regarding the event's size, this project aims to use web scrapping to get information around the conference and plot as a word cloud.
# 
# The source of our information is the g1 portal, an important Brazilian news website.


# Libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup



# Reading the website
url = 'https://g1.globo.com/busca/?q=covid' # The url we are using to access

option = Options() 
option.headless = True 

driver = webdriver.Chrome('D:\\GitHub\\webscraping-to-wordcloud\\chromedriver.exe', options=option)
driver.get(url)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(10) # Waiting to have all data loaded



# Finding the content
element = driver.find_element_by_id("content")
html = element.get_attribute('outerHTML')
driver.quit() # closes the browser 

soup = BeautifulSoup(html, 'lxml') # Interpretando o html



# Title and summary
texto = []

for bloco in soup.find_all(class_='widget--info__text-container'):
    #print(bloco)
    for href in bloco.find_all('a'):
        titulo = href.find(class_="widget--info__title product-color")
        if(titulo != None):
            # print('titulo',titulo.text[7:-2])
            texto.append(titulo.text[7:-2])
        resumo = href.find(class_="widget--info__description")
        if(resumo != None):
            texto.append(resumo.text)
texto = ' '.join(texto)
# print(texto)



# Implemantation The word cloud
import nltk
nltk.download('stopwords')

comment_words = ''
stop_words_pt = nltk.corpus.stopwords.words('portuguese') # lista de stopword em portugues, stopw word palavras que não traz significado para o texto como: para, a, também,o
stop_words_pt = set(stop_words_pt)
stop_words_pt.update(['cop','pq',"ter","fala",'tá','pra','agora','todo', 'sobre','aí','taí'])

# print(stop_words_pt) # lista de stop word da biblioteca nltk


tokens = texto.split()

for i in range(len(tokens)):
    tokens[i] = tokens[i].lower()
    comment_words += " ".join(tokens)+" "



# Plot graph
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud

mask = np.array(Image.open('D:\\GitHub\\webscraping-to-wordcloud\\mask-covid19.png'))


wordcloud = WordCloud(mask = mask, margin = 10,
                background_color ='rgb(255, 56, 56)',
                stopwords = stop_words_pt,
                min_font_size = 10).generate(comment_words)


default_colors = wordcloud.to_array()
plt.figure()
plt.imshow(default_colors, interpolation="bilinear")
wordcloud.to_file("wordcloud-covid19.png")
plt.axis("off")
plt.show()
