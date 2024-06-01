from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

from solar_flare_ds import dataset


def split_train_test(t_set):
    return [row[:-1] for row in t_set], [row[-1] for row in t_set]


def split_dataset(n):
    return dataset[n:], dataset[:n]


def remove_column(t_set, index):
    return [[col for i, col in enumerate(row) if i != index] for row in t_set]


def calculate_accuracy(c1, c2, ts_length, x1, y1, x2, y2):
    acc = 0
    for i in range(ts_length):
        predicted_class = c1.predict([x1[i]])[0]
        real_class = y1[i]
        if predicted_class == real_class:
            acc += 1
    accuracy_1 = acc / ts_length

    acc = 0
    for i in range(ts_length):
        predicted_class = c2.predict([x2[i]])[0]
        real_class = y2[i]
        if predicted_class == real_class:
            acc += 1
    accuracy_2 = acc / ts_length

    if accuracy_1 > accuracy_2:
        print("Klasifiktorot so site koloni ima pogolema tochnost")
        return y1, c1.predict(x1)
    elif accuracy_2 > accuracy_1:
        print("Klasifiktorot so edna kolona pomalku ima pogolema tochnost")
        return y2, c2.predict(x2)
    else:
        print("Klasifikatorite imaat ista tochnost")
        return y1, c1.predict(x1)


def calculate_precision(y, predicitons):
    tp, fp, tn, fn = 0, 0, 0, 0
    for true, pred in zip(y, predicitons):
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
    print(tp / (tp + fp))


if __name__ == "__main__":
    entries_to_predict = int(input())

    train_set, test_set = split_dataset(entries_to_predict)
    train_x, train_y = split_train_test(train_set)
    test_x, test_y = split_train_test(test_set)

    classifier_type = input()
    index_to_remove = int(input())

    train_set_2, test_set_2 = remove_column(train_set, index_to_remove), remove_column(test_set, index_to_remove)
    train_x_2, train_y_2 = split_train_test(train_set_2)
    test_x_2, test_y_2 = split_train_test(test_set_2)

    if classifier_type == "DT":
        classifier = DecisionTreeClassifier(random_state=0)
        classifier.fit(train_x, train_y)

        classifier_2 = DecisionTreeClassifier(random_state=0)
        classifier_2.fit(train_x_2, train_y_2)

        y, predictions = calculate_accuracy(classifier, classifier_2, len(test_set), test_x, test_y,
                                            test_x_2,
                                            test_y_2)
        calculate_precision(y, predictions)
    elif classifier_type == "NB":
        classifier = GaussianNB()
        classifier.fit(train_x, train_y)

        classifier_2 = GaussianNB()
        classifier_2.fit(train_x_2, train_y_2)

        y, predictions = calculate_accuracy(classifier, classifier_2, len(test_set), test_x, test_y,
                                            test_x_2,
                                            test_y_2)
        calculate_precision(y, predictions)
    else:
        classifier = MLPClassifier(hidden_layer_sizes=3, activation='relu', learning_rate_init=0.003, max_iter=200,
                                   random_state=0)
        classifier.fit(train_x, train_y)

        classifier_2 = MLPClassifier(hidden_layer_sizes=3, activation='relu', learning_rate_init=0.003, max_iter=200,
                                     random_state=0)
        classifier_2.fit(train_x_2, train_y_2)

        y, predictions = calculate_accuracy(classifier, classifier_2, len(test_set), test_x, test_y,
                                            test_x_2,
                                            test_y_2)
        calculate_precision(y, predictions)
