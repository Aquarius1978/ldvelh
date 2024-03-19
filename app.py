import json
import openai
import os
import random
import re
import streamlit as st

# Configuration et initialisation
openai.api_key = os.getenv('OPENAI_API_KEY')
if openai.api_key is None:
    st.error("Clé API OpenAI non trouvée. Veuillez définir la variable d'environnement OPENAI_API_KEY.")
    st.stop()

# Définitions des fonctions
def extraire_infos_adversaires(test_str):
    # Utilisez une expression régulière pour extraire les informations des adversaires
    pattern = re.compile(r"Combat (\w+.*?ENDURANCE: \d+)")
    matches = pattern.findall(test_str)
    infos_adversaires = "\n".join(matches)  # Formatage des informations
    return infos_adversaires

# Fonction pour interagir avec l'API OpenAI
def obtenir_texte_enrichi(paragraphe_id, consigne):
    paragraphe = livre[paragraphe_id]
    prompt = paragraphe.get("intro", "")

    if "text" in paragraphe:
        prompt += "\n\n" + paragraphe["text"]

    # Vérifier si la consigne est un combat et ajuster le prompt en conséquence
    prompt_supplementaire = prompts_supplementaires.get(consigne, "")
    prompt_complet = prompt + "\n\n" + prompt_supplementaire

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un conteur hors pair. Tu racontes l'histoire d'un aventurier qui explore un labyrinthe souterrain truffé de monstres, de pièges, de trésors. Le but de cet aventurier est de détruire le sorcier à la tête de ce labyrinthe. Tu t'adresse au lecteur par 'vous', car le lecteur est l'aventurier."},
            {"role": "user", "content": prompt_complet}
        ]
    )

    texte_genere = response.choices[0].message["content"].strip()

    # Ajouter directement les informations des adversaires à la fin du texte généré si nécessaire
    if "test" in paragraphe and "Combat" in paragraphe["test"]:
        details_combats = paragraphe["test"].split(". ")
        # Supprimer "Combat" de chaque entrée et formater pour l'affichage
        infos_adversaires = "\n".join([combat.replace("Combat ", "") for combat in details_combats])
        texte_genere += "\n\nAdversaire(s) :\n" + infos_adversaires

    return texte_genere


with open('prompts.json', 'r') as file_prompt:
    prompts_supplementaires = json.load(file_prompt)
with open("livre.json", "r", encoding="utf-8") as file_livre:
    livre = json.load(file_livre)


# Initialisation de l'état
if 'paragraphe_actuel' not in st.session_state:
    st.session_state.paragraphe_actuel = "1"  # Commencer par le paragraphe 1 par défaut
if 'regles_lues' not in st.session_state:
    st.session_state['regles_lues'] = False
if 'resultat_de_6_faces' not in st.session_state:
    st.session_state['resultat_de_6_faces'] = None
if 'resultat_deux_des' not in st.session_state:
    st.session_state['resultat_deux_des'] = None
if 'texte_genere' not in st.session_state:
    st.session_state['texte_genere'] = "Appuyez sur le bouton pour générer le texte de votre aventure."

if not st.session_state['regles_lues']:
    st.title('Règles du jeu')
else:
    st.title('Le Sorcier de la Montagne de Feu')

col1, col2, col3 = st.columns([5, 2, 1])

# Fenêtre de lecture
with col1:
    if not st.session_state['regles_lues']:
        # Lire et afficher les règles depuis un fichier texte
        with open("regles.txt", "r", encoding="utf-8") as fichier_regles:
            regles = fichier_regles.read()
        regles_formattees = regles.replace("\n", "  \n")
        st.markdown(regles_formattees, unsafe_allow_html=True)
        if st.button("J'ai lu les règles, commencer l'aventure"):
            st.session_state['regles_lues'] = True  # Marquer les règles comme lues
            st.session_state['texte_genere'] = obtenir_texte_enrichi("1", "default")
            st.session_state['paragraphe_actuel'] = "1"
    else:
        st.header("Aventure")    
        paragraphe_id = st.session_state["paragraphe_actuel"]    
        paragraphe = livre.get(paragraphe_id, {})    
        consigne = 'default'
    
        # Vérifier si une balise "test" est présente et ajuster la consigne en conséquence
        test_tag = paragraphe.get("test", "")
        if "combat" in test_tag:
            consigne = "combat"
        elif any(other_condition in test_tag for other_condition in ["decouverte", "autre_condition"]):  # Exemple pour d'autres conditions
            consigne = "la_clé_correspondante_dans_prompts_json"  # Assurez-vous d'ajouter la clé correcte de prompts.json

        # Générer et afficher le texte enrichi après un choix
        if not st.session_state['texte_genere'] or "generer_texte" in st.session_state and st.session_state["generer_texte"]:
            texte_enrichi = obtenir_texte_enrichi(paragraphe_id, consigne)
            st.session_state['texte_genere'] = texte_enrichi
            st.session_state["generer_texte"] = False  # Réinitialiser pour le prochain choix
            st.write(texte_enrichi)
        else:
            # Affichage initial du paragraphe
            if "intro" in paragraphe:
                st.write(paragraphe["intro"])
    
        # S'assurer que 'paragraphe' contient des choix avant de tenter de les afficher
        if "choices" in paragraphe:
            # Gestion des choix
            for index, choix in enumerate(paragraphe["choices"], start=1):
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

# Personnage
with col2:
    st.header("Fiche du joueur")
    # Exemple de caractéristiques modifiables
    habilete = st.number_input("HABILETÉ", min_value=0, max_value=12, value=6)
    endurance = st.number_input("ENDURANCE", min_value=0, max_value=24, value=12)
    chance = st.number_input("CHANCE", min_value=0, max_value=12, value=6)
    # Exemple d'inventaire
    inventaire = st.text_area("Inventaire", value="Lampe, épée, potion de soin")
    bourse = st.number_input("OR", min_value=0, max_value=500, value=1)

# Lancer de dés
with col3:
    st.header("Lancer de dés")
    
    if st.button("Lancer un dé à 6 faces"):
        st.session_state['resultat_de_6_faces'] = random.randint(1, 6)
    
    if st.button("Lancer deux dés à 6 faces"):
        st.session_state['resultat_deux_des'] = random.randint(1, 6) + random.randint(1, 6)
    
    if st.session_state['resultat_de_6_faces'] is not None:
        st.write(f"Résultat du dé à 6 faces: {st.session_state['resultat_de_6_faces']}")
    
    if st.session_state['resultat_deux_des'] is not None:
        st.write(f"Résultat de deux dés à 6 faces: {st.session_state['resultat_deux_des']}")