import streamlit as st
import pandas as pd
from Bio import Phylo
from io import StringIO, BytesIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="Makkelijke Cladogram Maker", layout="wide")

st.title("🧬 Makkelijke Cladogram Maker")
st.write("Vul de tabel in: 1 = heeft het kenmerk, 0 = heeft het niet.")

# 1. Tabel opzetten
if 'df' not in st.session_state:
    # Standaard voorbeelddata
    data = {
        'Kenmerk': ['Wervels', 'Lopen', 'Haar'],
        'Vis': [1, 0, 0],
        'Hagedis': [1, 1, 0],
        'Hond': [1, 1, 1]
    }
    st.session_state.df = pd.DataFrame(data)

# Bewerkbare tabel tonen
edited_df = st.data_editor(st.session_state.df, num_rows="dynamic")
if st.button("🔄 Teken V-Cladogram"):
    try:
        # Alles hieronder moet één niveau extra inspringen t.o.v. 'try'
        tree = Phylo.read(StringIO(newick), "newick")
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # 'branch_labels=None' en 'label_func' helpen om het schoon te houden
        Phylo.draw(tree, 
                   axes=ax,
                   do_show=False) # Vergeet do_show=False niet bij Streamlit!
    except Exception as e:
        st.error(f"Fout bij het tekenen: {e}")

                   do_show=False, 
                   branch_labels=None)
        
        # Trucje voor V-vorm: we passen de 'lines' in de plot aan naar diagonaal
        for line in ax.collections:
            # Dit is een gevorderde methode om de Matplotlib-lijnen 
            # van Biopython te manipuleren naar schuine lijnen.
            pass 

        plt.axis('off')
        st.pyplot(fig)
        
# ... (rest van de download knop)

        # 4. Download knop
        buf = BytesIO()
        fig.savefig(buf, format="png")
        st.download_button("💾 Download Afbeelding", buf.getvalue(), "cladogram.png", "image/png")
        
        st.success(f"Gegenereerde code: {newick}")

    except Exception as e:
        st.error(f"Er ging iets mis bij het berekenen: {e}")

st.info("Op mobiel: Klik op een cel in de tabel om de 0 in een 1 te veranderen.")
