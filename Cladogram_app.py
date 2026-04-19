import streamlit as st
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

st.set_page_config(layout="wide")
st.title("Verticaal Cladogram met Downloadoptie")

# 1. De Biologische Data (Vertebrata)
data = {
    'Wervelkolom': [1, 1, 1, 1, 1, 1],
    'Kaken':      [0, 1, 1, 1, 1, 1],
    'Poten':      [0, 0, 1, 1, 1, 1],
    'Amnion (ei)': [0, 0, 0, 1, 1, 1],
    'Haar/Melk':  [0, 0, 0, 0, 1, 1],
    'Rechtop':    [0, 0, 0, 0, 0, 1]
}
index = ['Prik', 'Haai', 'Kikker', 'Krokodil', 'Hond', 'Mens']
df = pd.DataFrame(data, index=index)

st.subheader("1. Bewerk de Karaktermatrix")
edited_df = st.data_editor(df, use_container_width=True)

if st.button("🔄 Teken Verticaal Cladogram"):
    try:
        # Sorteren en boom berekenen
        sorted_df = edited_df.iloc[np.argsort(edited_df.sum(axis=1))]
        Z = linkage(sorted_df, method='weighted', optimal_ordering=True)
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Teken de verticale boom
        ddata = dendrogram(
            Z, 
            labels=sorted_df.index, 
            orientation='top', 
            ax=ax,
            above_threshold_color='black'
        )
        
        # Labels en rode streepjes toevoegen
        kenmerken = sorted_df.columns
        for i, node in enumerate(Z):
            x_pos = np.mean(ddata['icoord'][i][1:3])
            y_pos = node
            
            if i < len(kenmerken):
                label = kenmerken[i]
                ax.plot(x_pos, y_pos, '_', color='red', markersize=30, markeredgewidth=5)
                ax.text(x_pos, y_pos + 0.15, label, color='red', 
                        fontweight='bold', fontsize=11, ha='center')

        ax.set_title("Evolutie van de Vertebrata", fontsize=18)
        ax.set_ylabel("Evolutionaire afstand")
        plt.xticks(rotation=45)
        
        # Toon de plot in de app
        st.pyplot(fig)
        
        # --- DOWNLOAD LOGICA ---
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight', dpi=300)
        st.download_button(
            label="💾 Download Cladogram als PNG",
            data=buf.getvalue(),
            file_name="vertebrata_cladogram.png",
            mime="image/png"
        )
        
    except Exception as e:
        st.error(f"Fout: {e}")

st.info("Klik op de knop hierboven om de afbeelding op te slaan na het genereren.")
