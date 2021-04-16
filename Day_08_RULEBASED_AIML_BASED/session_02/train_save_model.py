import argparse
import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier


def train_save_model(data, model):

    df = pd.read_csv(data)

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    tree = DecisionTreeClassifier(max_depth=4)
    tree.fit(X, y)

    joblib.dump(tree, model)
    print(f"your tree classifier is saved as {model}")




if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--data',  default="data.csv")
    args.add_argument('--model', default="tree_clf.model")
    parsed_args = args.parse_args()
    train_save_model(parsed_args.data, parsed_args.model)