import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import spacy
from math import exp


class InstagramClassification:
    def __init__(self, df: pd.DataFrame):
        """Fonction d'initialisation de ClassificationInstagram Class.
            Le DataFrame est vidé des lignes vides/inutilisables, puis stocké dans 2 attributs
        Args:
            df : DataFrame contenant le pseudo de l'utilisateur, la localisation et la légende.
        Returns:
            None.
        """
        string_empty = df[(df['Location'] == '') & (df['Caption'] == '')].index
        df.drop(string_empty, inplace=True)
        no_description = df[(df['Location'] == '') & (df['Caption'] == 'No photo description available.')].index
        df.drop(no_description, inplace=True)

        self.df_location = df.copy()
        self.df_description = df.copy()
        self.users = df.User_Name.unique().tolist()
        self.nlp_en = spacy.load('en_core_web_lg')

    def is_traveler(self, row):
        """Fonction déterminant si un utilisateur est "traveler" ou non
            Si l'utilisateur a visité 10 lieux différents ou plus, il est traveler.
        Args:
            row : une ligne d'un dataframe contenant au minimum la colonne Location
        Returns:
            label : booléen True si l'utilisateur est traveler
        """
        if row['Location'] >= 10:
            label = True
        else:
            label = False
        return label

    def is_foody(self, row):
        """Fonction déterminant si un utilisateur est "foody" ou non
            Si l'utilisateur a photographié au moins 1 caffé, au moins 100 boissons[...] alors il est foody
        Args:
            row : une ligne d'un dataframe contenant au minimum les colonnes coffee, drink, eating, food, pizza
        Returns:
            label : booléen True si l'utilisateur est foody
        """
        label = False
        try:
            if row['coffee'] >= 1:
                label = True
            elif row['drink'] >= 100:
                label = True
            elif row['eating'] >= 100:
                label = True
            elif row['food'] >= 100:
                label = True
            elif row['pizza'] >= 10:
                label = True
        except:
            return label
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
            if (value < 0.4):
                value = 0
            total_count += row[word]
            score += row[word] * exp(value * 3)
        return score / total_count

    def traveler_scoring(self):
        # Data cleaning
        no_location = self.df_location[(self.df_location['Location'] == '')].index
        self.df_location.drop(no_location, inplace=True)
        # Count and is_traveler function
        by_user_by_location = pd.DataFrame(self.df_location.groupby(['User_Name'])['Location'].nunique())
        by_user_by_location['traveler'] = by_user_by_location.apply(self.is_traveler, axis=1)
        return by_user_by_location

    def label_scoring(self):
        # Data cleaning
        no_description = self.df_description[(self.df_description['Caption'] == '')].index
        self.df_description.drop(no_description, inplace=True)
        no_description = self.df_description[
            (self.df_description['Caption'] == 'No photo description available.')].index
        self.df_description.drop(no_description, inplace=True)

        # One row by user
        description_by_user = []
        for user in self.users:
            is_user = self.df_description['User_Name'] == user
            description_by_user.append(pd.DataFrame(self.df_description[is_user]))
        text_concat = self.df_description.groupby('User_Name').apply(lambda x: ' '.join(x.Caption))

        # Bag of words and is_foody function
        count = CountVectorizer()
        bag_of_words = count.fit_transform(text_concat)
        bag_of_words.toarray()
        feature_names = count.get_feature_names()
        bow_description = pd.DataFrame(bag_of_words.toarray(), columns=feature_names)

        # Word similarity
        label = self.nlp_en('food')
        similarity_to_label = {}
        for word in feature_names:
            token = self.nlp_en(word)
            token = token[0]
            default_similarity = 0
            if (token.has_vector):
                default_similarity = label.similarity(token)
            similarity_to_label[token.text] = default_similarity
        score_foody = bow_description.apply(self.similarity_scoring, args=(similarity_to_label,), axis=1)

        # Join
        df_text = pd.DataFrame(text_concat)
        values_foody = []
        for val in score_foody:
            values_foody.append(val)
        df_text['foody'] = values_foody
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

        # Foody or not
        by_user_by_label = self.label_scoring()

        # Jointure of both labels
        classification = by_user_by_location.join(by_user_by_label).drop(0, axis=1)
        return classification
