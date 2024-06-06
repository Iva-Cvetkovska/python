from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

from some_ds import dataset


def split_ds(percent):
    # Првите X% од секоја класа се земаат за тренирање, додека останатите примероци се за тестирање.
    positive_class = [row for row in dataset if row[-1] == 1]
    negative_class = [row for row in dataset if row[-1] == 0]

    train = positive_class[:int(percent * len(positive_class))] + negative_class[:int(percent * len(negative_class))]
    test = positive_class[int(percent * len(positive_class)):] + negative_class[int(percent * len(negative_class)):]

    return train, test


def split_train_test(t_set):
    return [row[:-1] for row in t_set], [row[-1] for row in t_set]


def calculate_accuracy(c, x, y, length):
    acc = 0
    for i in range(length):
        pred = c.predict([x[i]])[0]
        true = y[i]
        if pred == true:
            acc += 1
    return acc / length


def add_weight(best_pred, losers):
    count_positive = 0
    count_negative = 0
    if best_pred == 1:
        count_positive += 2
    else:
        count_negative += 2

    for loser in losers:
        if loser == 1:
            count_positive += 1
        else:
            count_negative += 1

    return count_positive, count_negative


def calculate_predictions(classifiers, x):
    predictions = []
    for classifier in classifiers:
        prediction = classifier.predict(x)
        predictions.append(prediction)

    true_predictions = []
    for best_pred, c2_pred, c3_pred, c4_pred in zip(predictions[0], predictions[1], predictions[2], predictions[3]):
        count_positive, count_negative = add_weight(best_pred, [c2_pred, c3_pred, c4_pred])
        if count_positive >= count_negative:
            true_predictions.append(1)
        else:
            true_predictions.append(0)

    return true_predictions


def calculate_recall(y, predictions):
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

    if tp + fn == 0:
        print(0)
    else:
        print(f'Odzivot na kolekcijata so klasifikatori e {tp / (tp + fn)}')


if __name__ == "__main__":
    split_percent = int(input()) / 100

    train_set, test_set = split_ds(split_percent)
    train_x, train_y = split_train_test(train_set)
    test_x, test_y = split_train_test(test_set)

    nb_classifier = GaussianNB()
    nb_classifier.fit(train_x, train_y)
    accuracy_nb = calculate_accuracy(nb_classifier, test_x, test_y, len(test_set))

    tree_classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
    tree_classifier.fit(train_x, train_y)
    accuracy_tree = calculate_accuracy(tree_classifier, test_x, test_y, len(test_set))

    forest_classifier = RandomForestClassifier(n_estimators=4, criterion='entropy', random_state=0)
    forest_classifier.fit(train_x, train_y)
    accuracy_forest = calculate_accuracy(forest_classifier, test_x, test_y, len(test_set))

    mlp_classifier = MLPClassifier(hidden_layer_sizes=10, activation='relu', learning_rate_init=0.001, random_state=0)
    mlp_classifier.fit(train_x, train_y)
    accuracy_mlp = calculate_accuracy(mlp_classifier, test_x, test_y, len(test_set))

    if accuracy_nb >= accuracy_tree and accuracy_nb >= accuracy_forest and accuracy_nb >= accuracy_mlp:
        print("Najgolema tocnost ima klasifikatorot Naive Bayes")
        classifiers = [nb_classifier, tree_classifier, forest_classifier, mlp_classifier]
    elif accuracy_tree >= accuracy_nb and accuracy_tree >= accuracy_forest and accuracy_tree >= accuracy_mlp:
        print("Najgolema tocnost ima klasifikatorot Decision Tree")
        classifiers = [tree_classifier, nb_classifier, forest_classifier, mlp_classifier]
    elif accuracy_forest >= accuracy_nb and accuracy_forest >= accuracy_tree and accuracy_forest >= accuracy_mlp:
        print("Najgolema tocnost ima klasifikatorot Random Forest")
        classifiers = [forest_classifier, tree_classifier, nb_classifier, mlp_classifier]
    else:
        print("Najgolema tocnost ima klasifikatorot MLP")
        classifiers = [mlp_classifier, tree_classifier, forest_classifier, nb_classifier]

    # За предвидена се смета класата која што ќе добие најголем број гласови
    final_predictions = calculate_predictions(classifiers, test_x)
    calculate_recall(test_y, final_predictions)