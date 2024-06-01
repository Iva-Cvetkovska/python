from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler

from some_dataset_ds import dataset

def divide_sets():
    train_ds = dataset[:int(0.8 * len(dataset))]
    val_ds = dataset[int(0.8 * len(dataset)):]
    return train_ds, val_ds


if __name__ == "__main__":
    neurons = int(input())
    alpha = float(input())
    index_to_delete = int(input())
    entry_to_classify = [float(row) for row in input().split(' ')]

    train_set, val_set = divide_sets()
    train_x, train_y = [row[:-1] for row in train_set], [row[-1] for row in train_set]
    val_x, val_y = [row[:-1] for row in val_set], [row[-1] for row in val_set]

    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaler.fit(train_x)

    classifier = MLPClassifier(neurons, learning_rate_init=alpha, max_iter=20, activation='relu', random_state=0)
    classifier.fit(scaler.transform(train_x), train_y)

    predictions_train = classifier.predict(scaler.transform(train_x))
    acc_train = 0
    for true, pred in zip(train_y, predictions_train):
        if true == pred:
            acc_train += 1
    accuracy_train = acc_train / len(train_y)

    predictions_val = classifier.predict(scaler.transform(val_x))
    acc_val = 0
    for true, pred in zip(val_y, predictions_val):
        if true == pred:
            acc_val += 1
    accuracy_val = acc_val / len(val_y)

    accuracy_diff = accuracy_train - accuracy_val
    if accuracy_diff > accuracy_val * 0.15:
        print("Se sluchuva overfitting")
        train_set_new = [[col for i, col in enumerate(row) if i != index_to_delete] for row in train_set]
        train_x_new, train_y_new = [row[:-1] for row in train_set_new], [row[-1] for row in train_set_new]

        scaler2 = MinMaxScaler(feature_range=(-1, 1))
        scaler2.fit(train_x_new)

        classifier2 = MLPClassifier(neurons, learning_rate_init=alpha, max_iter=20, activation='relu', random_state=0)
        classifier2.fit(scaler2.transform(train_x_new), train_y_new)

        entry_to_classify_new = [e for i, e in enumerate(entry_to_classify) if i != index_to_delete]

        prediction_for_entry = classifier2.predict(scaler2.transform([entry_to_classify_new]))[0]
        print(prediction_for_entry)
    else:
        print("Ne se sluchuva overfitting")
        prediction_for_entry = classifier.predict([entry_to_classify])[0]
        print(prediction_for_entry)


