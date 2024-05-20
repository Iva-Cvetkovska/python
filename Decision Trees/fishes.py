from sklearn.ensemble import RandomForestClassifier
from fishes_ds import dataset

if __name__ == '__main__':
    index_to_remove = int(input())
    n_trees = int(input())
    criterion = input()
    to_classify = input().split()
    to_classify.pop(index_to_remove)

    ds = list()
    for d in dataset:
        row = [d[i] for i in range(len(d)) if i != index_to_remove]
        ds.append(row)

    train_set = ds[:int(0.85 * len(ds))]
    train_x = [row[:-1] for row in train_set]
    train_y = [row[-1] for row in train_set]

    test_set = ds[int(0.85 * len(ds)):]
    test_x = [row[:-1] for row in test_set]
    test_y = [row[-1] for row in test_set]

    classifier = RandomForestClassifier(n_estimators=n_trees, criterion=criterion, random_state=0)
    classifier.fit(train_x, train_y)

    accuracy = 0

    for i in range(len(test_set)):
        predicted_class = classifier.predict([test_x[i]])[0]
        real_class = test_y[i]
        if predicted_class == real_class:
            accuracy += 1

    accuracy = accuracy / len(test_set)
    print(f'Accuracy: {accuracy}')

    predicted_class_new = classifier.predict([to_classify])[0]
    probabilities = classifier.predict_proba([to_classify])[0]

    print(predicted_class_new)
    print(probabilities)

