from pathlib import Path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.colors as mcolor
from matplotlib import cm


FONT_PATH = str(Path(__file__).parent / "data" / "Arimo-VariableFont_wght.ttf")


class PublicationWordCloud(WordCloud):
    def __init__(self, **args):
        args["height"] = 400
        args["width"] = 400
        args["prefer_horizontal"] = 1
        args["font_path"] = FONT_PATH
        args["font_step"] = 2
        args["background_color"] = None
        args["relative_scaling"] = 1
        args["mode"] = "RGBA"
        super().__init__(**args)

    def heatmap_to_wordcloud(self, word_value):
        # turn value to integer
        self.color_func = _WordColorFunc(word_value)
        wc_val = {k: abs(int(word_value[k] * 10)) for k in word_value}
        return self.generate_from_frequencies(frequencies=wc_val)


class _WordColorFunc:
    """Create a color function object which assigns EXACT colors
    to certain words based on the color to words mapping

    Parameters
    ----------
    word_freq : dict(str -> int)
        A dictionary that maps a word to its frequency.
    cmap : str
        Name of the matplotlib color map of choice
    default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words. Defaule to grey
    """

    def __init__(self, word_freq, cmap="RdBu_r", default_color="grey"):
        vmax = _fine_max(word_freq.values())
        self.word_to_color = {
            word: _get_color_hex(val, vmax, cmap)
            for (word, val) in word_freq.items()
        }

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)


def _fine_max(values):
    """find the absolute maximum values
    values : List
        A list of numerical values
    """
    vmax = 0
    for i in values:
        if abs(i) > vmax:
            vmax = abs(i)
    return vmax


def _rescale(value, vmax):
    """Recale the value between 0 and 1 for getting color
    value : float
        A numerical values
    vmax : float
        maximum value of the original list
    """
    return value + vmax / 2 * vmax


def _get_color_hex(value, vmax, cmap):
    """get hex code color in colormap from a value"""
    cm_obj = cm.get_cmap(cmap)
    return mcolor.to_hex(cm_obj(_rescale(value, vmax)))


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
