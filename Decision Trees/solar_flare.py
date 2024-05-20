from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier
from solar_flare_ds import dataset

if __name__ == '__main__':
    percent = int(input()) / 100
    criterion = input()

    encoder = OrdinalEncoder()
    encoder.fit([row[:-1] for row in dataset])

    train_set = dataset[int((1 - percent) * len(dataset)):]
    train_x = encoder.transform([row[:-1] for row in train_set])
    train_y = [row[-1] for row in train_set]

    test_set = dataset[:int((1 - percent) * len(dataset))]
    test_x = encoder.transform([row[:-1] for row in test_set])
    test_y = [row[-1] for row in test_set]

    classifier = DecisionTreeClassifier(criterion=criterion, random_state=0)
    classifier.fit(train_x, train_y)

    print(f'Depth: {classifier.get_depth()}')
    print(f'Number of leaves: {classifier.get_n_leaves()}')

    accuracy = 0

    for i in range(len(test_set)):
        predicted_class = classifier.predict([test_x[i]])[0]
        real_class = test_y[i]
        if predicted_class == real_class:
            accuracy += 1

    accuracy = accuracy / len(test_set)

    print(f'Accuracy: {accuracy}')

    feature_importances = list(classifier.feature_importances_)
    most_important_feature = feature_importances.index(max(feature_importances))
    least_important_feature = feature_importances.index(min(feature_importances))

    print(f'Most important feature: {most_important_feature}')
    print(f'Least important feature: {least_important_feature}')

