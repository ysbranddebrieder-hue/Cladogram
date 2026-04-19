import streamlit as st
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cladogram met Eigenschappen")

st.title("🌿 Cladogram met Kenmerken")
st.write("Vink de eigenschappen aan om te zien waar ze in de evolutie verschijnen.")

# Input
soorten_input = st.text_input("Soorten:", "Hond, Kat, Vis, Mens")
eigenschappen_input = st.text_input("Eigenschappen:", "Haar, Vinnen, Longen")

soorten = [s.strip() for s in soorten_input.split(",")]
eigenschappen = [e.strip() for e in eigenschappen_input.split(",")]

# Matrix
data = {}
for e in eigenschappen:
    data[e] = [st.checkbox(f"{s} heeft {e}", key=f"{s}_{e}") for s in soorten]

df = pd.DataFrame(data, index=soorten)

if st.button("Genereer Cladogram"):
    if len(soorten) < 2:
        st.error("Voeg minimaal 2 soorten toe.")
    else:
        # Berekening
        Z = linkage(df.astype(int), method='ward')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        # Haal data uit dendrogram voor coordinaten
        ddata = dendrogram(Z, labels=df.index, orientation='top', ax=ax)
        
        # Logica om eigenschappen op knooppunten te plaatsen
        # icoord bevat x-posities, dcoord bevat y-posities (hoogte van knooppunt)
        for i, d in zip(ddata['icoord'], ddata['dcoord']):
            x = 0.5 * sum(i[1:3]) # Midden van de horizontale lijn
            y = d[1]               # Hoogte van de splitsing
            
            # Hier kun je logica toevoegen om te bepalen WELKE eigenschap hier hoort.
            # Voor nu zetten we een marker neer op elk knooppunt:
            plt.plot(x, y, 'ro', markersize=4) 
            plt.annotate("Nieuwe eigenschap", (x, y), xytext=(0, 5), 
                         textcoords='offset points', va='bottom', ha='center', fontsize=8, color='darkred')

        plt.title("Cladogram: Punten markeren evolutie-stappen")
        st.pyplot(fig)
        st.success("De rode stippen geven de 'nodes' aan waar eigenschappen veranderen.")
