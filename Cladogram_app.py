 import streamlit as st
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

st.set_page_config(layout="wide")
st.title("Diagonaal Vertebrata Cladogram")

# 1. Data voor Vertebrata (Nu met ingevulde waarden om de error te voorkomen)
data = {
    'Wervels': [1, 1, 1, 1, 1, 0],
    'Kaken':   [1, 1, 1, 1, 0, 0],
    'Poten':   [1, 1, 1, 0, 0, 0],
    'Amnion':  [1, 1, 0, 0, 0, 0],
    'Haar/Melk':[1, 0, 0, 0, 0, 0]
}
index = ['Mens', 'Krokodil', 'Kikker', 'Haai', 'Prik', 'Vlieg']
df = pd.DataFrame(data, index=index)

st.subheader("1. Karaktermatrix")
edited_df = st.data_editor(df, use_container_width=True)

if st.button("🔄 Teken Diagonaal Cladogram"):
    try:
        # Sorteer op complexiteit
        sorted_df = edited_df.iloc[np.argsort(edited_df.sum(axis=1))]
        Z = linkage(sorted_df, method='weighted', optimal_ordering=True)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Bereken de boom coördinaten
        ddata = dendrogram(Z, labels=sorted_df.index, no_plot=True)

        # Teken handmatig de schuine lijnen
        for icoord, dcoord in zip(ddata['icoord'], ddata['dcoord']):
            x = [icoord[0], (icoord[1] + icoord[2]) / 2, icoord[3]]
            y = [dcoord[0], dcoord[1], dcoord[3]]
            ax.plot(x, y, color='black', lw=2)

        # Kenmerken toevoegen op de knooppunten
        kenmerken = sorted_df.columns
        for i, (icoord, dcoord) in enumerate(zip(ddata['icoord'], ddata['dcoord'])):
            if i < len(kenmerken):
                x_node = (icoord[1] + icoord[2]) / 2
                y_node = dcoord[1]
                ax.plot(x_node, y_node, 'ro', markersize=8)
                ax.text(x_node + 2, y_node, f" {kenmerken[i]}", 
                        color='red', fontweight='bold', va='center')

        # X-as instellen voor de dierennamen
        ax.set_xticks(np.arange(5, len(sorted_df) * 10 + 5, 10))
        ax.set_xticklabels(ddata['ivl'], rotation=45, ha='right')

        # Layout opschonen
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_yticks([])
        
        st.pyplot(fig)
        
        # Download knop
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight')
        st.download_button("💾 Download Diagonaal Cladogram", buf.getvalue(), "diagonaal_cladogram.png")
        
    except Exception as e:
        st.error(f"Fout: {e}")
