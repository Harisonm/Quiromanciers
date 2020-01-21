import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import spacy
from math import exp
import matplotlib.pyplot as plt
from math import pi
import math
import streamlit as st


class InstagramClassification:
    def __init__(self, df: pd.DataFrame, labels: [str]):
        """Fonction d'initialisation de ClassificationInstagram Class.
            Le DataFrame est vidé des lignes vides/inutilisables, puis stocké dans 2 attributs
        Args:
            df : DataFrame contenant le pseudo de l'utilisateur, la localisation et la légende.
        Returns:
            None.
        """
        string_empty = df[(df["Location"] == "") & (df["Caption"] == "")].index
        df.drop(string_empty, inplace=True)

        no_description = df[
            (df["Location"] == "")
            & (df["Caption"] == "No photo description available.")
        ].index
        df.drop(no_description, inplace=True)

        self.df_location = df.copy()
        self.df_description = df.copy()
        self.users = df.User_Name.unique().tolist()
        self.nlp_en = spacy.load("en_core_web_lg")
        self.labels = labels
        self.classification = pd.DataFrame()


    def is_traveler(self, row):
        """Fonction déterminant si un utilisateur est "traveler" ou non
            Si l'utilisateur a visité 10 lieux différents ou plus, il est traveler.
        Args:
            row : une ligne d'un dataframe contenant au minimum la colonne Location
        Returns:
            label : booléen True si l'utilisateur est traveler
        """
        if row["Location"] >= 10:
            label = True
        else:
            label = False
        return label

    def similarity_scoring(self, row, similarity_to_label):
        """Fonction déterminant le score entre le label choisi et les mots détectés dans les photos de l'utilisateur
        Args:
            row : une ligne du BoW d'un utilisateur
            similarity_to_label : Le score de similarité entre le label et les mots du BoW
        Returns:
            score : score de l'utilisateur sur le label
        """
        score = 0
        total_count = 0
        for word, sim in similarity_to_label.items():
            value = sim
            if value < 0.4:
                value = 0
            total_count += row[word]
            score += row[word] * exp(value * 3)
        return (score / total_count) - 0.75

    def traveler_scoring(self):
        # Data cleaning
        no_location = self.df_location[(self.df_location["Location"] == "")].index
        self.df_location.drop(no_location, inplace=True)
        # Count and is_traveler function
        by_user_by_location = pd.DataFrame(
            self.df_location.groupby(["User_Name"])["Location"].nunique()
        )
        by_user_by_location["traveler"] = by_user_by_location.apply(
            self.is_traveler, axis=1
        )
        return by_user_by_location

    def label_scoring(self, label_to_score: str):
        # Data cleaning
        no_description = self.df_description[
            (self.df_description["Caption"] == "")
        ].index
        self.df_description.drop(no_description, inplace=True)
        no_description = self.df_description[
            (self.df_description["Caption"] == "No photo description available.")
        ].index
        self.df_description.drop(no_description, inplace=True)

        # One row by user
        description_by_user = []
        for user in self.users:
            is_user = self.df_description["User_Name"] == user
            description_by_user.append(pd.DataFrame(self.df_description[is_user]))
        text_concat = self.df_description.groupby("User_Name").apply(
            lambda x: " ".join(x.Caption)
        )

        # Bag of words and is_foody function
        count = CountVectorizer()
        bag_of_words = count.fit_transform(text_concat)
        bag_of_words.toarray()
        feature_names = count.get_feature_names()
        bow_description = pd.DataFrame(bag_of_words.toarray(), columns=feature_names)

        # Word similarity
        label = self.nlp_en(label_to_score)
        similarity_to_label = {}
        for word in feature_names:
            token = self.nlp_en(word)
            token = token[0]
            default_similarity = 0
            if token.has_vector:
                default_similarity = label.similarity(token)
            similarity_to_label[token.text] = default_similarity
        score_foody = bow_description.apply(
            self.similarity_scoring, args=(similarity_to_label,), axis=1
        )

        # Join
        df_text = pd.DataFrame(text_concat)
        values_label = []
        for val in score_foody:
            values_label.append(val)
        df_text[label_to_score] = values_label
        return df_text

    def result(self) -> pd.DataFrame:
        """Fonction déterminant si les utilisateurs sont traveler et/ou foody
        Args:
            None
        Returns:
             DataFrame indiquant si les utilisateurs sont traveler et/ou foody
        """
        # Traveler or not
        by_user_by_location = self.traveler_scoring()
        self.classification = by_user_by_location

        for lab in self.labels:
            # Foody or not
            by_user_by_label = self.label_scoring(lab)

            # Jointure of both labels
            self.classification = self.classification.join(by_user_by_label).drop(0, axis=1)
        return self.classification

    def print_classification(self):
        scores = {}
        somme = 0
        for lab in self.labels:
            somme += self.classification[lab][0]
        for lab in self.labels:
            scores[lab] = self.classification[lab][0] / somme * 100
        max_to_print = math.ceil(max(scores.values()) / 10) * 10

        df = pd.DataFrame({
            'group': ['Labels'],
            'foody': [scores['food']],
            'musician': [scores['musician']],
            'travel': [scores['travel']],
        })

        categories = list(df)[1:]
        N = len(categories)
        values = df.loc[0].drop('group').values.flatten().tolist()
        values += values[:1]

        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        ax = plt.subplot(111, polar=True)

        plt.xticks(angles[:-1], categories, color='grey', size=8)
        ax.set_rlabel_position(0)
        plt.yticks(range(0, max_to_print, 10), [k for k in range(0, max_to_print, 10)], color="grey", size=7)
        plt.ylim(0, max_to_print)

        ax.plot(angles, values, linewidth=1, linestyle='solid')
        ax.fill(angles, values, 'b', alpha=0.1)

        st.pyplot()
