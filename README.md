# Kerning Validator

Compares kerning defined in `.glyphs` source with kerning defined in binary font.

It reads all kerning pairs of all masters of a Variable Font from the `.glyphs` source
and shapes the pairs using the binary font with `vharfbuzz`, once with and once without 
kerning enabled, then compares the two values.

To catch absolutely all kerning, it gathers all unicodes associated with a kerning class
and cross-checks all possible combinations. This is necessary because members of a kerning class
may be part of different writing scripts and may or may not be included in the font based on their script.

## Invocation

From the command line:
`kerningvalidator -s font.glyphs -b font.ttf`

From within Python:
```python
from kerningvalidator import missing_kerning

# Convert this to list() as missing_kerning() is a generator
missing_kerning = list(missing_kerning(source_path, binary_path))
```

## Limitations

1. This tool was written with Variable Fonts in mind that contain both `LTR` and `RTL` kerning pairs
2. The tests are currently limited to encoded glyphs only
3. It takes forever