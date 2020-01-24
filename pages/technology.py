import streamlit as st
from PIL import Image

#image_github = Image.open('docs/logo/github.png')
#image_python = Image.open('docs/logo/python3.png')
#image_openAI = Image.open('docs/logo/openAI.png')
#image_spacy = Image.open('docs/logo/spacy.png')
def content():
    st.sidebar.title("Technologies Used")
    st.sidebar.info("Un tour d'horizon des technologies que nous avons utilisé pour développer ce projet.")
    st.markdown("Github : Git nous permet de stocker notre projet (repository) sur un serveur distant. \
                Il nous a permis de travailler en collaboration en avançant plus rapidement sur nos tâches. \
                Github intègre également des configurations pour avoir un workflow entre le repository et un serveur de production. \
                Dans notre cas nous avons mis en place un workflow pour monter un container et le déployer dans GKE. \
                Lien github : https://github.com/Harisonm/Quiromanciers")
    st.markdown("Docker : Docker est un outil permettant de gérer et monter facilement \
                des containers ou seront packagé notre application globale. \
                Une fois notre application containerisée,\
                nous utilisons Kubernetes pour pouvoir l’orchestrer plus facilement. \
                    Lien Docker : https://www.docker.com/")
    st.markdown("Kubernetes : Kubernetes est un orchestrateur de container. \
                Nous avons choisi d’utiliser kubernetes car il transforme les containers \
                en pod et ces pods sont ensuite mis à l’échelle (scaling) selon les \
                ressources dont l’application a besoin en fonction des ressources disponible.\
                Lien Kubernetes: https://kubernetes.io/fr/")
    st.markdown("GKE : Google Kubernetes Engine (GKE) est un environnement géré et prêt à \
                l'emploi pour le déploiement d'applications en conteneur \
                dans des clusters Kubernetes. Il regroupe permet d’avoir \
                une efficacité en gestion des ressources, en automatisation \
                des opérations et en flexibilité. Il nous permet de monitorer nos ressources. \
                Notre configuration des clusters et pods GKE : \
                -	3 clusters \
                -	90G de RAM \
                -	24 processeurs virtuels \
                -	Version côté GKE : 1.13.11-gke.14 \
                Lien GKE : https://cloud.google.com/kubernetes-engine/?hl=fr")
    st.markdown("Python : On a utilisé python 3.7 car tous les libraires de machine Learning sont disponible sur python version 3.7.")
    st.markdown("GPT2 : GPT2 est un modèle de OpenAI entrainé sur les données wikipedia, \
                pour notre projet, nous avons pris gpt2-simple afin de générer du texte \
                en faisant du fine-tuning (transfert-learning). \
                Nous l’avons utilisé afin d’entrainer le modèle \
                sur nos propres données et de ressortir des biographies spécifiques selon \
                les préférences de l’utilisateur. \
                Lien Github openAI: https://github.com/openai/gpt-2 \
                Lien Gpt2-simple (leger): https://github.com/minimaxir/gpt-2-simple ")
    st.markdown("Spacy: Spacy est une librairie qui permet de faire des traitement \
                automatique du langage naturel, nous l’avons utilisé pour faire des \
                découpage en token, des analyses de similarités. \
                Lien Spacy : https://spacy.io/")
    st.markdown("Instaloader : Instaloader est une librarie qui permet de \
                faire un call API sur instagram avec de récupérer des \
                données de différents compte instagram. \
                Lien Instaloader : https://instaloader.github.io/")
    
    #st.image([image_github,image_openAI,image_spacy,image_python],width=100)

