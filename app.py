import os
import streamlit as st
import openai

# Configuration de la clé API OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# message d'erreur si la clé n'est pas trouvée
if openai.api_key is None:
    st.error("Clé API OpenAI non trouvée. Veuillez définir la variable d'environnement OPENAI_API_KEY.")
    st.stop()

# Fonction pour interagir avec l'API OpenAI
def obtenir_texte_aventure(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Ou "gpt-3.5-turbo", selon ce que vous utilisez
        prompt=prompt,
        max_tokens=100  # Ajustez selon la longueur de texte désirée
    )
    return response.choices[0].text.strip()

 # Initialisation de l'état
if 'habilete' not in st.session_state:
    st.session_state.habilete = 6  # Valeur initiale d'HABILETÉ
if 'endurance' not in st.session_state:
    st.session_state.endurance = 12  # Valeur initiale d'ENDURANCE
if 'chance' not in st.session_state:
    st.session_state.chance = 6  # Valeur initiale de CHANCE
if 'inventaire' not in st.session_state:
    st.session_state.inventaire = "Lampe, épée, potion de soin"  # Inventaire initial
if 'texte_aventure' not in st.session_state:
    st.session_state.texte_aventure = "Bienvenue dans votre aventure ! Que souhaitez-vous faire ?"

# Titre de l'application
st.title('Le Sorcier de la Montagne de Feu')

# Diviser l'écran en 3 colonnes pour la fenêtre de lecture, l'illustration, et la fiche du joueur
col1, col2, col3 = st.columns([2, 1, 1])

# Fenêtre de lecture
with col1:
    st.header("Aventure")
    # Remplacer ce texte par le paragraphe actuel de votre histoire
    st.write(st.session_state.texte_aventure)

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