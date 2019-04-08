posce : POpulation Shrinkage Covariance Embedding
=================================================

posce is a functional connectivity estimator from rfMRI timeseries.
It relies on the Riemannian geometry of covariances and integrates 
prior knowledge of covariance distribution over a population.

This is an implementation of the work introduced in :

M. Rahim, B. Thirion and G. Varoquaux. Population
shrinkage of covariance (PoSCE) for better individual brain
functional-connectivity estimation, in Medical Image Analysis (2019).
`link <https://hal.inria.fr/hal-02068389>`_

Installation
============


::

    python setup.py install --user


posce requires:

- nilearn
