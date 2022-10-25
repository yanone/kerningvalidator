# Kerning Validator

Compares kerning defined in `.glyphs` source with kerning defined in binary font.
This is currently limited to encoded glyphs only.

It reads all kerning pairs of all masters of a Variable Font from the `.glyphs` source
and shapes the pairs using the binary font with `vharfbuzz`, once with and once without 
kerning enabled, then compares the two values.

To catch absolutely all kerning, it gathers all unicodes associated with a kerning class
and cross-checks all possible combinations. This is necessary because members of a kerning class
may be part of different writing scripts.

## Invocation

From the command line:
`kerningvalidator -s font.glyphs -b font.ttf`

From within Python:
```python
import kerningvalidator

missing_kerning = list(kerningvalidator.missing_kerning(source_path, binary_path))
```

## Limitations

This tool was written with Variable Fonts in mind that contain both `LTR` and `RTL` kerning pairs.