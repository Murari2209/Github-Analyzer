import matplotlib.pyplot as plt

def plot_languages(lang_counts):

    lang_counts.plot(kind="bar")

    plt.title("Programming Language Distribution")

    plt.savefig("charts/language_distribution.png")

    plt.close()