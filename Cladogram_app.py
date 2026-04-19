import streamlit as st
import matplotlib.pyplot as plt

def teken_v_cladogram(soorten):
    fig, ax = plt.subplots(figsize=(8, 6))
    n = len(soorten)
    
    # We tekenen handmatig de lijnen voor een V-vorm
    for i, soort in enumerate(soorten):
        # Lijnen trekken vanuit het midden naar de uiteinden
        ax.plot([0, 1], [0, i], color='black', lw=2)
        ax.text(1.05, i, soort, fontsize=12, va='center')
    
    ax.set_title("V-vormig Cladogram", fontsize=16)
    ax.axis('off') # Verwijder de assen
    return fig

st.title("Eenvoudige Cladogram Maker")

# Makkelijke invoer: een simpele lijst
input_data = st.text_area("Typ de namen van je soorten (één per regel):", 
                          "Mens\nChimpansee\nGorilla\nOrang-oetan")

soorten_lijst = [s.strip() for s in input_data.split('\n') if s.strip()]

if st.button("🔄 Teken Cladogram"):
    if soorten_lijst:
        fig = teken_v_cladogram(soorten_lijst)
        st.pyplot(fig)
    else:
        st.error("Voer eerst wat namen in!")
