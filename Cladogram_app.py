import streamlit as st
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

# ... (Hetzelfde input gedeelte als hiervoor) ...

if st.button("Genereer Uitgebreid Cladogram"):
    if len(soorten) < 2:
        st.error("Voeg meer soorten toe.")
    else:
        # Maak nieuwe labels voor de onderkant: "Soort (Eigenschap1, Eigenschap2)"
        nieuwe_labels = []
        for s in soorten:
            # Zoek alle eigenschappen die 'True' zijn voor deze soort
            soort_traits = df.loc[s]
            actieve_traits = soort_traits[soort_traits].index.tolist()
            if actieve_traits:
                label = f"{s}\n({', '.join(actieve_traits)})"
            else:
                label = s
            nieuwe_labels.append(label)
        
        # Tijdelijke dataframe met de nieuwe labels voor de berekening
        df_plot = df.copy()
        df_plot.index = nieuwe_labels

        # Berekening
        Z = linkage(df_plot.astype(int), method='ward')
        
        fig, ax = plt.subplots(figsize=(10, 8))
        # Gebruik de nieuwe_labels in de dendrogram
        ddata = dendrogram(Z, labels=df_plot.index, orientation='top', ax=ax)
        
        # Logica voor de knooppunten (de rode stippen van de vorige stap)
        n_species = len(df_plot)
        clusters = {i: [i] for i in range(n_species)}
        
        for i, merge in enumerate(Z):
            node_id = n_species + i
            members = clusters[int(merge[0])] + clusters[int(merge[1])]
            clusters[node_id] = members
            
            common_traits = df.iloc[members].all()
            traits_list = common_traits[common_traits].index.tolist()
            
            x = 0.5 * sum(ddata['icoord'][i][1:3])
            y = ddata['dcoord'][i]
            
            if traits_list:
                plt.plot(x, y, 'ro', markersize=5)
                plt.annotate(", ".join(traits_list), (x, y), xytext=(5, 5), 
                             textcoords='offset points', fontsize=8, color='blue')

        # Zorg dat de tekst aan de onderkant goed leesbaar is
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.3) # Ruimte voor lange teksten onderaan
        
        st.pyplot(fig)
