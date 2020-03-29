
#tahap scrape data------------------------------------
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

import pandas as pd

import pandas as pd
import re
import string
import nltk
import Sastrawi
import matplotlib.pyplot as plt
import numpy as np
import Sastrawi
import seaborn as sns
import math 

from nltk.tokenize import word_tokenize 
from nltk.tokenize import WordPunctTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from os import path
from PIL import Image
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import naive_bayes
from sklearn.metrics import roc_auc_score
from pylab import rcParams
from bs4 import BeautifulSoup
from matplotlib import rc
from collections import Counter, defaultdict
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix

class sentimenAnalysis:
    search=""
   
    def scrappingData(request, data):  
        
        search = data
        print(data)
        nltk.download('punkt')
        nltk.download('stopwords')
        
        # %matplotlib inline
        RANDOM_SEED = 42
        np.random.seed(RANDOM_SEED)

        chrome_path= r"C:\Users\Rifqi Rosidin\Documents\za\chromedriver_win32\chromedriver.exe"
        driver=webdriver.Chrome(chrome_path)
        
            
        driver.get('https://play.google.com/store/search?q=' +search+ '&c=apps'+ '&hl=in')
        tes = driver.find_element_by_xpath("//*[@id='fcxH9b']/div[4]/c-wiz/div/div[2]/div/c-wiz/c-wiz[1]/c-wiz/div/div[2]/div[1]/c-wiz/div/div/div[1]/div/div/a")
        tes.click()
        time.sleep(5)
        tes1 = driver.find_element_by_xpath("//*[@id='fcxH9b']/div[4]/c-wiz[2]/div/div[2]/div/div[1]/div/div/div[1]/div[6]/div/span/span")
        tes1.click()

        count = 1
        i = 1
        while i < 2:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            if((i % 2)== 0):
                driver.execute_script('window.scrollTo(1, 2000);')
                time.sleep(2)
                tes2 = driver.find_element_by_xpath("//*[@id='fcxH9b']/div[4]/c-wiz[3]/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div/span/span")
                tes2.click()
            print("scroll ke -" + str(count))
            i += 1
            count+=1
        print('udah scrolling')
        a = 'test1'
        b = 1
        c = []
       
        driver.execute_script('window.scrollTo(1, 10);')

        while a != 'test':
            d = 2
            try:
                tes3 = driver.find_element_by_xpath("//*[@id='fcxH9b']/div[4]/c-wiz[3]/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div["+str(b)+"]/div/div[2]/div[2]/span[1]/div/button")
                tes3.click()
            except NoSuchElementException:
                d = 1
                
            tes4 = driver.find_element_by_xpath("/html/body/div[1]/div[4]/c-wiz[3]/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div["+str(b)+"]/div/div[2]/div[2]/span["+str(d)+"]")
            print(str(b) + tes4.text)
            c.append(tes4.text)
            if(b >= 10):
                a = 'test'
            b += 1
    #akhir tahap scrape data------------------------------------

        print(len(c))

    # hapus komentar
        data = pd.DataFrame({"ulasan": c})
        df = data['ulasan']
        ulasan = []
        x = 0
        y = ''
        for i in df :
            emoji = i.replace('emoji','')
            if emoji.isspace(): 
                ulasan.append(x)
            else:
                y = 'tess'
            x += 1
        komentar = data.drop(ulasan)

        print("--------------hapus Emoji-------")
        print(komentar)

        #tahap melakukan case folding dan angka dan whitespace()
        case = []
        for i in komentar['ulasan']:
            b = re.sub(r'', '', str(i))
            a = b.lower() #menjadikan huruf kecil
            c = re.sub(r'[0-9]+', '', a) #menghilangkan angka
            d = c.strip() #menghapus whitecase
            e = d.translate(str.maketrans("","",string.punctuation)) #menghilangkan karakter
            case.append(e)

        komentar['ulasan'] = case
        print("\n")
        print("-------case folding dan angka dan whirespace---------")
        print(komentar)

        token=[]

        for i in komentar['ulasan']:
            tokens = nltk.tokenize.word_tokenize(str(i))
            token.append(tokens)
        token

    #akhir tahap pemisahan teks menjadi potongan-potongan 
        def listToString(s):  
        
        # initialize an empty string 
            str1 = ""  
            
            # traverse in the string   
            for i in s:  
                str1 += str(i) 
            
            # return string   
            return str1

        kata = listToString(token)
            
        #add stopword
        print("-------pemisahan teks menjadi potongan-potongan ---------")
        print(kata)

        #add stopword

        stop_factory = StopWordRemoverFactory().get_stop_words()
        more_stopword = ['yg', 'tp'] #menambahkan stopword
        print(stopwords)

        factory = StopWordRemoverFactory()
        stopword = factory.create_stop_word_remover()

        word=[]
        for i in komentar['ulasan']:
            stop = stopword.remove(str(i))
            tokens = nltk.tokenize.word_tokenize(stop)
            word = stop_factory + more_stopword
            word.append(tokens)
        # word

        #akhir add stopword

        #menjadikan kata ke bentuk dasarnya

        factory = StemmerFactory()
        stemmer = factory.create_stemmer()

        Hasil=[]

        for i in komentar['ulasan']:
            hasil = stemmer.stem(str(i))
            Hasil.append(hasil)
        Hasil

        kata = listToString(Hasil)

        print("------menjadikan kata ke bentuk dasarnya--------")
        print(kata)

       