from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from cryotherapy_ds import dataset


def convert_to_int():
    int_ds = [[float(col) for col in row] for row in dataset]
    return [row[:-1] for row in int_ds], [row[-1] for row in int_ds]


if __name__ == '__main__':
    x, y = convert_to_int()

    train_x, test_x, train_y, test_y = train_test_split(x, y, train_size=0.85, test_size=0.15, shuffle=False)

    classifier = GaussianNB()
    classifier.fit(train_x, train_y)

    pred_y = classifier.predict(test_x)
    accuracy = accuracy_score(test_y, pred_y)

    print(accuracy)

    # 1 20 4 3 1 6
    entry = [float(e) for e in input().split(' ')]

    predicted_class_for_entry = classifier.predict([entry])[0]
    probabilities_for_entry = classifier.predict_proba([entry])
    print(int(predicted_class_for_entry))
    print(probabilities_for_entry)
