import streamlit as st
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

st.title("Cladogram op basis van Eigenschappen")

st.write("Vul de tabel in: 1 = Ja, 0 = Nee")

# 1. Maak een standaard tabelletje als voorbeeld
data = {
    'Huidmondjes': [1, 1, 1, 0],
    'Zaden': [1, 1, 0, 0],
    'Bloemen': [1, 0, 0, 0]
}
df = pd.DataFrame(data, index=['Zonnebloem', 'Den', 'Varen', 'Alg'])

# 2. Laat de gebruiker de tabel bewerken in Streamlit
edited_df = st.data_editor(df)

if st.button("🔄 Genereer Cladogram"):
    try:
        # Bereken de afstanden tussen de soorten op basis van de 1-en en 0-en
        # We gebruiken 'ward' linkage voor een mooie boomstructuur
        Z = linkage(edited_df, method='ward')
        
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # Teken het dendrogram (wat in feite een cladogram is)
        dendrogram(
            Z,
            labels=edited_df.index,
            orientation='left', # 'left' zorgt voor de klassieke zijwaartse boom
            ax=ax,
            color_threshold=0 # Houdt de lijnen standaard zwart/blauw
        )
        
        ax.set_title("Evolutionaire Verwantschap")
        ax.set_xlabel("Afstand (verschil in eigenschappen)")
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Er ging iets mis: {e}")

st.info("De soorten die de meeste 'enen' delen, komen dichter bij elkaar te staan.")
