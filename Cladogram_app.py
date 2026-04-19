import streamlit as st
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

st.set_page_config(layout="wide")
st.title("Diagonaal Vertebrata Cladogram")

# 1. Data voor Vertebrata
data = {
    'Wervels': ,
    'Kaken':   ,
    'Poten':   ,
    'Amnion':  ,
    'Haar/Melk':
}
index = ['Mens', 'Hond', 'Krokodil', 'Kikker', 'Haai', 'Prik']
df = pd.DataFrame(data, index=index)

st.subheader("1. Karaktermatrix")
edited_df = st.data_editor(df, use_container_width=True)

if st.button("🔄 Teken Diagonaal Cladogram"):
    try:
        # Sorteer op complexiteit (aantal 1-en)
        sorted_df = edited_df.iloc[np.argsort(edited_df.sum(axis=1))]
        Z = linkage(sorted_df, method='weighted', optimal_ordering=True)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # We vangen de data op zonder direct te plotten
        ddata = dendrogram(Z, labels=sorted_df.index, no_plot=True)

        # Teken handmatig de schuine (diagonale) lijnen
        for icoord, dcoord in zip(ddata['icoord'], ddata['dcoord']):
            # Maak een V-vorm van de takken
            x = [icoord[0], (icoord[0] + icoord[3]) / 2, icoord[3]]
            y = [dcoord[0], dcoord[1], dcoord[3]]
            ax.plot(x, y, color='black', lw=2)

        # Plaats eigenschappen op de knooppunten
        kenmerken = sorted_df.columns
        for i, (icoord, dcoord) in enumerate(zip(ddata['icoord'], ddata['dcoord'])):
            if i < len(kenmerken):
                x_node = (icoord[0] + icoord[3]) / 2
                y_node = dcoord[1]
                ax.plot(x_node, y_node, 'ro', markersize=8)
                ax.text(x_node + 2, y_node, f" {kenmerken[i]}", 
                        color='red', fontweight='bold', va='center')

        # FIX voor de Error: Gebruik de individuele blad-posities voor de X-as
        leaf_positions = np.array([ (icoord[0] if dcoord[0] == 0 else icoord[3]) 
                                   for icoord, dcoord in zip(ddata['icoord'], ddata['dcoord']) 
                                   if dcoord[0] == 0 or dcoord[3] == 0 ])
        
        # Zorg dat we alleen unieke posities voor de labels gebruiken
        unique_pos = np.unique(np.array(ddata['icoord']).flatten())
        ax.set_xticks(np.arange(5, len(sorted_df) * 10 + 5, 10))
        ax.set_xticklabels(ddata['ivl'], rotation=45, ha='right')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_yticks([]) # Verwijder y-as voor een cleaner uiterlijk
        
        st.pyplot(fig)
        
        # Downloadoptie
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight')
        st.download_button("💾 Download Diagonaal Cladogram", buf.getvalue(), "diagonaal_cladogram.png")
        
    except Exception as e:
        st.error(f"Fout: {e}")
