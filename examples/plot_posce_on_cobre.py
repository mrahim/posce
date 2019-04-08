from nilearn.datasets import fetch_atlas_msdl, fetch_cobre
from nilearn.input_data import NiftiMapsMasker
from nilearn.connectome import vec_to_sym_matrix
from nilearn.plotting import plot_matrix
from posce import PopulationShrunkCovariance

# fetch atlas 
msdl = fetch_atlas_msdl()

# fetch rfMRI scans from cobre dataset
cobre = fetch_cobre(n_subjects=20)

# extract timeseries
masker = NiftiMapsMasker(
    msdl.maps, detrend=True, standardize=True, verbose=1, memory="."
)
masker.fit()
ts = [masker.transform(f) for f in cobre.func]

# compute PoSCE on the same dataset
posce = PopulationShrunkCovariance(shrinkage=1e-2)
posce.fit(ts)
connectivities = posce.transform(ts)

# plot the first shrunk covariance
cov = vec_to_sym_matrix(connectivities[0])
plot_matrix(cov)
