# -*- coding: utf-8 -*-

import nnet

__author__ = 'kaiolae'


# Class for holding your data - one object for each line in the dataset
class DataInstance(object):

    def __init__(self, qid, rating, features):
        self.qid = qid  # ID of the query
        self.rating = rating  # Rating of this site for this query
        self.features = features  # The features of this query-site pair.

    def __str__(self):
        return "DataInstance - qid: %s. rating: %s. features: %s" % (self.qid, self.rating, self.features)


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


def run_ranker(trainingset, testset):
    # TODO: Insert the code for training and testing your ranker here.

    # Dataholders for training and testset
    dh_training = DataHolder(trainingset)
    dh_testing = DataHolder(testset)

    # Creating an ANN instance - feel free to experiment with the learning rate (the third parameter).
    nn = nnet.NN(46, 10, 0.0011)

    # TODO: The lists below should hold training patterns in this format:
    # [(data1Features,data2Features), (data1Features,data3Features), ... , (dataNFeatures,dataMFeatures)]

    # TODO: The training set needs to have pairs ordered so the first item of the pair has a higher rating.

    training_patterns = []  # For holding all the training patterns we will feed the network
    test_patterns = []  # For holding all the test patterns we will feed the network
    for qid in dh_training.dataset.keys():
        # This iterates through every query ID in our training set
        data_instance = dh_training.dataset[qid]  # All data instances (query, features, rating) for query qid

        # TODO: Store the training instances into the trainingPatterns array.
        # Remember to store them as pairs, where the first item is rated higher than the second.

        # TODO: Hint: A good first step to get the pair ordering right,
        # is to sort the instances based on their rating for this query. (sort by x.rating for each x in dataInstance)

    for qid in dh_testing.dataset.keys():
        # This iterates through every query ID in our test set
        data_instance = dh_testing.dataset[qid]

        # TODO: Store the test instances into the testPatterns array, once again as pairs.

        # TODO: Hint: The testing will be easier for you if you also now order the pairs,
        # it will make it easy to see if the ANN agrees with your ordering.

    # Check ANN performance before training
    nn.countMisorderedPairs(test_patterns)
    for i in range(25):
        # Running 25 iterations, measuring testing performance after each round of training.
        # Training
        nn.train(training_patterns)
        # Check ANN performance after training.
        nn.countMisorderedPairs(test_patterns)

    # TODO: Store the data returned by countMisorderedPairs and plot it,
    # showing how training and testing errors develop.


run_ranker("train.txt", "test.txt")
