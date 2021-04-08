from pathlib import Path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.colors as mcolor
from matplotlib import cm


FONT_PATH = str(Path(__file__).parent / "data" / "Arimo-VariableFont_wght.ttf")


class PublicationWordCloud(WordCloud):
    """Create word cloud for publication.
    Force some default settings for consistency:
    Horizontal text
    Arial like font (allow over write)
    Transparent back ground
    Word value / frequency strictly translate to the size

    Parameters
    ----------
    **args: key, value pairings
        Other keyword arguments are passed through to the underlying plotting function.
        Please see wordcloud.WordCloud

    Example
    -------
    >> val = {"self": 0.7, "other": -0.3, "focus": 0.1, "test": -0.5}
    >> wc = PublicationWordCloud()
    >> wc = wc.heatmap_to_wordcloud(val)
    """

    def __init__(self, **args):
        if args.get("font_path", False) is False:
            args["font_path"] = FONT_PATH
        args["prefer_horizontal"] = 1
        args["background_color"] = None
        args["relative_scaling"] = 1
        args["mode"] = "RGBA"
        super().__init__(**args)

    def heatmap_to_wordcloud(
        self, word_value, cmap="RdBu_r", default_color="grey"
    ):
        """Create a word cloud from word and value parings
        The returned word cloud will use font size to present value magnitude.
        Sign of the values will be reflected on the extreme ends of the color map of choice

        Parameters
        ----------
        word_value: dict(str -> float)
            Contains words and associated value, such as a principle
            component feature and the associated coefficient
        cmap: str
            matplotlib color map name
        default_color: str
            Color for word that's not present in word_value
        """
        self.color_func = _WordColorFunc(word_value, cmap, default_color)
        wc_val = val_to_freq(word_value, scalar=10)
        return self.generate_from_frequencies(frequencies=wc_val)


class _WordColorFunc:
    """Create a color function object which assigns exact colors
    to certain words based on the color to words mapping

    Parameters
    ----------
    word_freq : dict(str -> float)
        A dictionary that maps a word to its associated value.
    cmap : str
        Name of the matplotlib color map of choice
    default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words. Defaule to grey
    """

    def __init__(self, word_freq, cmap="RdBu_r", default_color="grey"):
        vmax = _find_max(word_freq.values())
        word_to_color = {}
        for (word, val) in word_freq.items():
            v = _rescale(val, vmax)
            word_to_color[word] = _get_color_hex(v, cmap)

        self.word_to_color = word_to_color
        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)


def val_to_freq(word_value, scalar):
    """turn value to integer"""
    return {k: abs(int(word_value[k] * scalar)) for k in word_value}


def _find_max(values):
    """find the absolute maximum values

    Parameters
    ----------
    values : List
        A list of numerical values
    """
    vmax = 0
    for i in values:
        if abs(i) > vmax:
            vmax = abs(i)
    return vmax


def _rescale(value, vmax):
    """Recale the value between 0 and 1 for getting color on a symmatric scale

    Parameters
    ----------
    value : float
        A numerical values
    vmax : float
        maximum value of the original list
    """
    return value + vmax / 2 * vmax


def _get_color_hex(value, cmap):
    """get hex code color in colormap from a value

    Parameters
    ----------
    value : float
        A numerical values between 1 and 0
    cmap : str
        matplotlib color map name
    """
    cm_obj = cm.get_cmap(cmap)
    return mcolor.to_hex(cm_obj(value))


# if __name__ == "__main__":
#     # test data
#     val = {"self": 0.7, "other": -0.3, "focus": 0.1, "test": -0.5}

#     # base of wc
#     wc = PublicationWordCloud()
#     pic = wc.heatmap_to_wordcloud(val)

#     plt.figure()
#     plt.imshow(pic, interpolation="bilinear")
#     plt.axis("off")
#     plt.show()
