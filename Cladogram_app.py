import streamlit as st
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

st.set_page_config(layout="wide")
st.title("Verticaal Cladogram (Gecorrigeerd)")

# 1. Data
data = {
    'Wervelkolom': [1, 1, 1, 1, 1, 0],
    'Kaken':      [1, 1, 1, 1, 0, 0],
    'Poten':      [1, 1, 1, 0, 0, 0],
    'Amnion':     [1, 1, 0, 0, 0, 0],
    'Haar/Melk':  [1, 0, 0, 0, 0, 0]
}
index = ['Mens', 'Hond', 'Kikker', 'Haai', 'Prik', 'Vlieg']
df = pd.DataFrame(data, index=index)

st.subheader("1. Karaktermatrix")
edited_df = st.data_editor(df, use_container_width=True)

if st.button("🔄 Teken Verticaal Cladogram"):
    try:
        # Sorteren
        sorted_df = edited_df.iloc[np.argsort(edited_df.sum(axis=1))]
        Z = linkage(sorted_df, method='weighted', optimal_ordering=True)
        
        fig, ax = plt.subplots(figsize=(12, 10))
        ddata = dendrogram(Z, labels=sorted_df.index, orientation='top', ax=ax)
        
        # FIX: We lopen door de getekende lijnen van het dendrogram
        # ddata['icoord'] bevat de x-posities, ddata['dcoord'] de y-posities (hoogtes)
        kenmerken = sorted_df.columns
        
        # We pakken alleen de horizontale tussenstukken (waar de innovatie zit)
        for i in range(len(ddata['icoord'])):
            x_pos = np.mean(ddata['icoord'][i][1:3])
            y_pos = ddata['dcoord'][i][1] # De hoogte van de horizontale balk
            
            # Plaats alleen labels zolang we kenmerken hebben
            if i < len(kenmerken):
                label = kenmerken[i]
                ax.plot([x_pos], [y_pos], '_', color='red', markersize=30, markeredgewidth=5)
                ax.text(x_pos, y_pos + 0.1, label, color='red', fontweight='bold', ha='center')

        ax.set_title("Evolutie van de Vertebrata", fontsize=18)
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        # Download knop
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight')
        st.download_button("💾 Download PNG", buf.getvalue(), "cladogram.png", "image/png")
        
    except Exception as e:
        st.error(f"Fout: {e}")
