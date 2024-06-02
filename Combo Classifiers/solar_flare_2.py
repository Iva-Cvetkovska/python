from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

from solar_flare_ds_2 import data


def split_ds(m, split):
    if m == 'balanced':
        # use the first split% from each class for the training set and the rest for testing
        negative_class = [row for row in data if row[-1] == 0]
        positive_class = [row for row in data if row[-1] == 1]

        train_ds = negative_class[:int(split * len(negative_class))] + positive_class[:int(split * len(positive_class))]
        test_ds = negative_class[int(split * len(negative_class)):] + positive_class[int(split * len(positive_class)):]

        return train_ds, test_ds
    else:
        # use the first split% from the dataset for the training set and the rest for testing
        return data[:int(split * len(data))], data[int(split * len(data)):]


def calculate_precision(y, predictions):
    tp, fp, tn, fn = 0, 0, 0, 0
    for true, pred in zip(y, predictions):
        if true == 1:
            if pred == 1:
                tp += 1
            else:
                fn += 1
        else:
            if pred == 0:
                tn += 1
            else:
                fp += 1

    if tp + fp == 0:
        return tp
    else:
        return tp / (tp + fp)


def calculate_accuracy(x, y, classifier, length):
    acc = 0
    for i in range(length):
        pred = classifier.predict([x[i]])[0]
        true = y[i]
        if pred == true:
            acc += 1
    return acc / length


if __name__ == "__main__":
    mode = input()
    split_percent = int(input()) / 100

    train_set, test_set = split_ds(mode, split_percent)
    train_x, train_y = [row[:-1] for row in train_set], [row[-1] for row in train_set]
    test_x, test_y = [row[:-1] for row in test_set], [row[-1] for row in test_set]

    nb_classifier = GaussianNB()
    nb_classifier.fit(train_x, train_y)
    nb_precision = calculate_precision(test_y, nb_classifier.predict(test_x))

    forest_classifier = RandomForestClassifier(50, criterion='entropy', random_state=0)
    forest_classifier.fit(train_x, train_y)
    forest_precision = calculate_precision(test_y, forest_classifier.predict(test_x))

    nn_classifier = MLPClassifier(hidden_layer_sizes=50, activation='relu', learning_rate_init=0.001)
    nn_classifier.fit(train_x, train_y)
    nn_precision = calculate_precision(test_y, nn_classifier.predict(test_x))

    if nb_precision >= forest_precision and nb_precision >= nn_precision:
        print("The first classifier has the highest precision")
        accuracy = calculate_accuracy(test_x, test_y, nb_classifier, len(test_set))
        print(f"Accuracy: {accuracy}")
    elif forest_precision >= nb_precision and forest_precision >= nn_precision:
        print("The second classifier has the highest precision")
        accuracy = calculate_accuracy(test_x, test_y, forest_classifier, len(test_set))
        print(f"Accuracy: {accuracy}")
    elif nn_precision >= nb_precision and nn_precision >= forest_precision:
        print("The third classifier has the highest precision")
        accuracy = calculate_accuracy(test_x, test_y, nn_classifier, len(test_set))
        print(f"Accuracy: {accuracy}")
