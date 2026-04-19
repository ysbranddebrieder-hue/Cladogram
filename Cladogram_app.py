import streamlit as st
from Bio import Phylo
from io import StringIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cladogram Maker", layout="centered")

st.title("🧬 Cladogram Maker")

# Tekstveld voor de Newick string
newick_input = st.text_area(
    "Voer je Newick string in:", 
    "(Mens, (Chimp, Gorilla));",
    height=150
)

# De knop om het tekenen te forceren
if st.button("🔄 Teken Cladogram"):
    if newick_input:
        try:
            # Lees de boom in
            tree = Phylo.read(StringIO(newick_input), "newick")
            
            # Maak de visualisatie
            fig = plt.figure(figsize=(10, 6))
            ax = fig.add_subplot(1, 1, 1)
            
            # Teken de boom (cladogram stijl)
            Phylo.draw(tree, axes=ax, do_show=False)
            
            # Verwijder assen voor een schoner beeld
            plt.axis('off')
            
            # Toon in Streamlit
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Er zit een fout in je Newick string: {e}")
    else:
        st.warning("Voer eerst een Newick string in.")

st.info("Tip: Gebruik haakjes, komma's en eindig met een puntkomma (;)")
