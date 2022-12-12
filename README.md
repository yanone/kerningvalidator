# Kerning Validator

Compares kerning defined in `.glyphs` source with kerning defined in binary font.

It reads all kerning pairs of all masters of a Variable Font from the `.glyphs` source
and shapes the pairs using the binary font with `vharfbuzz`, once with and once without 
kerning enabled, then compares the two values.

To catch absolutely all kerning, it gathers all unicodes associated with a kerning class
and cross-checks all possible combinations. This is necessary because members of a kerning class
may be part of different writing scripts and may or may not be included in the font based on their script.

The shaped kerning is lazily read from the `vharfbuzz` buffer through the `x` value of `buf.glyph_positions`
by simply comparing the highest `x` value of each composition.

## Invocation

From the command line:

`kerningvalidator font.glyphs font.ttf`

From within Python:
```python
from kerningvalidator import missing_kerning

# Convert this to list() as missing_kerning() is a generator
# and will otherwise return instantly without results
missing_kerning = list(missing_kerning("font.glyphs", "font.ttf"))
```

## Limitations

1. This tool was written with Variable Fonts in mind that contain both `LTR` and `RTL` kerning pairs
1. This tool currently only consumes `.glyphs` sources, no UFOs
1. The kerning comparisons are currently limited to encoded glyphs only
1. The `vharfbuzz` shaping has shown a difference of up to 1 font unit compared to the kerning defined in the `.glyphs` source. The tool therefore allows for 1 unit difference
1. There are currently no unit tests for this tool
1. It takes forever for a large font


## Package

To create a new package, install twine via `pip install twine`, then `cd` to `Lib/` and then:

* `python setup.py sdist`
* `twine upload dist/*`
