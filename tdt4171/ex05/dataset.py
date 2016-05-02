# -*- coding: utf-8 -*-

import matplotlib
import nnet
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

__author__ = 'kaiolae'


# Class for holding your data - one object for each line in the dataset
class DataInstance(object):

    def __init__(self, qid, rating, features):
        self.qid = qid  # ID of the query
        self.rating = rating  # Rating of this site for this query
        self.features = features  # The features of this query-site pair.

    def __str__(self):
        return "\nDataInstance - qid: %s\nrating: %s\nfeatures: %s" % (self.qid, self.rating, self.features)

    def __repr__(self):
        return self.__str__()


# A class that holds all the data in one of our sets (the training set or the testset)
class DataHolder(object):

    def __init__(self, dataset):
        self.dataset = self.load_data(dataset)

    @staticmethod
    def load_data(file):
        # Input: A file with the data.
        # Output: A dict mapping each query ID to the relevant documents,
        # like this: dataset[queryID] = [dataInstance1, dataInstance2, ...]
        data = open(file)
        dataset = {}
        for line in data:
            # Extracting all the useful info from the line of data
            line_data = line.split()
            rating = int(line_data[0])
            qid = int(line_data[1].split(':')[1])
            features = []
            for elem in line_data[2:]:
                if '#docid' in elem:  # We reached a comment. Line done.
                    break
                features.append(float(elem.split(':')[1]))
            # Creating a new data instance, inserting in the dict.
            di = DataInstance(qid, rating, features)
            if qid in dataset.keys():
                dataset[qid].append(di)
            else:
                dataset[qid] = [di]
        return dataset


def run_ranker(trainingset, testset, iterations=25, runs=1):
    # Dataholders for training and testset
    dh_training = DataHolder(trainingset)
    dh_testing = DataHolder(testset)

    training_patterns = []  # For holding all the training patterns we will feed the network
    test_patterns = []  # For holding all the test patterns we will feed the network

    for q, item in dh_training.dataset.items():
        for a in range(len(item) - 1):
            for b in range(a + 1, len(item)):
                if item[a].rating == item[b].rating:
                    continue

                training_patterns.append((
                    max(item[a], item[b], key=lambda x: x.rating),
                    min(item[a], item[b], key=lambda x: x.rating)
                ))

    for q, item in dh_testing.dataset.items():
        for a in range(len(item) - 1):
            for b in range(a + 1, len(item)):
                if item[a].rating == item[b].rating:
                    continue

                test_patterns.append((
                    max(item[a], item[b], key=lambda x: x.rating),
                    min(item[a], item[b], key=lambda x: x.rating)
                ))

    # Verify dataset integrity
    for pair in training_patterns:
        a, b = pair
        assert a.rating > b.rating
    for pair in test_patterns:
        a, b = pair
        assert a.rating > b.rating

    results = []
    for i in range(1, runs + 1):
        # Create new network for each run
        nn = nnet.NN(46, 10, learning_rate=0.0012)

        # Store each (train, test) error tuple for later plotting
        results.append(
            [e for e in nn.train(training_patterns, iterations=iterations, test_patterns=test_patterns)]
        )

    train_averages = []
    test_averages = []
    for i in range(iterations):
        tot_train = 0.0
        tot_test = 0.0
        for r in range(runs):
            train, test = results[r][i]

            tot_train += train
            tot_test += test

        train_averages.append(1.0 - tot_train / runs)
        test_averages.append(1.0 - tot_test / runs)

    epochs = list(map(lambda x: x+1, range(iterations)))
    plt.plot(epochs, train_averages, 'r-', label='Training')
    plt.plot(epochs, test_averages, 'b-', label='Testing')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.xlabel('Epoch')
    plt.ylabel('Correctness')
    axes = plt.gca()
    axes.set_xlim([0, 20])
    axes.set_ylim([0.0, 1.0])
    plt.show()


if __name__ == '__main__':
    run_ranker('train.txt', 'test.txt', runs=5, iterations=20)
