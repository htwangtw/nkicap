from ..plotting import PublicationWordCloud


def test_sort_value_abs():
    # the word cloud should be ordered by absolute value
    val = {"a": 0.7, "b": -0.3, "c": 0.1, "d": -0.5}
    wc = PublicationWordCloud()
    pic = wc.heatmap_to_wordcloud(val)

    assert list(pic.words_.keys()) == ["a", "d", "b", "c"]
    assert list(pic.words_.values())[0] == 1

    val = {"a": -0.7, "b": -0.3, "c": 0.1, "d": -0.5}
    wc = PublicationWordCloud()
    pic = wc.heatmap_to_wordcloud(val)

    assert list(pic.words_.keys()) == ["a", "d", "b", "c"]
    assert list(pic.words_.values())[0] == 1

    val = {"a": -0.7, "b": -0.3, "c": -0.1, "d": -0.5}
    wc = PublicationWordCloud()
    pic = wc.heatmap_to_wordcloud(val)

    assert list(pic.words_.keys()) == ["a", "d", "b", "c"]
    assert list(pic.words_.values())[0] == 1

# test for color

# check if certain seeting ignore user input