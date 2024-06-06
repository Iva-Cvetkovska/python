from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from type_of_glass_ds import dataset


def split_ds(s_num):
    # првите N примероци ќе се користат за тестирање, а останатите за тренирање
    return dataset[s_num:], dataset[:s_num]


def remove_most_important_attribute(t_set, index):
    return [[col for i, col in enumerate(row) if i != index] for row in t_set]


def calculate_accuracy(c, x, y, length):
    acc = 0
    for i in range(length):
        pred = c.predict([x[i]])[0]
        true = y[i]
        if pred == true:
            acc += 1
    return acc / length


# 9 attributes and 7 different classes, 10 columns
if __name__ == "__main__":
    split_number = int(input())
    max_leaves = int(input())
    trees = int(input())

    train_set, test_set = split_ds(split_number)
    train_x, train_y = [row[:-1] for row in train_set], [row[-1] for row in train_set]
    test_x, test_y = [row[:-1] for row in test_set], [row[-1] for row in test_set]

    tree_classifier = DecisionTreeClassifier(max_leaf_nodes=max_leaves, random_state=0)
    tree_classifier.fit(train_x, train_y)
    feature_importances = list(tree_classifier.feature_importances_)
    most_important_index = feature_importances.index(max(feature_importances))

    train_set_removed = remove_most_important_attribute(train_set, most_important_index)
    train_x_removed, train_y_removed = [row[:-1] for row in train_set_removed], [row[-1] for row in train_set_removed]
    test_set_removed = remove_most_important_attribute(test_set, most_important_index)
    test_x_removed, test_y_removed = [row[:-1] for row in test_set_removed], [row[-1] for row in test_set_removed]

    standard_scaler = StandardScaler()
    standard_scaler.fit(train_x_removed)

    # Тренирајте го класификаторот со оригиналното податочно множество
    forest_classifier_original = RandomForestClassifier(n_estimators=trees, criterion='gini', random_state=0)
    forest_classifier_original.fit(train_x, train_y)

    forest_classifier_removed = RandomForestClassifier(n_estimators=trees, criterion='gini', random_state=0)
    forest_classifier_removed.fit(standard_scaler.transform(train_x_removed), train_y_removed)

    accuracy_original = calculate_accuracy(forest_classifier_original, test_x, test_y, len(test_set))
    accuracy_when_removed = calculate_accuracy(forest_classifier_removed, standard_scaler.transform(test_x_removed), test_y_removed,
                                               len(test_set_removed))

    print(f'Tochnost so originalnoto podatochno mnozestvo: {accuracy_original}')
    print(f'Tochnost so skalirani atributi: {accuracy_when_removed}')

    if accuracy_original > accuracy_when_removed:
        print('Skaliranjeto na atributi ne ja podobruva tochnosta')
    elif accuracy_when_removed > accuracy_original:
        print('Skaliranjeto na atributi ja podobruva tochnosta')
    else:
        print('Skaliranjeto na atributi nema vlijanie')
