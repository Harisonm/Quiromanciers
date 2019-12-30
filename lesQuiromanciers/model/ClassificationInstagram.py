import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


class ClassificationInstagram:
    def __init__(self, df: pd.DataFrame, users: [str]):
        """Fonction d'initialisation de ClassificationInstagram Class.
            Le DataFrame est vidé des lignes vides/inutilisables, puis stocké dans 2 attributs
        Args:
            df : DataFrame contenant le pseudo de l'utilisateur, la localisation et la légende.
            users : Liste d'utilisateurs présents dans le dataset
        Returns:
            None.
        """
        string_empty = df[(df['Location'] == '') & (df['Caption'] == '')].index
        df.drop(string_empty, inplace=True)
        no_description = df[(df['Location'] == '') & (df['Caption'] == 'No photo description available.')].index
        df.drop(no_description, inplace=True)

        self.df_location = df.copy()
        self.df_description = df.copy()
        self.users = users

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

    def result(self) -> pd.DataFrame:
        """Fonction déterminant si les utilisateurs sont traveler et/ou foody
        Args:
            None
        Returns:
             DataFrame indiquant si les utilisateurs sont traveler et/ou foody
        """
        ## Traveler or not
        # Data cleaning
        no_location = self.df_location[(self.df_location['Location'] == '')].index
        self.df_location.drop(no_location, inplace=True)
        #Count and is_traveler function
        by_user_by_location = pd.DataFrame(self.df_location.groupby(['User_Name'])['Location'].nunique())
        by_user_by_location['traveler'] = by_user_by_location.apply(self.is_traveler, axis=1)

        ## Foody or not
        # Data cleaning
        no_description = self.df_description[(self.df_description['Caption'] == '')].index
        self.df_description.drop(no_description, inplace=True)
        no_description = self.df_description[
            (self.df_description['Caption'] == 'No photo description available.')].index
        self.df_description.drop(no_description, inplace=True)

        description_by_user = []
        for user in self.users:
            is_user = self.df_description['User_Name'] == user
            description_by_user.append(pd.DataFrame(self.df_description[is_user]))
        text_concat = self.df_description.groupby('User_Name').apply(lambda x: ' '.join(x.Caption))

        #Bag of words and is_foody function
        count = CountVectorizer()
        bag_of_words = count.fit_transform(text_concat)
        bag_of_words.toarray()
        feature_names = count.get_feature_names()
        bow_description = pd.DataFrame(bag_of_words.toarray(), columns=feature_names)
        col_foody = bow_description.apply(self.is_foody, axis=1)

        df_text = pd.DataFrame(text_concat)
        values_foody = []
        for val in col_foody:
            values_foody.append(val)
        df_text['foody'] = values_foody

        # Jointure of both labels
        classification = by_user_by_location.join(df_text).drop(0, axis=1)
        return classification
