#%% imports
import pandas as pd
import matplotlib.pyplot as plt
import os


#%%
working_dir="/b/Dropbox/jgt/drop"
# Load the data from the CSV file
filename_to_observe= "jgtml_observe_dataset__240515_valid_BIG_alligator_SELL.result.csv"
fullpath_of_file_to_observe =os.path.join(working_dir, filename_to_observe)

data = pd.read_csv(fullpath_of_file_to_observe)

#/var/lib/jgt/full/data/targets/mx/SPX500_D1.csv

#%%

#%% Create a scatter plot of the per_trade vs nb_entry
plt.scatter(data["per_trade"], data["nb_entry"])
plt.xlabel("per_trade")
plt.ylabel("nb_entry")
plt.show()

#%% Create a histogram of the tsum
plt.hist(data["tsum"], bins=20)
plt.xlabel("tsum")
plt.ylabel("Frequency")
plt.show()

#%% Create a box plot of the tsum for different instruments
plt.boxplot([data[data["instrument"]==i]["tsum"] for i in data["instrument"].unique()], showmeans=True)
plt.xlabel("instrument")
plt.ylabel("tsum")
plt.show()

#%% Create a heatmap of the correlation between the features
plt.imshow(data.corr(), cmap="coolwarm")
plt.colorbar()
plt.show()

#%% Perform a principal component analysis (PCA)
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
pca.fit(data[["per_trade", "nb_entry", "tsum"]])
pca_data = pca.transform(data[["per_trade", "nb_entry", "tsum"]])

#%% Create a scatter plot of the PCA components
plt.scatter(pca_data[:, 0], pca_data[:, 1])
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.show()

#%% Perform a k-means clustering
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3)
kmeans.fit(pca_data)

#%% Create a scatter plot of the clusters
plt.scatter(pca_data[:, 0], pca_data[:, 1], c=kmeans.labels_)
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.show()
# %%
