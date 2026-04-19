 import streamlit as st
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

st.set_page_config(layout="wide") # Breed beeld werkt beter voor tabellen
st.title("Cladogram & Eigenschappen Explorer")

# 1. Voorbeeld data (0 = Nee, 1 = Ja)
data = {
    'Wervelkolom': [1, 1, 1, 1, 0],
    'Longen':      [1, 1, 1, 0, 0],
    'Haar':        [1, 1, 0, 0, 0],
    'Duim':        [1, 0, 0, 0, 0]
}
index = ['Mens', 'Hond', 'Hagedis', 'Vis', 'Fruitvlieg']
df = pd.DataFrame(data, index=index)

st.subheader("1. Vul de eigenschappen in")
st.write("Pas de tabel aan om de boom te veranderen. 1 betekent 'aanwezig', 0 betekent 'afwezig'.")
edited_df = st.data_editor(df, use_container_width=True)

# 2. Layout met twee kolommen
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("2. Het Cladogram")
    if st.button("🔄 Genereer Boom"):
        try:
            # Berekening van de boomstructuur
            Z = linkage(edited_df, method='ward')
            
            fig, ax = plt.subplots(figsize=(10, 6))
            dendrogram(
                Z,
                labels=edited_df.index,
                orientation='left',
                ax=ax,
                color_threshold=0
            )
            ax.set_title("Evolutionaire Verwantschap")
            ax.set_xlabel("Afstand (verschil in eigenschappen)")
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Fout: {e}")

with col2:
    st.subheader("3. Check de Kenmerken")
    # Toont alleen de rijen die '1' hebben voor een geselecteerde soort
    geselecteerde_soort = st.selectbox("Bekijk eigenschappen van:", edited_df.index)
    
    kenmerken = edited_df.loc[geselecteerde_soort]
    aanwezige_kenmerken = kenmerken[kenmerken == 1].index.tolist()
    
    if aanwezige_kenmerken:
        for k in aanwezige_kenmerken:
            st.success(f"✅ {k}")
    else:
        st.info("Geen van de opgegeven eigenschappen aanwezig.")
