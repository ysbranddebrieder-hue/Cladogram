import streamlit as st
from Bio import Phylo
from io import StringIO, BytesIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cladogram Maker", layout="centered")

st.title("🧬 Cladogram Maker")

# Tekstveld voor de Newick string
newick_input = st.text_area(
    "Voer je Newick string in:", 
    "(Mens, (Chimp, Gorilla));",
    height=150
)

# Knop om te tekenen
if st.button("🔄 Teken Cladogram"):
    if newick_input:
        try:
            # 1. Lees de boom in
            tree = Phylo.read(StringIO(newick_input), "newick")
            
            # 2. Maak de plot
            fig = plt.figure(figsize=(10, 6))
            ax = fig.add_subplot(1, 1, 1)
            Phylo.draw(tree, axes=ax, do_show=False)
            plt.axis('off')
            
            # 3. Toon de afbeelding
            st.pyplot(fig)
            
            # 4. Maak een download-bestand (PNG) in het geheugen
            buf = BytesIO()
            fig.savefig(buf, format="png", bbox_inches='tight')
            st.download_button(
                label="💾 Download als Afbeelding (PNG)",
                data=buf.getvalue(),
                file_name="mijn_cladogram.png",
                mime="image/png"
            )
            
        except Exception as e:
            st.error(f"Fout in de string: {e}")
    else:
        st.warning("Voer eerst een Newick string in.")

st.info("Tip: Eindig altijd met een puntkomma (;)")
