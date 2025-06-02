from matplotlib.font_manager import FontSuperfamily


def test_font_superfamily_basic_resolution():
    sf = FontSuperfamily.get_superfamily("Roboto")
    sf.register("serif", "Roboto Serif")
    sf.register("sans", "Roboto")
    sf.register("mono", "Roboto Mono")

    assert sf.get_family("serif") == "Roboto Serif"
    assert sf.get_family("sans") == "Roboto"
    assert sf.get_family("mono") == "Roboto Mono"
    assert sf.get_family("fantasy") is None
