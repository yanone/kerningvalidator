import kerningvalidator
import os

PATH = os.path.join(os.path.dirname(__file__))
print(PATH)


def test_kerning():
    source = os.path.join(PATH, "data", "testfont.glyphs")
    binary = os.path.join(PATH, "data", "Testfont-Regular.ttf")
    assert len(kerningvalidator.missing_kerning(source, binary)) == 0
