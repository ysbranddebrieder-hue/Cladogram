import streamlit as st
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

st.set_page_config(layout="wide")
st.title("Diagonaal Vertebrata Cladogram")

# 1. Data voor Vertebrata (Gevuld om SyntaxErrors te voorkomen)
data = {
    'Wervelkolom': [0, 1, 1, 1, 1, 1],
    'Kaken':       [0, 0, 1, 1, 1, 1],
    'Poten':       [0, 0, 0, 1, 1, 1],
    'Amnion':      [0, 0, 0, 0, 1, 1],
    'Haar/Melk':   [0, 0, 0, 0, 0, 1]
}
index = ['Fruitvlieg', 'Prik', 'Haai', 'Kikker', 'Krokodil', 'Mens']
df = pd.DataFrame(data, index=index)

st.subheader("1. Karaktermatrix")
edited_df = st.data_editor(df, use_container_width=True)

if st.button("🔄 Teken Diagonaal Cladogram"):
    try:
        # Sorteren op complexiteit
        sorted_df = edited_df.iloc[np.argsort(edited_df.sum(axis=1))]
        Z = linkage(sorted_df, method='weighted', optimal_ordering=True)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ddata = dendrogram(Z, labels=sorted_df.index, no_plot=True)

        # 2. Teken handmatig de schuine lijnen (Ladder-stijl)
        for icoord, dcoord in zip(ddata['icoord'], ddata['dcoord']):
            # FIX: We pakken de individuele waarden uit de lijst icoord
            # icoord[1] en icoord[2] zijn de middelste punten van de tak
            x = [icoord[0], (icoord[1] + icoord[2]) / 2, icoord[3]]
            y = [dcoord[0], dcoord[1], dcoord[3]]
            ax.plot(x, y, color='black', lw=2.5)

        # 3. Kenmerken toevoegen op de splitsingen
        kenmerken = sorted_df.columns
        for i, (icoord, dcoord) in enumerate(zip(ddata['icoord'], ddata['dcoord'])):
            if i < len(kenmerken):
                x_node = (icoord[1] + icoord[2]) / 2
                y_node = dcoord[1]
                ax.plot(x_node, y_node, 'ro', markersize=8)
                ax.text(x_node + 2, y_node, f" {kenmerken[i]}", 
                        color='red', fontweight='bold', va='center')

        # 4. Namen van de dieren onderaan
        x_ticks = np.arange(5, len(sorted_df) * 10, 10)
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(ddata['ivl'], rotation=45, ha='right')

        # Layout opschonen
        ax.axis('off')
        st.pyplot(fig)
        
        # Download knop
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight')
        st.download_button("💾 Download PNG", buf.getvalue(), "cladogram.png", "image/png")
        
    except Exception as e:
        st.error(f"Fout: {e}")
