import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
import re
import string

vectorization = TfidfVectorizer()
LR = LogisticRegression()
DT = DecisionTreeClassifier()
GBC = GradientBoostingClassifier(random_state=0)
RFC = RandomForestClassifier(random_state=0)

def wordopt(text):
   if isinstance(text, float):
      return "" 
   text = text.lower()
   text = re.sub('\[.*?\]', '', text)
   text = re.sub("\\W"," ",text) 
   text = re.sub('https?://\S+|www\.\S+', '', text)
   text = re.sub('<.*?>+', '', text)
   text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
   text = re.sub('\n', '', text)
   text = re.sub('\w*\d\w*', '', text)    
   return text

def trainModel():
   df = pd.read_csv("/Users/aaravnair/FakeNewsNet 2.csv")
   x, y = df["news_url"].apply(wordopt), df['real']
   x_train, x_test, y_train, y_test = train_test_split(x, y,test_size=.5,random_state =123)

   xv_train = vectorization.fit_transform(x_train)
   xv_test = vectorization.transform(x_test)

   LR.fit(xv_train,y_train)
   pred_lr=LR.predict(xv_test)
   LR.score(xv_test, y_test)

   DT.fit(xv_train, y_train)
   pred_dt = DT.predict(xv_test)
   DT.score(xv_test, y_test)

   GBC.fit(xv_train, y_train)
   pred_gbc = GBC.predict(xv_test)
   GBC.score(xv_test, y_test)

   RFC.fit(xv_train, y_train)
   pred_rfc = RFC.predict(xv_test)
   RFC.score(xv_test, y_test)

def manual_testing(news):
   testing_news = {"news_url":[news]}
   new_def_test = pd.DataFrame(testing_news)
   new_def_test["news_url"] = new_def_test["news_url"].apply(wordopt) 
   new_x_test = new_def_test["news_url"]
   new_xv_test = vectorization.transform(new_x_test)
   pred_LR = LR.predict(new_xv_test)
   pred_DT = DT.predict(new_xv_test)
   pred_GBC = GBC.predict(new_xv_test)
   pred_RFC = RFC.predict(new_xv_test)
   all = [pred_LR, pred_DT, pred_GBC, pred_RFC]
   return "Real" if sum(all) >= 2 else "Fake"
