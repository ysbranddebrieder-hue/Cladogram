import streamlit as st
from Bio import Phylo
from io import StringIO
import matplotlib.pyplot as plt

st.title("🧬 Interactieve Cladogram Maker")

# Input: Gebruiker kan een Newick string plakken
newick_input = st.text_area(
    "Plak hier je Newick string:", 
    "(Mens:0.1, (Chimp:0.1, Gorilla:0.2):0.1);"
)

if newick_input:
    try:
        # Lees de boom in vanuit de string
        tree = Phylo.read(StringIO(newick_input), "newick")
        
        # Instellingen voor de visualisatie
        st.sidebar.header("Instellingen")
        tree_type = st.sidebar.selectbox("Type:", ["cladogram", "phylogram"])
        
        # Maak de plot
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)
        
        # Teken de boom
        Phylo.draw(tree, axes=ax, do_show=False, branch_labels=lambda c: "")
        
        # Streamlit display
        st.pyplot(fig)
        
        # Download optie
        st.download_button(
            label="Download Cladogram als afbeelding",
            data=StringIO(newick_input).read(),
            file_name="cladogram.nwk"
        )
        
    except Exception as e:
        st.error(f"Fout bij het laden van de boom: {e}")

