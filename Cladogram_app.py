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



        # 4. Download knop
        buf = BytesIO()
        fig.savefig(buf, format="png")
        st.download_button("💾 Download Afbeelding", buf.getvalue(), "cladogram.png", "image/png")
        
        st.success(f"Gegenereerde code: {newick}")

    except Exception as e:
        st.error(f"Er ging iets mis bij het berekenen: {e}")

st.info("Op mobiel: Klik op een cel in de tabel om de 0 in een 1 te veranderen.")
