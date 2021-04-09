from ..plotting import CoefficientWordCloud, CoefficentColor, _get_color_hex
from .utils import get_test_data_path

testdata = f"{get_test_data_path()}/font.ttf"


def test_sort_value_abs():
    # the word cloud should be ordered by absolute value
    val = {"a": 0.7, "b": -0.3, "c": 0.1, "d": -0.5}
    wc = CoefficientWordCloud()
    pic = wc.heatmap_to_wordcloud(val)

    assert list(pic.words_.keys()) == ["a", "d", "b", "c"]
    assert list(pic.words_.values())[0] == 1

    val = {"a": -0.7, "b": -0.3, "c": 0.1, "d": -0.5}
    wc = CoefficientWordCloud()
    pic = wc.heatmap_to_wordcloud(val)

    assert list(pic.words_.keys()) == ["a", "d", "b", "c"]
    assert list(pic.words_.values())[0] == 1

    val = {"a": -0.7, "b": -0.3, "c": -0.1, "d": -0.5}
    wc = CoefficientWordCloud()
    pic = wc.heatmap_to_wordcloud(val)

    assert list(pic.words_.keys()) == ["a", "d", "b", "c"]
    assert list(pic.words_.values())[0] == 1

def test_coefficent_color():
    val = {"a": 0.7, "b": -0.3, "c": 0.1, "d": -0.5, "e": 0}
    color_word = CoefficentColor(val, cmap="RdBu_r").word_to_color
    # positive number should be red, negative, blue on the RdBu_r colormap
    # map should be zero centred
    assert color_word["e"] == _get_color_hex(0.5, "RdBu_r")
    assert color_word["a"] == _get_color_hex(1.0, "RdBu_r")


def test_overwrite_font():
    # over write font by user
    wc = CoefficientWordCloud(font_path=testdata)
    assert "font.ttf" in wc.font_path