import matplotlib as mpl
from matplotlib.font_manager import FontSuperfamily, FontProperties


# Define a testable superfamily registry for isolated tests
def setup_superfamily():
    sf = FontSuperfamily.get_superfamily("TestFamily")
    sf.register("serif", "Test Serif")
    sf.register("serif", "Test Serif Bold", weight="bold")
    sf.register("sans", "Test Sans")
    sf.register("mono", "Test Mono", weight="bold", style="italic")
    return sf


# Create test functions
def test_register_and_get_family_default():
    sf = setup_superfamily()
    assert sf.get_family("serif") == "Test Serif"


def test_get_family_with_weight():
    sf = setup_superfamily()
    assert sf.get_family("serif", weight="bold") == "Test Serif Bold"


def test_get_family_with_style_and_weight():
    sf = setup_superfamily()
    assert sf.get_family("mono", weight="bold", style="italic") == "Test Mono"


def test_get_family_fallback_to_default():
    sf = setup_superfamily()
    # This should fallback to "normal-normal" entry
    assert sf.get_family("sans", weight="light") == "Test Sans"


def test_get_family_not_found_returns_none():
    sf = setup_superfamily()
    assert sf.get_family("fantasy") is None


# Validate FontProperties resolves the superfamily correctly
def test_fontproperties_with_superfamily(monkeypatch):
    setup_superfamily()
    # Inject rcParams temporarily
    monkeypatch.setitem(mpl.rcParams, "font.superfamily", "TestFamily")
    monkeypatch.setitem(mpl.rcParams, "font.family", "serif")

    fp = FontProperties(weight="bold")
    assert fp.get_family() == ["Test Serif Bold"]


def test_fontproperties_without_superfamily(monkeypatch):
    monkeypatch.setitem(mpl.rcParams, "font.family", "serif")
    monkeypatch.setitem(mpl.rcParams, "font.superfamily", None)

    fp = FontProperties()
    # Should not use the superfamily logic, and preserve original family
    assert fp.get_family() == ["serif"]


def test_get_family_with_nonexistent_weight_style_combination():
    sf = setup_superfamily()
    # Should fall back to default genre if exact match for weight+style doesn't exist
    assert sf.get_family("mono", weight="bold", style="oblique") == "Test Mono"


def test_fontproperties_superfamily_partial_match(monkeypatch):
    # Only genre match exists, weight and style do not
    setup_superfamily()
    monkeypatch.setitem(mpl.rcParams, "font.superfamily", "TestFamily")
    monkeypatch.setitem(mpl.rcParams, "font.family", "sans")

    # No specific weight/style for sans, should still resolve
    fp = FontProperties(weight="black", style="italic")
    assert fp.get_family() == ["Test Sans"]


def test_fontproperties_superfamily_not_defined(monkeypatch):
    # Superfamily name exists but no mapping for genre
    setup_superfamily()
    monkeypatch.setitem(mpl.rcParams, "font.superfamily", "TestFamily")
    monkeypatch.setitem(mpl.rcParams, "font.family", "fantasy")

    fp = FontProperties()
    # Should fall back to original family
    assert fp.get_family() == ["fantasy"]


def test_fontproperties_superfamily_unknown(monkeypatch):
    # Non-existent superfamily
    monkeypatch.setitem(mpl.rcParams, "font.superfamily", "UnknownFamily")
    monkeypatch.setitem(mpl.rcParams, "font.family", "serif")

    fp = FontProperties()
    # Should fall back to family as superfamily doesn't exist
    assert fp.get_family() == ["serif"]
