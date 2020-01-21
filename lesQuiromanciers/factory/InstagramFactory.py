from instaloader import *
import os
import json
import pandas as pd
import datetime as dt
import streamlit as st
import os


class InstagramFactory(object):
    def __init__(self, users: [str], start_date: dt.datetime, end_date: dt.datetime):
        """Fonction d'initialisation de InstaFactory Class.
            Seuls le texte et les métadonnées sont téléchargés.
        Args:
            users: Liste de pseudos d'utilisateurs desquels on récupère les posts Instagram
            start_date: Début de la période des posts que l'on récupère
            end_date: Fin de la période des posts que l'on récupère
        Returns:
            None
        """
        self.users = users
        self.start_date = start_date
        self.end_date = end_date
        self.loader = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_comments=False,
            compress_json=False,
            download_video_thumbnails=False,
        )

    def __str__(self) -> str:
        return (
            "User list : "
            + str(self.users)
            + " Time interval : "
            + str(self.start_date)
            + " to : "
            + str(self.end_date)
        )

    def get_users(self) -> [str]:
        return self.users

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def set_users(self, users: [str]):
        self.users = users

    def set_start_date(self, start_date: dt.datetime):
        self.start_date = start_date

    def set_end_date(self, end_date: dt.datetime):
        self.end_date = end_date

    def download_data(self):
        """Fonction pour télécharger les posts instagram selon les attributs de la classe (utilisateurs et période)
        Args: None
        Returns: None
        """
        os.chdir("data/")
        for user in self.users:
            if os.path.isdir(user):
                continue
            profile = Profile.from_username(self.loader.context, user)
            for post in profile.get_posts():
                if self.start_date < post.date <= self.end_date:
                    self.loader.download_post(post, target=user)
        os.chdir("../")

    def dataframe_creation(self) -> pd.DataFrame:
        """Extraction des métadonnées des fichiers json pour créer un DataFrame
            Cette fonction doit être appelée après download_data(). Sinon le DataFrame sera logiquement vide
        Args:
            None
        Returns:
            DataFrame contenant la localisation du post et la légende générée par Instagram
        """
        user_name = []
        location = []
        caption = []
        st.write(os.getcwd())
        for user in self.users:
            if not os.path.isdir("data/" + user):
                break
            directory = "data/" + user + "/"
            for element in os.listdir(directory):
                if element.endswith(".json"):
                    user_name.append(user)
                    with open(directory + element) as json_file:
                        post = json.load(json_file)
                        if post["node"] is not None:
                            if post["node"]["location"] is not None:
                                location.append(post["node"]["location"]["slug"])
                            else:
                                location.append("")
                            if "accessibility_caption" in post["node"]:
                                caption.append(post["node"]["accessibility_caption"])
                            else:
                                caption.append("")
        dataset = {"User_Name": user_name, "Location": location, "Caption": caption}
        return pd.DataFrame(dataset)
