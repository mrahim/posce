#%%
from nilearn.datasets import fetch_atlas_msdl, fetch_cobre
from nilearn.input_data import NiftiMapsMasker
from nilearn.connectome import vec_to_sym_matrix, ConnectivityMeasure
from nilearn.plotting import plot_matrix
from posce import PopulationShrunkCovariance

#%%
# fetch atlas
msdl = fetch_atlas_msdl()

# fetch rfMRI scans from cobre dataset
cobre = fetch_cobre(n_subjects=20)
#  extract timeseries
#%%
masker = NiftiMapsMasker(
    msdl.maps, detrend=True, standardize=True, verbose=1, memory="."
)
masker.fit()
ts = [masker.transform(f) for f in cobre.func]
#%%
# compute correlation
corr = ConnectivityMeasure(kind="correlation")
corr_connectivities = corr.fit_transform(ts)

# compute partial correlation
pcorr = ConnectivityMeasure(kind="partial correlation")
pcorr_connectivities = pcorr.fit_transform(ts)

# compute tangent embedding
tangent = ConnectivityMeasure(kind="tangent")
tangent_connectivities = tangent.fit_transform(ts)
#%%
# compute PoSCE
posce = PopulationShrunkCovariance(shrinkage=1e-2)
posce.fit(ts)
shrunk_connectivities = posce.transform(ts)
shrunk_connectivities = [vec_to_sym_matrix(c) for c in shrunk_connectivities]

#%%
# plot first subject
plot_matrix(corr_connectivities[0], title="Correlation")
plot_matrix(pcorr_connectivities[0], title="Partial Correlation")
plot_matrix(tangent_connectivities[0], title="Tangent Embedding")
plot_matrix(shrunk_connectivities[0], title="PoSCE")
