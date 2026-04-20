import streamlit as st
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cladogram Maker", layout="wide")

st.title("🌿 Cladogram met Knooppunt-Eigenschappen")

# 1. Input
soorten_input = st.text_input("Soorten:", "Hond, Kat, Vis, Mens")
eigenschappen_input = st.text_input("Eigenschappen:", "Haar, Vinnen, Longen, Duim")

soorten = [s.strip() for s in soorten_input.split(",") if s.strip()]
eigenschappen = [e.strip() for e in eigenschappen_input.split(",") if e.strip()]

if len(soorten) < 2:
    st.warning("Voeg minimaal 2 soorten toe.")
    st.stop()

# 2. Matrix
st.subheader("Matrix invullen")
matrix_data = {}
cols = st.columns(len(soorten))
for i, s in enumerate(soorten):
    with cols[i]:
        st.write(f"**{s}**")
        matrix_data[s] = [st.checkbox(f"{e}", key=f"{s}_{e}") for e in eigenschappen]

df = pd.DataFrame(matrix_data, index=eigenschappen).T

# 3. Berekening en Tekenen
if st.button("Genereer Cladogram"):
    # Labels voor uiteinden
    nieuwe_labels = []
    for s in soorten:
        actieve = df.columns[df.loc[s]].tolist()
        label = f"{s}\n({', '.join(actieve)})" if actieve else s
        nieuwe_labels.append(label)

    # Dendrogram berekenen
    Z = linkage(df.astype(int), method='ward')
    fig, ax = plt.subplots(figsize=(10, 8))
    ddata = dendrogram(Z, labels=nieuwe_labels, orientation='top', ax=ax)
    
    # Knooppunten analyseren
    n_species = len(df)
    clusters = {i: [i] for i in range(n_species)}
    
    # We lopen door de stamboom-splitsingen
    for i, merge in enumerate(Z):
        node_id = n_species + i
        # Haal de twee takken op (links en rechts)
        child1_id = int(merge[0])
        child2_id = int(merge[1])
        
        # Voeg de soorten van beide takken samen voor dit nieuwe knooppunt
        members = clusters[child1_id] + clusters[child2_id]
        clusters[node_id] = members
        
        # Welke eigenschappen delen ALLE soorten in dit specifieke cluster?
        common_traits = df.iloc[members].all()
        traits_list = common_traits[common_traits].index.tolist()
        
        # Coördinaten bepalen:
        # icoord[i][1:3] geeft de x-waarden van de horizontale lijn van de 'U'
        # dcoord[i][1] geeft de y-waarde (hoogte) van die horizontale lijn
        x_val = sum(ddata['icoord'][i][1:3]) / 2
        y_val = ddata['dcoord'][i][1]
        
        if traits_list:
            # Teken stip
            ax.plot(x_val, y_val, 'ro', markersize=6)
            # Zet alle gedeelde eigenschappen bij dit knooppunt
            label_text = "\n".join(traits_list)
            ax.annotate(label_text, (x_val, y_val), 
                         xytext=(5, 5), textcoords='offset points', 
                         fontsize=9, color='blue', fontweight='bold',
                         bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.7))

    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Afstand (Verschil)")
    plt.tight_layout()
    st.pyplot(fig)
