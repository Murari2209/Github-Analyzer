def language_distribution(df):

    return df["language"].value_counts()


def stars_vs_forks(df):

    return df[["stars", "forks"]]