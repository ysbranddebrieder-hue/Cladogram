import streamlit as st
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")
st.title("Ultieme Cladogram Generator")

# 1. De Data (Matrix) - Standaard voorbeeld
data = {
    'Wervels': [1, 1, 1, 1, 0],
    'Longen':  [1, 1, 1, 0, 0],
    'Haar':    [1, 1, 0, 0, 0],
    'Duim':    [1, 0, 0, 0, 0]
}
index = ['Mens', 'Hond', 'Hagedis', 'Vis', 'Vlieg']
df = pd.DataFrame(data, index=index)

st.subheader("1. Karaktermatrix aanpassen")
st.write("Verander de 1-en en 0-en om de evolutie te beïnvloeden.")
edited_df = st.data_editor(df, use_container_width=True)

if st.button("🔄 Genereer Gecorrigeerd Cladogram"):
    try:
        # We sorteren de data eerst op aantal kenmerken voor een stabielere boom
        sorted_df = edited_df.iloc[np.argsort(edited_df.sum(axis=1))]

        # 'weighted' en 'optimal_ordering' zorgen voor de juiste plaatsing van soorten
        Z = linkage(sorted_df, method='weighted', optimal_ordering=True)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Teken de boom
        ddata = dendrogram(
            Z, 
            labels=sorted_df.index, 
            orientation='right', 
            ax=ax,
            above_threshold_color='black'
        )
        
        # Eigenschappen op de kruispunten plaatsen
        # We kijken welke eigenschap per stap 'bijkomt'
        kenmerken = sorted_df.columns
        for i, node in enumerate(Z):
            # Bereken positie van het kruispunt
            x_pos = node[2]
            y_pos = np.mean(ddata['icoord'][i][1:3])
            
            # Label toevoegen (gebaseerd op kolomvolgorde)
            if i < len(kenmerken):
                label = kenmerken[i]
                ax.plot(x_pos, y_pos, '|', color='red', markersize=15, markeredgewidth=3)
                ax.text(x_pos + 0.1, y_pos, f" {label}", color='red', 
                        fontweight='bold', va='center', fontsize=11)

        ax.set_title("Cladogram met evolutionaire innovaties", fontsize=15)
        ax.set_xlabel("Evolutionaire afstand")
        
        # Toon de plot
        st.pyplot(fig)
        
        st.success("Boom succesvol gegenereerd. De mens en hond staan nu correct gegroepeerd!")

    except Exception as e:
        st.error(f"Fout bij het genereren: {e}")

st.info("Tip: Als de mens en hond nog steeds wisselen, voeg dan een extra kolom toe (bijv. 'Taal') waar de Mens een 1 heeft en de Hond een 0.")
