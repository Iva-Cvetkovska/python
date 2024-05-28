from sklearn.neural_network import MLPClassifier

# 15 attributes and 2 classes
from solar_signals_ds import dataset


def divide_sets():
    metal_cylinder_class = [row for row in dataset if row[-1] == 0]
    cylinder_rock_class = [row for row in dataset if row[-1] == 1]

    train_ds = metal_cylinder_class[:int(0.8 * len(metal_cylinder_class))] + cylinder_rock_class[
                                                                             :int(0.8 * len(cylinder_rock_class))]
    val_ds = metal_cylinder_class[int(0.8 * len(metal_cylinder_class)):] + cylinder_rock_class[
                                                                           int(0.8 * len(cylinder_rock_class)):]

    return train_ds, val_ds


if __name__ == "__main__":
    alpha = float(input())
    epochs = int(input())

    train_set, val_set = divide_sets()
    train_x, train_y = [row[:-1] for row in train_set], [row[-1] for row in train_set]
    val_x, val_y = [row[:-1] for row in val_set], [row[-1] for row in val_set]

    classifier = MLPClassifier(6, activation='tanh', learning_rate_init=alpha, max_iter=epochs, random_state=0)
    classifier.fit(train_x, train_y)

    predictions = classifier.predict(train_x)
    acc_train = 0
    for true, pred in zip(train_y, predictions):
        if true == pred:
            acc_train += 1
    accuracy_train = acc_train / len(train_y)

    predictions_val = classifier.predict(val_x)
    acc_val = 0
    for true, pred in zip(val_y, predictions_val):
        if true == pred:
            acc_val += 1
    accuracy_val = acc_val / len(val_y)

    accuracy_difference = accuracy_train - accuracy_val

    if accuracy_difference > accuracy_val * 0.15:
        print('Overfitting is present')
    else:
        print('Overfitting is NOT present')

    print(f'Accuracy with training set: {accuracy_train}')
    print(f'Accuracy with validation set: {accuracy_val}')
