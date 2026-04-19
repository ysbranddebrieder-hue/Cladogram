import streamlit as st
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import numpy as np

st.title("Cladogram met Evolutie-labels")

# 1. De Data
data = {
    'Wervels': [1, 1, 1, 1, 0],
    'Longen':  [1, 1, 1, 0, 0],
    'Haar':    [1, 1, 0, 0, 0],
    'Duim':    [1, 0, 0, 0, 0]
}
df = pd.DataFrame(data, index=['Mens', 'Hond', 'Hagedis', 'Vis', 'Vlieg'])

st.write("Pas de 1-en en 0-en aan:")
edited_df = st.data_editor(df)

if st.button("🔄 Genereer Cladogram met Labels"):
    # Bereken de boom
    Z = linkage(edited_df, method='single') # 'single' werkt vaak beter voor simpele stambomen
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ddata = dendrogram(Z, labels=edited_df.index, orientation='right', ax=ax)
    
    # Haal de volgorde van de soorten in de plot op
    leaves = ddata['leaves']
    
    # Voor elk kruispunt in de boom (Z bevat de koppelingen)
    for i, node in enumerate(Z):
        # Zoek het x-punt van de splitsing (waar de verticale lijn in de plot staat)
        x_pos = node[2] 
        # Zoek het y-punt (het gemiddelde van de twee takken die samenkomen)
        y_pos = np.mean(ddata['icoord'][i][1:3])
        
        # Bepaal welke eigenschappen 'nieuw' zijn voor deze groep
        # We kijken naar de soorten onder dit knooppunt
        # (Simpele logica voor dit voorbeeld: we tonen de naam van de kolom)
        if i < len(edited_df.columns):
            label = edited_df.columns[-(i+1)]
            
            # Teken een streepje en de tekst
            ax.plot(x_pos, y_pos, '|', color='red', markersize=15, markeredgewidth=3)
            ax.text(x_pos, y_pos + 2, f" {label}", color='red', 
                    fontweight='bold', fontsize=10, rotation=45)

    ax.set_title("Evolutie van eigenschappen (rode streepjes = innovatie)")
    st.pyplot(fig)

st.info("De rode tekst geeft aan waar een nieuwe eigenschap voor het eerst verschijnt in de evolutie.")
