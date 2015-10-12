# -*- coding_ utf-8 -*-

from pybrain.structure import TanhLayer
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer


if __name__ == '__main__':
    ds = SupervisedDataSet(1, 1)

    # Add data samples
    ds.addSample((1,), (1,))
    ds.addSample((2,), (2,))
    ds.addSample((3,), (3,))
    ds.addSample((4,), (4,))
    ds.addSample((5,), (5,))
    ds.addSample((6,), (6,))
    ds.addSample((7,), (7,))
    ds.addSample((8,), (8,))

    net = buildNetwork(1, 8, 1, bias=True, hiddenclass=TanhLayer)
    net.sortModules()
    trainer = BackpropTrainer(net, ds)

    trainer.trainUntilConvergence(verbose=False, validationProportion=0.15, maxEpochs=1000, continueEpochs=10)

    print(net.activateOnDataset(ds))

    print(net)
    print(net.params)
    print(sum(net.params))

    #print(net.activate((15,)))
    #print(net.activate((0.152,)))
    #print(net.activate((-4,)))

