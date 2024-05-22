from solar_flare_ds import dataset
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier

# Main goal: calculate accuracy and precision of the last X samples from the dataset.

if __name__ == '__main__':
    samples_to_predict = int(input())
    criteria = 'gini'

    # Start: encode and split data
    encoder = OrdinalEncoder()
    encoder.fit([row[:-1] for row in dataset])

    train_set = dataset[:int(len(dataset)-samples_to_predict)]
    train_x = encoder.transform([row[:-1] for row in train_set])
    train_y = [row[-1] for row in train_set]

    test_set = dataset[int(len(dataset)-samples_to_predict):]
    test_x = encoder.transform([row[:-1] for row in test_set])
    test_y = [row[-1] for row in test_set]
    # End: encode and split data

    # Start: train classifier
    classifier = DecisionTreeClassifier(criterion=criteria, random_state=0)
    classifier.fit(train_x, train_y)
    # End: train classifier

    # Start: calculate accuracy
    TP = 0  # true positives
    FP = 0  # false positives
    TN = 0  # true negatives
    FN = 0  # false negatives

    for i in range(len(test_x)):
        predicted_class = classifier.predict([test_x[i]])[0]
        real_class = test_y[i]
        if predicted_class == real_class:
            if int(real_class) == 1:
                TP += 1
            else:
                TN += 1
        else:
            if int(predicted_class) == 1:
                FP += 1
            else:
                FN += 1

    accuracy = (TP + TN) / (TP + FP + TN + FN)
    print(f'Accuracy: {accuracy}')
    # End: calculate accuracy

    # Start: calculate precision
    if TP + FP == 0:
        precision = 0.0
    else:
        precision = TP / (TP + FP)
    print(f'Precision: {precision}')
    # End: calculate precision

