import streamlit as st
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

st.set_page_config(layout="wide")
st.title("Diagonaal Vertebrata Cladogram")

# 1. Data
data = {
    'Wervels':  [1, 1, 1, 1, 1, 0],
    'Kaken':    [1, 1, 1, 1, 0, 0],
    'Poten':    [1, 1, 1, 0, 0, 0],
    'Amnion':   [1, 1, 0, 0, 0, 0],
    'Haar/Melk':[1, 0, 0, 0, 0, 0]
}
index = ['Mens', 'Hagedis', 'Kikker', 'Haai', 'Prik', 'Vlieg']
df = pd.DataFrame(data, index=index)

st.subheader("1. Karaktermatrix")
edited_df = st.data_editor(df, use_container_width=True)

if st.button("🔄 Teken Diagonaal Cladogram"):
    try:
        # Sorteer op complexiteit
        sorted_df = edited_df.iloc[np.argsort(edited_df.sum(axis=1))]
        Z = linkage(sorted_df, method='weighted', optimal_ordering=True)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 'link_color_func' gebruiken we om alle lijnen zwart te maken
        # 'orientation=top' is de basis, maar we passen de tekenstijl aan
        ddata = dendrogram(
            Z, 
            labels=sorted_df.index, 
            orientation='top', 
            ax=ax,
            no_plot=True # We vangen de data op om zelf schuin te tekenen
        )

        # Teken handmatig de schuine lijnen (Slanted style)
        for icoord, dcoord in zip(ddata['icoord'], ddata['dcoord']):
            x = [icoord[0], (icoord[1]+icoord[2])/2, icoord[3]]
            y = [dcoord[0], dcoord[1], dcoord[3]]
            ax.plot(x, y, color='black', lw=2)

        # Voeg labels voor eigenschappen toe op de schuine ruggengraat
        kenmerken = sorted_df.columns
        for i, (icoord, dcoord) in enumerate(zip(ddata['icoord'], ddata['dcoord'])):
            if i < len(kenmerken):
                x_mid = (icoord[1] + icoord[2]) / 2
                y_mid = dcoord[1]
                ax.plot(x_mid, y_mid, 'ro', markersize=8)
                ax.text(x_mid + 2, y_mid, f" {kenmerken[i]}", color='red', fontweight='bold')

        # Opmaak
        ax.set_xticks(ddata['icoord'])
        ax.set_xticklabels(ddata['ivl'], rotation=45, ha='right')
        ax.axis('off')
        st.pyplot(fig)
        
        # Download
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight')
        st.download_button("💾 Download Diagonaal Cladogram", buf.getvalue(), "slanted_cladogram.png")
        
    except Exception as e:
        st.error(f"Fout: {e}")
