from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

from solar_signals_ds import data


def split_ds():
    positive_class = [row for row in data if row[-1] == 1]
    negative_class = [row for row win data if row[-1] == 0]

    split_factor_25 = 0.25
    split_factor_50 = 0.5
    split_factor_75 = 0.75

    s_1 = positive_class[:int(split_factor_25 * len(positive_class))] + negative_class[
                                                                        :int(split_factor_25 * len(negative_class))]
    s_2 = positive_class[
          int(split_factor_25 * len(positive_class)):int(split_factor_50 * len(positive_class))] + negative_class[
                                                                                                   int(split_factor_25 * len(
                                                                                                       negative_class)):int(
                                                                                                       split_factor_50 * len(
                                                                                                           negative_class))]
    s_3 = positive_class[
          int(split_factor_50 * len(positive_class)):int(split_factor_75 * len(positive_class))] + negative_class[
                                                                                                   int(split_factor_50 * len(
                                                                                                       negative_class)):int(
                                                                                                       split_factor_75 * len(
                                                                                                           negative_class))]
    s_4 = positive_class[int(split_factor_75 * len(positive_class)):] + negative_class[
                                                                        int(split_factor_75 * len(negative_class)):]
    return s_1, s_2, s_3, s_4


def get_train_set(index, subsets):
    train_s = []
    for i, subset in enumerate(subsets):
        if i != index:
            train_s += subset
    return train_s


def calculate_accuracy(c, x, y, length):
    acc = 0
    for i in range(length):
        pred = c.predict([x[i]])[0]
        true = y[i]
        if pred == true:
            acc += 1
    return acc / length


def get_accuracies(c, subsets):
    accuracies = []
    for i in range(4):
        train_set, test_set = get_train_set(i, subsets), subsets[i]
        train_x, train_y = [row[:-1] for row in train_set], [row[-1] for row in train_set]
        test_x, test_y = [row[:-1] for row in test_set], [row[-1] for row in test_set]

        c.fit(train_x, train_y)
        acc = calculate_accuracy(c, test_x, test_y, len(test_set))
        accuracies.append(acc)
    return accuracies


def best_split_for_train_test(i_to_remove, best_i, subsets):
    train_s, test_s = get_train_set(best_i, subsets), subsets[best_i]
    train_s = [[col for i, col in enumerate(row) if i != i_to_remove] for row in train_s]
    test_s = [[col for i, col in enumerate(row) if i != i_to_remove] for row in test_s]
    return train_s, test_s


if __name__ == "__main__":
    # warnings.filterwarnings('ignore', category=ConvergenceWarning)
    subset_0, subset_1, subset_2, subset_3 = split_ds()
    subsets = [subset_0, subset_1, subset_2, subset_3]

    model = input()
    col_to_remove = int(input())

    if model == 'NB':
        nb_classifier = GaussianNB()
        accuracies = get_accuracies(nb_classifier, subsets)

        average_accuracy = sum(accuracies) / len(accuracies)
        print(f"Average accuracy: {average_accuracy}")

        best_precision_index = accuracies.index(max(accuracies))
        best_train_set, best_test_set = best_split_for_train_test(col_to_remove, best_precision_index, subsets)
        best_train_x, best_train_y = [row[:-1] for row in best_train_set], [row[-1] for row in best_train_set]
        best_test_x, best_test_y = [row[:-1] for row in best_test_set], [row[-1] for row in best_test_set]

        nb_classifier.fit(best_train_x, best_train_y)
        acc = calculate_accuracy(nb_classifier, best_test_x, best_test_y, len(best_test_set))
        print(f'Accuracy when we remove the column: {acc}')
    elif model == 'MLP':
        mlp_classifier = MLPClassifier(hidden_layer_sizes=50, activation='relu', learning_rate_init=0.001,
                                       random_state=0)
        accuracies = get_accuracies(mlp_classifier, subsets)
        average_accuracy = sum(accuracies) / len(accuracies)
        print(f"Average accuracy: {average_accuracy}")

        best_precision_index = accuracies.index(max(accuracies))
        best_train_set, best_test_set = best_split_for_train_test(col_to_remove, best_precision_index, subsets)
        best_train_x, best_train_y = [row[:-1] for row in best_train_set], [row[-1] for row in best_train_set]
        best_test_x, best_test_y = [row[:-1] for row in best_test_set], [row[-1] for row in best_test_set]

        mlp_classifier.fit(best_train_x, best_train_y)
        acc = calculate_accuracy(mlp_classifier, best_test_x, best_test_y, len(best_test_set))
        print(f'Accuracy when we remove the column: {acc}')
