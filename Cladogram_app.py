import streamlit as st
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cladogram Maker", layout="wide")

st.title("🌿 Mobiele Cladogram Generator")

# 1. Input
soorten_input = st.text_input("Soorten:", "Hond, Kat, Vis, Mens")
eigenschappen_input = st.text_input("Eigenschappen:", "Haar, Vinnen, Longen")

soorten = [s.strip() for s in soorten_input.split(",") if s.strip()]
eigenschappen = [e.strip() for e in eigenschappen_input.split(",") if e.strip()]

if len(soorten) < 2:
    st.warning("Vul minimaal 2 soorten in.")
    st.stop()

# 2. Matrix
st.subheader("Vink eigenschappen aan:")
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
    
    # We houden bij welke eigenschappen we al getoond hebben om dubbelingen te voorkomen
    getoonde_eigenschappen = set()

    for i, merge in enumerate(Z):
        node_id = n_species + i
        child1, child2 = int(merge[0]), int(merge[1])
        members = clusters[child1] + clusters[child2]
        clusters[node_id] = members
        
        # Welke eigenschappen delen deze leden?
        common_traits = df.iloc[members].all()
        traits_list = [t for t in common_traits[common_traits].index.tolist() if t not in getoonde_eigenschappen]
        
        # Haal de X en Y coordinaten op voor het horizontale middenstuk
        # ddata['icoord'][i] en ddata['dcoord'][i] zijn lijsten van 4 punten
        x_val = 0.5 * (ddata['icoord'][i][1] + ddata['icoord'][i][2])
        y_val = ddata['dcoord'][i][1] # De hoogte van de horizontale lijn
        
        if traits_list:
            ax.plot(x_val, y_val, 'ro', markersize=6)
            ax.annotate(", ".join(traits_list), (x_val, y_val), 
                         xytext=(5, 5), textcoords='offset points', 
                         fontsize=9, color='blue', fontweight='bold')
            # Voeg toe aan getoond zodat ze niet lager in de boom weer verschijnen
            for t in traits_list:
                getoonde_eigenschappen.add(t)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)
