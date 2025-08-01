from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st

def show_cluster_wordclouds(df, text_col='Summary', cluster_col='Cluster'):
    st.subheader("🔤 Word Clouds by Cluster")
    clusters = df[cluster_col].dropna().unique()
    
    for cluster in clusters:
        cluster_texts = df[df[cluster_col] == cluster][text_col].dropna().str.cat(sep=' ')
        if cluster_texts.strip():
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(cluster_texts)
            st.markdown(f"**Cluster {cluster}**")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
