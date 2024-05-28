from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPClassifier

from wdbc_ds import dataset


def map_dataset():
    return [[0 if col == 'B' else 1 if col == 'M' else col for col in row] for row in dataset]


def divide_sets(ds):
    malignant_class = [row for row in ds if row[0] == 1]
    benign_class = [row for row in ds if row[0] == 0]

    train_ds = malignant_class[:int(0.7 * len(malignant_class))] + benign_class[:int(0.7 * len(benign_class))]
    test_ds = malignant_class[int(0.7 * len(malignant_class)):] + benign_class[int(0.7 * len(benign_class)):]

    return train_ds, test_ds


if __name__ == "__main__":
    hidden_neurons = int(input())

    ds = map_dataset()

    train_set, test_set = divide_sets(ds)
    train_x, train_y = [row[1:] for row in train_set], [row[0] for row in train_set]
    test_x, test_y = [row[1:] for row in test_set], [row[0] for row in test_set]

    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaler.fit(train_x)

    classifier = MLPClassifier(hidden_neurons, learning_rate_init=0.001, max_iter=20, activation='relu', random_state=0)
    classifier.fit(scaler.transform(train_x), train_y)

    predictions_train = classifier.predict(scaler.transform(train_x))

    tp_train, fp_train, tn_train, fn_train = 0, 0, 0, 0
    for true, pred in zip(train_y, predictions_train):
        if true == 1:
            if pred == 1:
                tp_train += 1
            else:
                fn_train += 1
        else:
            if pred == 0:
                tn_train += 1
            else:
                fp_train += 1

    acc_train = tp_train / (tp_train + fp_train)
    reply_train = tp_train / (tp_train + fn_train)

    print(f'Precision of the training set: {acc_train}')
    print(f'Recall of the training set: {reply_train}')

    predictions_test = classifier.predict(scaler.transform(test_x))

    tp_test, fp_test, tn_test, fn_test = 0, 0, 0, 0
    for true, pred in zip(test_y, predictions_test):
        if true == 1:
            if pred == 1:
                tp_test += 1
            else:
                fn_test += 1
        else:
            if pred == 0:
                tn_test += 1
            else:
                fp_test += 1

    if tp_test + fp_test == 0:
        acc_test = 0
    else:
        acc_test = tp_test / (tp_test + fp_test)
    if tp_test + fn_test == 0:
        recall_test = 0
    else:
        recall_test = tp_test / (tp_test + fn_test)

    print(
        f'Precision of the testing set: {acc_test}')
    print(f'Recall of the testing set: {recall_test}')
