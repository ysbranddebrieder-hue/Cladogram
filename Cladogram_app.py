import streamlit as st
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

st.set_page_config(page_title="Evolutie Cladogram", layout="wide")

st.title("🌿 Slim Cladogram")
st.write("De app berekent automatisch waar eigenschappen in de stamboom verschijnen.")

# 1. Input sectie
col1, col2 = st.columns(2)
with col1:
    soorten_input = st.text_input("Soorten (komma-gescheiden):", "Hond, Kat, Vis, Mens")
with col2:
    eigenschappen_input = st.text_input("Eigenschappen (komma-gescheiden):", "Haar, Vinnen, Longen")

soorten = [s.strip() for s in soorten_input.split(",")]
eigenschappen = [e.strip() for e in eigenschappen_input.split(",")]

# 2. Karakter Matrix Invullen
st.subheader("Vink aan wat van toepassing is:")
data = {}
cols = st.columns(len(soorten))
for i, s in enumerate(soorten):
    with cols[i]:
        st.write(f"**{s}**")
        data[s] = [st.checkbox(f"{e}", key=f"{s}_{e}") for e in eigenschappen]

df = pd.DataFrame(data, index=eigenschappen).T

# 3. Berekening en Visualisatie
if st.button("Genereer Cladogram met Labels"):
    if len(soorten) < 2:
        st.error("Voeg meer soorten toe.")
    else:
        # Bereken de boomstructuur
        Z = linkage(df.astype(int), method='ward')
        
        fig, ax = plt.subplots(figsize=(10, 7))
        ddata = dendrogram(Z, labels=df.index, orientation='top', ax=ax)
        
        # Logica om eigenschappen aan knooppunten te koppelen
        n_species = len(df)
        clusters = {i: [i] for i in range(n_species)}
        
        # Loop door de splitsingen in de boom
        for i, merge in enumerate(Z):
            node_id = n_species + i
            child1, child2 = int(merge[0]), int(merge[1])
            members = clusters[child1] + clusters[child2]
            clusters[node_id] = members
            
            # Zoek eigenschappen die ALLE leden van dit cluster hebben
            common_traits = df.iloc[members].all()
            traits_list = common_traits[common_traits].index.tolist()
            
            # Verwijder eigenschappen die al bij een 'hoger' (eerder) knooppunt horen
            # (Heel simpel: toon alleen de eerste keer dat een eigenschap verschijnt)
            
            # Vind de coördinaten voor dit knooppunt in de plot
            x = 0.5 * sum(ddata['icoord'][i][1:3])
            y = ddata['dcoord'][i][1]
            
            if traits_list:
                label = "\n".join(traits_list)
                plt.plot(x, y, 'ro', markersize=6)
                plt.annotate(label, (x, y), xytext=(5, 5), 
                             textcoords='offset points', fontsize=9, 
                             color='blue', fontweight='bold', ha='left')

        plt.title("Cladogram: Blauwe tekst toont nieuwe eigenschappen")
        st.pyplot(fig)
