import streamlit as st
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

st.set_page_config(layout="wide")
st.title("Biologisch Diagonaal Cladogram")

# 1. Data
data = {
    'Wervelkolom':,
    'Kaken':     ,
    'Poten':     ,
    'Amnion':    ,
    'Haar/Melk': 
}
index = ['Mens', 'Hond', 'Kikker', 'Haai', 'Prik', 'Fruitvlieg']
df = pd.DataFrame(data, index=index)

st.subheader("1. Bewerk de Matrix")
edited_df = st.data_editor(df, use_container_width=True)

if st.button("🔄 Teken Diagonaal Cladogram"):
    try:
        # Sorteer op complexiteit voor de 'ladder' look
        sorted_df = edited_df.iloc[np.argsort(edited_df.sum(axis=1))]
        Z = linkage(sorted_df, method='single')
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Gebruik de 'top' oriëntatie en teken de lijnen handmatig schuin
        ddata = dendrogram(Z, labels=sorted_df.index, no_plot=True)

        # De 'ladder' tekenen
        for icoord, dcoord in zip(ddata['icoord'], ddata['dcoord']):
            # We verbinden de punten diagonaal in plaats van met blokken
            x = [icoord, (icoord + icoord) / 2, icoord]
            y = [dcoord, dcoord, dcoord]
            ax.plot(x, y, color='black', lw=2.5)

        # Labels op de juiste plekken (de rode innovaties)
        kenmerken = sorted_df.columns
        for i in range(len(Z)):
            x_pos = (ddata['icoord'][i] + ddata['icoord'][i]) / 2
            y_pos = ddata['dcoord'][i]
            
            if i < len(kenmerken):
                ax.plot(x_pos, y_pos, 'ro', markersize=10)
                ax.text(x_pos + 1, y_pos, f" {kenmerken[i]}", 
                        color='red', fontweight='bold', va='center', fontsize=12)

        # Fix de onderkant (namen van de dieren)
        ax.set_xticks(np.arange(5, len(sorted_df) * 10, 10))
        ax.set_xticklabels(ddata['ivl'], rotation=45, ha='right', fontsize=12)

        # Layout styling: maak het schoon
        ax.set_facecolor('white')
        ax.axis('off') # Verwijder alle lelijke assen en lijnen
        
        st.pyplot(fig)
        
        # Download
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight', transparent=False, facecolor='white')
        st.download_button("💾 Download deze afbeelding", buf.getvalue(), "cladogram.png")
        
    except Exception as e:
        st.error(f"Er ging iets mis bij het tekenen: {e}")

st.info("De rode stippen geven de 'knopen' aan waar een nieuwe eigenschap is ontstaan.")
