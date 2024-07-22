from lazypredict.Supervised import LazyRegressor
from lazypredict.Supervised import LazyClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("/Users/aaravnair/FakeNewsNet 2.csv")
x, y = df.drop('real', axis=1), df['real']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=100)


model = LogisticRegression()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)