import streamlit as st

 # Initialisation de l'état
if 'habilete' not in st.session_state:
    st.session_state.habilete = 6  # Valeur initiale d'HABILETÉ
if 'endurance' not in st.session_state:
    st.session_state.endurance = 12  # Valeur initiale d'ENDURANCE
if 'chance' not in st.session_state:
    st.session_state.chance = 6  # Valeur initiale de CHANCE
if 'inventaire' not in st.session_state:
    st.session_state.inventaire = "Lampe, épée, potion de soin"  # Inventaire initial

# Titre de l'application
st.title('Aventure Interactive')

# Diviser l'écran en 3 colonnes pour la fenêtre de lecture, l'illustration, et la fiche du joueur
col1, col2, col3 = st.columns([2, 1, 1])

# Fenêtre de lecture
with col1:
    st.header("Fenêtre de lecture")
    # Remplacer ce texte par le paragraphe actuel de votre histoire
    st.write("Ici s'affichera le texte du paragraphe que l'utilisateur doit lire.")

    # Champ pour la saisie du choix de l'utilisateur
    choix = st.text_input("Quel est votre choix ?")
    st.write("Vous avez choisi :", choix)

# Illustration
with col2:
    st.header("Illustration")
    st.write("Ici pourrait s'afficher une illustration générée ou sélectionnée en fonction du récit.")

# Fiche du joueur
with col3:
    st.header("Fiche du joueur")
    # Exemple de caractéristiques modifiables
    habilete = st.number_input("HABILETÉ", min_value=0, max_value=12, value=6)
    endurance = st.number_input("ENDURANCE", min_value=0, max_value=24, value=12)
    chance = st.number_input("CHANCE", min_value=0, max_value=12, value=6)
    # Exemple d'inventaire
    inventaire = st.text_area("Inventaire", value="Lampe, épée, potion de soin")