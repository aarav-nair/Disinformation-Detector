from lazypredict.Supervised import LazyRegressor
from lazypredict.Supervised import LazyClassifier
import pandas as pd
from sklearn.model_selection import train_test_split


# dir_path = os.path.dirname(os.path.realpath(__file__))
df = pd.read_csv("/Users/aaravnair/FakeNewsNet 2.csv")
x, y = df.drop('real', axis=1), df['real']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=100)
clf = LazyClassifier(verbose=0,ignore_warnings=True, custom_metric=None)
models, predictions = clf.fit(x_train, x_test, y_train, y_test)
print(models)