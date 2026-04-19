import streamlit as st
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

st.set_page_config(page_title="Mobiele Cladogram Maker")

st.title("🌿 Cladogram Generator")
st.write("Typ soorten en vink hun eigenschappen aan.")

# Stap 1: Input van soorten
soorten_input = st.text_input("Soorten (gescheiden door komma's):", "Hond, Kat, Vis, Mens")
eigenschappen_input = st.text_input("Eigenschappen (gescheiden door komma's):", "Haar, Vinnen, Longen")

soorten = [s.strip() for s in soorten_input.split(",")]
eigenschappen = [e.strip() for e in eigenschappen_input.split(",")]

# Stap 2: Matrix invullen
st.subheader("Karakter Matrix")
data = {}
for e in eigenschappen:
    data[e] = [st.checkbox(f"{s} heeft {e}", key=f"{s}_{e}") for s in soorten]

df = pd.DataFrame(data, index=soorten)
st.dataframe(df)

# Stap 3: Genereren
if st.button("Genereer Cladogram"):
    if len(soorten) < 2:
        st.error("Voeg minimaal 2 soorten toe.")
    else:
        # Bereken de boom (linkage matrix)
        # We zetten de vinkjes (True/False) om naar 1/0 voor berekening
        Z = linkage(df.astype(int), method='ward')
        
        # Teken het diagram
        fig, ax = plt.subplots(figsize=(10, 5))
        dendrogram(Z, labels=df.index, orientation='top', ax=ax)
        
        plt.title("Cladogram (gebaseerd op gedeelde eigenschappen)")
        plt.ylabel("Afstand")
        st.pyplot(fig)
        
        # Toon eigenschappen per groep
        st.info("Soorten die lager in de boom splitsen, delen meer eigenschappen.")
