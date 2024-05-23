from sklearn.naive_bayes import CategoricalNB
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from solar_flare_ds import dataset

if __name__ == '__main__':
    train_size = 0.75
    test_size = 0.25
    entry = [e for e in input().split(' ')]

    encoder = OrdinalEncoder()
    encoder.fit([row[:-1] for row in dataset])

    x = encoder.transform([row[:-1] for row in dataset])
    y = [row[-1] for row in dataset]

    train_x, test_x, train_y, test_y = train_test_split(x, y, train_size=train_size, test_size=test_size, shuffle=False)
    # train_set = dataset[:int(0.75 * len(dataset))]
    # train_x = encoder.transform([row[:-1] for row in train_set])
    # train_y = [row[-1] for row in train_set]
    #
    # test_set = dataset[int(0.75 * len(dataset)):]
    # test_x = encoder.transform([row[:-1] for row in test_set])
    # test_y = [row[-1] for row in test_set]

    classifier = CategoricalNB()
    classifier.fit(train_x, train_y)

    pred_y = classifier.predict(test_x)
    accuracy = accuracy_score(test_y, pred_y)
    print(accuracy)

    # for i in range(len(test_set)):
    #     predicted_class = classifier.predict([test_x[i]])[0]
    #     real_class = test_y[i]
    #     if predicted_class == real_class:
    #         accuracy += 1
    #
    # print(accuracy / len(test_set))

    # H R X 1 2 1 1 2 1 1
    encoded_entry = encoder.transform([entry])

    predicted_class_for_entry = classifier.predict(encoded_entry)[0]
    print(predicted_class_for_entry)

    print(classifier.predict_proba(encoded_entry))

