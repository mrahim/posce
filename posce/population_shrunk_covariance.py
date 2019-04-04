import numpy as np
from scipy.linalg import pinv
from sklearn.base import BaseEstimator, TransformerMixin, clone
from sklearn.covariance import LedoitWolf
from nilearn.connectome.connectivity_matrices import (
    is_spd,
    sym_matrix_to_vec,
    _geometric_mean,
    _map_eigenvalues,
)


def _shrunk_covariance_embedding(cov_embedding, Lambda0_inv, shrinkage=0.5):
    """Shrink the tangent embedding of a covariance (cov_embedding)
    according to a population prior (dSigma0, Lambda0_inv).
    """
    p = cov_embedding.shape[0]
    # XXX check whether it is useful to compute mu ?
    # mu = np.sum(cov_embedding) / p if scaling else 1.0

    # assuming Lambda = shrinkage*Identity
    Lambda_inv = (1.0 / shrinkage) * np.eye(p)

    # estimate dSigma
    C_inv = pinv(Lambda_inv + Lambda0_inv)
    shrunk_cov_embedding = np.dot(np.dot(C_inv, Lambda0_inv), cov_embedding)
    return shrunk_cov_embedding


class PopulationShrunkCovariance(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        cov_estimator=LedoitWolf(store_precision=False),
        prior_mean_type="geometric",
        shrinkage=0.5,
        discard_diagonal=False,
    ):
        self.cov_estimator = cov_estimator
        self.prior_mean_type = prior_mean_type
        self.shrinkage = shrinkage
        self.discard_diagonal = discard_diagonal

    def fit(self, X, y=0):
        # compute covariances from time-series
        self.cov_estimator_ = clone(self.cov_estimator)
        covariances = [self.cov_estimator_.fit(x).covariance_ for x in X]

        # compute prior mean
        if self.prior_mean_type == "geometric":
            self.mean_ = _geometric_mean(covariances, max_iter=30, tol=1e-7)
        elif self.prior_mean_type == "empirical":
            self.mean_ = np.mean(covariances, axis=0)
        else:
            raise ValueError(
                "Allowed mean types are"
                '"geometric", "euclidean"'
                ', got type "{}"'.format(self.prior_mean_type)
            )
        self.whitening_ = _map_eigenvalues(lambda x: 1.0 / np.sqrt(x), self.mean_)
        self.whitening_inv_ = _map_eigenvalues(lambda x: np.sqrt(x), self.mean_)

        # XXX compute prior dispersion
        connectivities = [
            _map_eigenvalues(np.log, self.whitening_.dot(cov).dot(self.whitening_))
            for cov in covariances
        ]
        connectivities = np.array(connectivities)
        connectivities = sym_matrix_to_vec(
            connectivities, discard_diagonal=self.discard_diagonal
        )
        self.Lambda0_ = np.mean(
            [np.expand_dims(c, 1).dot(np.expand_dims(c, 0)) for c in connectivities],
            axis=0,
        )
        self.Lambda0_inv_ = np.linalg.inv(self.Lambda0_)

    def transform(self, X):
        # compute covariances from time-series
        covariances = [self.cov_estimator_.fit(x).covariance_ for x in X]

        # transform in the tangent space
        connectivities = [
            _map_eigenvalues(np.log, self.whitening_.dot(cov).dot(self.whitening_))
            for cov in covariances
        ]

        connectivities = np.array(connectivities)
        connectivities = sym_matrix_to_vec(
            connectivities, discard_diagonal=self.discard_diagonal
        )
        # population shrinkage of connectivities
        shrunk_connectivities = [
            _shrunk_covariance_embedding(c, self.Lambda0_inv_, shrinkage=self.shrinkage)
            for c in connectivities
        ]
        return shrunk_connectivities
