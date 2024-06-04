from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from wine_quality_ds import dataset


def get_col(index, value, row_length):
    if index != row_length:
        return value
    elif value >= 5.0:
        return 1
    else:
        return 0


def split_classes():
    return [[get_col(i, col, len(row) - 1) for i, col in enumerate(row)] for row in dataset]


def split_ds(ds, s_percent):
    # First X percent from the dataset are used for testing, and the rest for training
    return ds[int(s_percent * len(ds)):], ds[:int(s_percent * len(ds))]


def calcuate_accuracy(c, scaler, y, x, length):
    acc = 0
    for i in range(length):
        pred = c.predict(scaler.transform([x[i]]))[0]
        true = y[i]
        if pred == true:
            acc += 1
    return acc / length



if __name__ == "__main__":
    ds = split_classes()
    split_percent = int(input()) / 100

    train_set, test_set = split_ds(ds, split_percent)
    train_x, train_y = [row[:-1] for row in train_set], [row[-1] for row in train_set]

    # ------ START TREE CLASSIFIER ------

    tree_classifier = DecisionTreeClassifier(criterion='gini', random_state=0)
    tree_classifier.fit(train_x, train_y)

    feature_importances = list(tree_classifier.feature_importances_)
    index = feature_importances.index(min(feature_importances))

    # ------ END TREE CLASSIFIER ------

    ds_without_least_important_attr = [[col for i, col in enumerate(row) if i != index] for row in ds]

    train_set_nn, test_set_nn = split_ds(ds_without_least_important_attr, split_percent)
    train_x_nn, train_y_nn = [row[:-1] for row in train_set_nn], [row[-1] for row in train_set_nn]
    test_x_nn, test_y_nn = [row[:-1] for row in test_set_nn], [row[-1] for row in test_set_nn]

    # ------ START STANDARD SCALER CLASSIFIER ------

    scaler_1 = StandardScaler()
    scaler_1.fit(train_x_nn)

    nn_classifier_1 = MLPClassifier(hidden_layer_sizes=15, activation='relu', learning_rate_init=0.001, max_iter=200,
                                    random_state=0)
    nn_classifier_1.fit(scaler_1.transform(train_x_nn), train_y_nn)

    acc_classifier_1 = calcuate_accuracy(nn_classifier_1, scaler_1, test_y_nn, test_x_nn, len(test_set_nn))
    print(f'Accuracy with StandardScaler: {acc_classifier_1}')

    # ------ END STANDARD SCALER CLASSIFIER ------

    # ------ START MINMAX SCALER CLASSIFIER ------

    scaler_2 = MinMaxScaler()
    scaler_2.fit(train_x_nn)

    nn_classifier_2 = MLPClassifier(hidden_layer_sizes=15, activation='relu', learning_rate_init=0.001, max_iter=200,
                                    random_state=0)
    nn_classifier_2.fit(scaler_2.transform(train_x_nn), train_y_nn)

    acc_classifier_2 = calcuate_accuracy(nn_classifier_2, scaler_2, test_y_nn, test_x_nn, len(test_set_nn))
    print(f'Accuracy with MinMaxScaler: {acc_classifier_2}')

    # ------ END MINMAX SCALER CLASSIFIER ------