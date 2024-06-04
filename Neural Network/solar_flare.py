from sklearn.neural_network import MLPClassifier

from solar_flare_ds import dataset


def split_ds(split_num):
    # The last X entries are for testing, the rest are for training
    return dataset[:len(dataset) - split_num], dataset[len(dataset) - split_num:]


def calculate_precision_and_recall(y, predictions):
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
        recall = 0
    else:
        recall = tp / (tp + fn)

    if tp + fp == 0:
        return 0, recall
    else:
        return tp / (tp + fp), recall


if __name__ == "__main__":
    split_num = int(input())

    train_set, test_set = split_ds(split_num)
    train_x, train_y = [row[:-1] for row in train_set], [row[-1] for row in train_set]
    test_x, test_y = [row[:-1] for row in test_set], [row[-1] for row in test_set]

    classifier = MLPClassifier(3, activation='relu', learning_rate_init=0.003, max_iter=200, random_state=0)
    classifier.fit(train_x, train_y)

    precision, recall = calculate_precision_and_recall(test_y, classifier.predict(test_x))
    print(f'Precision: {precision}')
    print(f'Recall: {recall}')
