import json
import openai
import os
import streamlit as st

# Configuration de la clé API OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Message d'erreur si la clé n'est pas trouvée
if openai.api_key is None:
    st.error("Clé API OpenAI non trouvée. Veuillez définir la variable d'environnement OPENAI_API_KEY.")
    st.stop()

# Charger les prompts à partir du fichier JSON
with open('prompts.json', 'r') as file_prompt:
    prompts_supplementaires = json.load(file_prompt)

# Charger le fichier JSON de l'aventure
with open("livre.json", "r", encoding="utf-8") as file_livre:
    livre = json.load(file_livre)
    
# Fonction pour interagir avec l'API OpenAI
def obtenir_texte_enrichi(paragraphe_id, consigne):
    paragraphe = livre[paragraphe_id]
    prompt = paragraphe.get("intro", "")

    # Ajouter le contenu de "text" au prompt, s'il existe
    if "text" in paragraphe:
        prompt += "\n\n" + paragraphe["text"]
        
    # Récupérer le prompt supplémentaire en fonction de la consigne
    prompt_supplementaire = prompts_supplementaires.get(consigne, prompts_supplementaires["default"])   
        
    # Ajouter le prompt supplémentaire pour plus de contexte
    prompt += "\n\n" + prompt_supplementaire

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].text.strip()

# Initialisation de l'état
if 'paragraphe_actuel' not in st.session_state:
    st.session_state.paragraphe_actuel = "1"  # Commencer par le paragraphe 1 par défaut

# Titre de l'application
st.title('Le Sorcier de la Montagne de Feu')

# Diviser l'écran en 3 colonnes pour la fenêtre de lecture, l'illustration, et la fiche du joueur
col1, col2, col3 = st.columns([3, 2, 2])

# Fenêtre de lecture
with col1:
    st.header("Aventure")
    consigne = 'default'
    
    paragraphe_id = st.session_state["paragraphe_actuel"]
    
    # Générer et afficher le texte enrichi après un choix
    if "generer_texte" in st.session_state and st.session_state["generer_texte"]:
        texte_enrichi = obtenir_texte_enrichi(paragraphe_id, consigne)
        st.write(texte_enrichi)
        st.session_state["generer_texte"] = False  # Réinitialiser pour le prochain choix
    else:
        # Affichage initial du paragraphe
        paragraphe = livre[paragraphe_id]
        st.write(paragraphe["intro"])
    
    # Gestion des choix
    for index, choix in enumerate(paragraphe.get("choices", []), start=1):
        choix_texte = choix.get("text", f"Choix {index}")
        if st.button(choix_texte):
            goto = choix.get("goto")
            if goto:
                st.session_state.paragraphe_actuel = str(goto)
                st.session_state["generer_texte"] = True
                st.experimental_rerun()
            else:
                st.error("Erreur: Ce choix ne mène nulle part. Veuillez choisir une autre option.")
    
    # Partie pour entrer un numéro de paragraphe directement
    st.write("Ou entrez un numéro de paragraphe pour y aller directement :")
    num_paragraphe = st.text_input("", key="num_paragraphe_direct")
    
    if st.button("Aller au paragraphe", key="go_to_paragraph"):
        if num_paragraphe.isdigit() and num_paragraphe in livre:
            st.session_state.paragraphe_actuel = num_paragraphe
            st.session_state["generer_texte"] = True
            st.experimental_rerun()
        else:
            st.error("Numéro de paragraphe invalide ou inexistant.")

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
    bourse = st.number_input("OR", min_value=0, max_value=500, value=1)