import streamlit as st
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cladogram Maker", layout="wide")

st.title("🌿 Mobiele Cladogram Generator")
st.write("Voer soorten en eigenschappen in en vink de matrix aan.")

# 1. Input sectie (altijd bovenaan)
soorten_input = st.text_input("Soorten (gescheiden door komma's):", "Hond, Kat, Vis, Mens")
eigenschappen_input = st.text_input("Eigenschappen (gescheiden door komma's):", "Haar, Vinnen, Longen")

# Variabelen direct definiëren om NameError te voorkomen
soorten = [s.strip() for s in soorten_input.split(",") if s.strip()]
eigenschappen = [e.strip() for e in eigenschappen_input.split(",") if e.strip()]

# 2. Matrix invullen
if len(soorten) < 2:
    st.warning("Vul minimaal 2 soorten in.")
    st.stop()

st.subheader("Eigenschappen Matrix")
# Maak kolommen voor een mobielvriendelijke weergave
matrix_data = {}
cols = st.columns(len(soorten))
for i, s in enumerate(soorten):
    with cols[i]:
        st.write(f"**{s}**")
        matrix_data[s] = [st.checkbox(f"{e}", key=f"{s}_{e}") for e in eigenschappen]

# Maak de DataFrame (Soorten als rijen, Eigenschappen als kolommen)
df = pd.DataFrame(matrix_data, index=eigenschappen).T

# 3. Berekening en Tekenen
if st.button("Genereer Cladogram"):
    # Labels maken voor de uiteinden: "Soort (Kenmerken)"
    nieuwe_labels = []
    for s in soorten:
        soort_traits = df.loc[s]
        actieve_traits = soort_traits[soort_traits].index.tolist()
        if actieve_traits:
            label = f"{s}\n({', '.join(actieve_traits)})"
        else:
            label = s
        nieuwe_labels.append(label)

    # Bereken de boom (Ward's methode is goed voor dit soort clusters)
    # We gebruiken de numerieke data (0 en 1)
    Z = linkage(df.astype(int), method='ward')
    
    # Plot maken
    fig, ax = plt.subplots(figsize=(10, 8))
    ddata = dendrogram(Z, labels=nieuwe_labels, orientation='top', ax=ax)
    
    # Knooppunten (Nodes) analyseren voor eigenschappen
    n_species = len(df)
    # clusters houdt bij welke soort-indices onder welk knooppunt vallen
    clusters = {i: [i] for i in range(n_species)}
    
    for i, merge in enumerate(Z):
        node_id = n_species + i
        child1, child2 = int(merge[0]), int(merge[1])
        members = clusters[child1] + clusters[child2]
        clusters[node_id] = members
        
        # Welke eigenschappen hebben ALLE soorten in deze tak?
        common_traits = df.iloc[members].all()
        traits_list = common_traits[common_traits].index.tolist()
        
        # Coördinaten van de splitsing
        x = 0.5 * sum(ddata['icoord'][i][1:3])
        y = ddata['dcoord'][i]
        
        if traits_list:
            plt.plot(x, y, 'ro', markersize=6)
            plt.annotate("\n".join(traits_list), (x, y), xytext=(5, 5), 
                         textcoords='offset points', fontsize=9, 
                         color='blue', fontweight='bold', ha='left')

    # Opmaak voor mobiel (schuine tekst)
    plt.xticks(rotation=45, ha='right')
    plt.title("Cladogram: Rode stippen markeren gedeelde eigenschappen")
    plt.tight_layout()
    
    st.pyplot(fig)
