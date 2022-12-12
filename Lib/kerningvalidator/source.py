def build_kerning_classes(source):
    """Build kerning classes from source font file."""
    kerning_classes = {}
    for glyph in source.glyphs:

        if glyph.leftKerningGroup:
            first_group = f"@MMK_R_{glyph.leftKerningGroup}"
            if first_group not in kerning_classes:
                kerning_classes[first_group] = []
            if glyph.name not in kerning_classes[first_group]:
                kerning_classes[first_group].append(glyph.name)

        if glyph.rightKerningGroup:
            second_group = f"@MMK_L_{glyph.rightKerningGroup}"
            if second_group not in kerning_classes:
                kerning_classes[second_group] = []
            if glyph.name not in kerning_classes[second_group]:
                kerning_classes[second_group].append(glyph.name)

    return kerning_classes


def unicodes_for_glyph_or_class(font, glyph_or_class, kerning_classes):
    """Return first found unicode for glyph or class."""
    if glyph_or_class.startswith("@"):
        unicodes = []
        for glyph_name in kerning_classes[glyph_or_class]:
            unicodes.extend(font.glyphs[glyph_name].unicodes)
        return unicodes
    else:
        if font.glyphs[glyph_or_class].unicodes:
            return font.glyphs[glyph_or_class].unicodes
        else:
            return []


def glyph_for_unicode(font, unicode):
    """Return glyph for unicode."""
    for glyph in font.glyphs:
        if unicode in glyph.unicodes:
            return glyph
