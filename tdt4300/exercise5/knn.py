#-*- coding: utf-8 -*-

import math

# FLAGS

DEBUG = False

# HOW MANY NEIGHBOURS ARE WE SELECTING?
K = 3

# ALL THE POINTS IN THE DATASET
POINTS = [
    (4,6),
    (6,9),
    (8,8),
    (3,3),
    (10,2),
    (9,6),
    (8,1),
    (3,4),
    (8,3),
    (4,4),
]

# THE CLUSTERS THE POINTS BELONG TO
CLUSTERS = [
    set([POINTS[0],POINTS[3],POINTS[7],POINTS[9]]),
    set([POINTS[1],POINTS[2],POINTS[5]]),
    set([POINTS[4],POINTS[6],POINTS[8]]),
]

# THE SAMPLE POINTS WE ARE TO CLASSIFY
SAMPLES = [
    (6,3),
    (6,6),
    (8,5),
]

### DISTANCE FUNCTIONS

def euclidean(point_one, point_two):
    """
    Calculates the euclidean distance between point one (x1, y1) and point two (x2, y2)
    """

    x1, y1 = point_one
    x2, y2 = point_two

    return math.sqrt(pow((x1-x2), 2) + pow((y1-y2), 2))

def manhattan(point_one, point_two):
    """
    Calculates the manhattan distance between point one (x1, y1) and point two (x2, y2)
    """

    x1, y1 = point_one
    x2, y2 = point_two

    return abs(x1-x2) + abs(y1-y2)

def generate_distances(point):
    """
    Takes in a point (X, Y) and generates distances lists for both Euclidean and
    Manhattan distances from the point to all the points in the dataset.
    Returns the two lists as a tuple
    """

    e_dist = list()
    m_dist = list()

    for p in POINTS:

        euclidean_distance = euclidean(point, p)
        manhattan_distance = manhattan(point, p)

        e_dist.append((euclidean_distance, p))
        m_dist.append((manhattan_distance, p))

    return (e_dist, m_dist)

def identify_cluster(knn_set):
    """
    Takes in a set of points that are the k-Nearest Neighbors,
    Returns which cluster that most accurately describes the sample
    """
    largest = 0
    classified = None
    confidence = 0.0

    if DEBUG:
        print "[DEBUG] Cluster identification"

    for cluster in CLUSTERS:
        if DEBUG:
            print "[DEBUG] Largest cluster as of now: %d" % largest
            print "[DEBUG] Now working on %s compared to %s" % (repr(knn_set), repr(cluster))
        if len(cluster & knn_set) > largest:
            largest = len(cluster & knn_set)
            classified = cluster
            if DEBUG:
                print "[DEBUG] We found a new larger this iteration, was: %s" % repr(cluster)
            confidence = (float(largest) / float(len(knn_set))) * 100.0

    return classified, confidence

### MAIN METHOD

if __name__ == '__main__':

    classified = dict()

    for point in SAMPLES:

        print "------------------------------------------------"
        print "Calculating distances for %s" % repr(point)

        euclidean_distance, manhattan_distance = generate_distances(point)

        euclidean_distance.sort()
        manhattan_distance.sort()

        print "-------------------------------------------------"

        print "3-NN (Euclidean) for %s is points %s, %s and %s" % (point, euclidean_distance[0][1], euclidean_distance[1][1], euclidean_distance[2][1])
        print "3-NN (Manhattan) for %s is points %s, %s and %s" % (point, manhattan_distance[0][1], manhattan_distance[1][1], manhattan_distance[2][1])

        print "-------------------------------------------------"
        print "Identifying cluster..."
        print "-------------------------------------------------"

        eucl_set = set([euclidean_distance[0][1], euclidean_distance[1][1], euclidean_distance[2][1]])
        manh_set = set([manhattan_distance[0][1], manhattan_distance[1][1], manhattan_distance[2][1]])

        cluster, confidence = identify_cluster(eucl_set)
        print "Point %s (Euclidean) most likely belongs to cluster:\n %s (Confidence: %.2f" % (repr(point), repr(cluster), confidence) + "%)"
        cluster, confidence = identify_cluster(manh_set)
        print "Point %s (Manhattan) most likely belongs to cluster:\n %s (Confidence: %.2f" % (repr(point), repr(cluster), confidence) + "%)"
