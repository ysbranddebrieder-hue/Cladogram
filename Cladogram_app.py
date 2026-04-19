import streamlit as st
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

st.title("Cladogram met Eigenschappen op de Takken")

# 1. De Data (Matrix)
data = {
    'Wervels': [1, 1, 1, 1, 0],
    'Longen':  [1, 1, 1, 0, 0],
    'Haar':    [1, 1, 0, 0, 0],
    'Duim':    [1, 0, 0, 0, 0]
}
df = pd.DataFrame(data, index=['Mens', 'Hond', 'Hagedis', 'Vis', 'Vlieg'])

edited_df = st.data_editor(df)

if st.button("🔄 Teken Cladogram"):
    Z = linkage(edited_df, method='ward')
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Dendrogram tekenen
    ddata = dendrogram(Z, labels=edited_df.index, orientation='right', ax=ax)
    
    # Eigenschappen op de kruispunten plaatsen
    # We lopen door de 'icoords' en 'dcoords' van de getekende lijnen
    for i, d, val in zip(ddata['icoord'], ddata['dcoord'], Z):
        # Het kruispunt (node) ligt op het punt waar de horizontale lijn stopt
        x = d[1] 
        y = i[1]
        
        # Logica: Welke eigenschappen horen hier?
        # Voor dit simpele voorbeeld zetten we een label bij de splitsing
        ax.plot(x, y, 'ro') # Rood puntje op het kruispunt
        ax.text(x, y, f" 🚩 Overgang", fontsize=9, verticalalignment='bottom')

    ax.set_title("Eigenschappen per splitsing")
    st.pyplot(fig)

st.info("De rode punten geven aan waar een evolutionaire verandering plaatsvindt.")
