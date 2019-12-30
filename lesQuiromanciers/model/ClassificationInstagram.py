import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


class ClassificationInstagram:
    def __init__(self, df: pd.DataFrame, users: [str]):
        string_empty = df[(df['Location'] == '') & (df['Caption'] == '')].index
        df.drop(string_empty, inplace=True)
        no_description = df[(df['Location'] == '') & (df['Caption'] == 'No photo description available.')].index
        df.drop(no_description, inplace=True)

        self.df_location = df.copy()
        self.df_description = df.copy()
        self.users = users

    def is_traveler(self, row):
        if row['Location'] >= 10:
            label = True
        else:
            label = False
        return label

    def is_foody(self, row):
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
        # Traveler or not
        no_location = self.df_location[(self.df_location['Location'] == '')].index
        self.df_location.drop(no_location, inplace=True)
        by_user_by_location = pd.DataFrame(self.df_location.groupby(['User_Name'])['Location'].nunique())
        by_user_by_location['traveler'] = by_user_by_location.apply(self.is_traveler, axis=1)

        # Foody or not
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

        # Jointure of both
        classification = by_user_by_location.join(df_text).drop(0, axis=1)
        return classification
