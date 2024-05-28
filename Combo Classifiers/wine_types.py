from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from wine_types_ds import dataset


def get_first_x_entries(percent, zero_set, first_set, second_set):
    z_set = zero_set[:int(percent * len(zero_set))]
    f_set = first_set[:int(percent * len(first_set))]
    s_set = second_set[:int(percent * len(second_set))]
    return z_set + f_set + s_set


def get_last_x_entries(percent, zero_set, first_set, second_set):
    z_set = zero_set[int(percent * len(zero_set)):]
    f_set = first_set[int(percent * len(first_set)):]
    s_set = second_set[int(percent * len(second_set)):]
    return z_set + f_set + s_set


def get_range_x1_to_x2(x1_percent, x2_percent, zero_set, first_set, second_set):
    z_set = zero_set[int(x1_percent * len(zero_set)):int(x2_percent * len(zero_set))]
    f_set = first_set[int(x1_percent * len(first_set)):int(x2_percent * len(first_set))]
    s_set = second_set[int(x1_percent * len(second_set)):int(x2_percent * len(second_set))]
    return z_set + f_set + s_set


if __name__ == '__main__':
    x1 = float(input())
    x2 = float(input())  # x2 is always > x1

    zero_wine_set = [row for row in dataset if row[-1] == 0]
    first_wine_set = [row for row in dataset if row[-1] == 1]
    second_wine_set = [row for row in dataset if row[-1] == 2]

    naive_bayes_set = get_first_x_entries(x1, zero_wine_set, first_wine_set, second_wine_set)
    tree_set = get_range_x1_to_x2(x1, x2, zero_wine_set, first_wine_set, second_wine_set)
    forest_set = get_first_x_entries(x2, zero_wine_set, first_wine_set, second_wine_set)

    x_naive, y_naive = [row[:-1] for row in naive_bayes_set], [row[-1] for row in naive_bayes_set]
    x_tree, y_tree = [row[:-1] for row in tree_set], [row[-1] for row in tree_set]
    x_forest, y_forest = [row[:-1] for row in forest_set], [row[-1] for row in forest_set]

    test_set = get_last_x_entries(x2, zero_wine_set, first_wine_set, second_wine_set)
    x_test, y_test = [row[:-1] for row in test_set], [row[-1] for row in test_set]

    naive_classifier = GaussianNB()
    naive_classifier.fit(x_naive, y_naive)
    y_pred_naive = naive_classifier.predict(x_test)

    tree_classifier = DecisionTreeClassifier(random_state=0)
    tree_classifier.fit(x_tree, y_tree)
    y_pred_tree = tree_classifier.predict(x_test)

    forest_classifier = RandomForestClassifier(n_estimators=3, random_state=0)
    forest_classifier.fit(x_forest, y_forest)
    y_pred_forest = forest_classifier.predict(x_test)

    final_predictions = 0
    for i in range(len(y_test)):
        count = 0
        if y_test[i] == y_pred_naive[i]:
            count += 1
        if y_test[i] == y_pred_tree[i]:
            count += 1
        if y_test[i] == y_pred_forest[i]:
            count += 1
        if count >= 2:
            final_predictions += 1

    accuracy = final_predictions / len(y_test)
    print(f'Accuracy: {accuracy}')

