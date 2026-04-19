import streamlit as st
from Bio import Phylo
from io import StringIO, BytesIO
import matplotlib.pyplot as plt

st.title("Cladogram Generator")

# Voorbeeld Newick string als input
newick = st.text_area("Voer Newick data in:", "(A:0.1,B:0.2,(C:0.3,D:0.4):0.5);")

if st.button("🔄 Teken V-Cladogram"):
    if newick:
        try:
            # 1. Lees de boom in
            tree = Phylo.read(StringIO(newick), "newick")
            
            # 2. Maak een Matplotlib figuur aan
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # 3. Teken de boom op de 'ax'
            # Let op de exacte inspringing hieronder
            Phylo.draw(tree, 
                       axes=ax, 
                       do_show=False)
            
            # 4. Toon in Streamlit
            st.pyplot(fig)
            
            # 5. Optioneel: Voorbereiden voor download
            buf = BytesIO()
            fig.savefig(buf, format="png")
            st.download_button(
                label="Download Cladogram als PNG",
                data=buf.getvalue(),
                file_name="cladogram.png",
                mime="image/png"
            )
            
        except Exception as e:
            st.error(f"Fout bij het verwerken van de Newick data: {e}")
    else:
        st.warning("Voer eerst Newick data in.")
