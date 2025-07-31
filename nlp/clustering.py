from sentence_transformers import SentenceTransformer
import umap
import hdbscan
import numpy as np
import pandas as pd

# Load transformer model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(texts):
    return model.encode(texts, show_progress_bar=True)

def cluster_embeddings(embeddings, min_cluster_size=5):
    reducer = umap.UMAP(n_neighbors=15, n_components=5, metric='cosine')
    reduced = reducer.fit_transform(embeddings)

    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, metric='euclidean', cluster_selection_method='eom')
    labels = clusterer.fit_predict(reduced)

    return labels, reduced

def label_complaint_clusters(df):
    if df.empty or 'Summary' not in df.columns:
        return df, {}

    texts = df['Summary'].astype(str).tolist()
    embeddings = generate_embeddings(texts)
    labels, reduced = cluster_embeddings(embeddings)

    df['Cluster'] = labels
    df['UMAP1'] = reduced[:, 0]
    df['UMAP2'] = reduced[:, 1]

    cluster_summary = df.groupby('Cluster').agg({
        'Summary': lambda x: ' | '.join(x.head(3)),
        'ODINumber': 'count'
    }).rename(columns={'ODINumber': 'NumComplaints'}).reset_index()

    return df, cluster_summary
