import logging
import glyphsLib
from .source import build_kerning_classes, unicodes_for_glyph_or_class, glyph_for_unicode
import vharfbuzz as vhb


def buf_x_translate(hb_font, buf):
    x_translate = 0
    x_cursor = 0
    y_cursor = 0
    paths = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        dx, dy = pos.position[0], pos.position[1]
        x_translate = max(x_translate, x_cursor + dx)
        x_cursor += pos.position[2]
        y_cursor += pos.position[3]
    return x_translate


def width(hb_font, variations, string, kerning):
    """Get kerning of string."""

    hb_buf = hb_font.shape(string, {"features": {"kern": kerning}, "variations": variations})
    x_translate = buf_x_translate(hb_font, hb_buf)
    return x_translate


def shaped_kerning(hb_font, variations, string):
    """Compare width of string with and without kerning."""

    return width(hb_font, variations, string, True) - width(hb_font, variations, string, False)


def missing_kerning(glyphs_source, font_binary):
    """Compare kerning between source and binary font files."""

    problems = []

    # Open source font file
    source = glyphsLib.load(glyphs_source)

    kerning_classes = build_kerning_classes(source)
    # print(kerning_classes)

    # Harfbuzz
    hb_font = vhb.Vharfbuzz(font_binary)

    # Cycle through kerning dictionaries
    for direction, kerning_data in (
        ("LTR", source.kerningLTR),
        ("RTL", source.kerningRTL),
    ):
        for master_id in kerning_data:

            # Assemble variations matrix
            variations = {}
            for i, axis in enumerate(source.axes):
                variations[axis.axisTag] = source.masters[master_id].axes[i]
            print(f"Checking master: variations: {variations}, direction: {direction}")

            for first in kerning_data[master_id]:

                # Complain about missing first glyph or class
                if first.startswith("@"):
                    if first not in kerning_classes:
                        logging.warning(f"Kerning found but class not defined for first in pair: {first}")
                else:
                    if first not in source.glyphs:
                        logging.warning(f"Kerning found but glyph not defined for first in pair: {first}")

                # Found first glyph or class
                if first in kerning_classes or first in source.glyphs:

                    for second in kerning_data[master_id][first]:

                        # Complain about missing second glyph or class
                        if second.startswith("@"):
                            if second not in kerning_classes:
                                logging.warning(f"Kerning found but class not defined for second in pair: {second}")
                        else:
                            if second not in source.glyphs:
                                logging.warning(f"Kerning found but glyph not defined for second in pair: {second}")

                        # Found second glyph or class
                        if second in kerning_classes or second in source.glyphs:
                            first_unicodes = unicodes_for_glyph_or_class(source, first, kerning_classes)
                            second_unicodes = unicodes_for_glyph_or_class(source, second, kerning_classes)

                            # Cycle through all unicode combinations
                            for first_unicode in first_unicodes:
                                first_glyph = glyph_for_unicode(source, first_unicode)
                                for second_unicode in second_unicodes:
                                    second_glyph = glyph_for_unicode(source, second_unicode)
                                    found = shaped_kerning(
                                        hb_font,
                                        variations,
                                        f"{chr(int(first_unicode, 16))}{chr(int(second_unicode, 16))}",
                                    )

                                    # Class kerning
                                    expected = kerning_data[master_id][first][second]
                                    difference = found - expected

                                    if difference < -1 or difference > 1:
                                        # Kerning exceptions
                                        if first_glyph and second_glyph:
                                            first_name = first_glyph.name
                                            second_name = second_glyph.name

                                            if (
                                                first_name in kerning_data[master_id]
                                                and second_name in kerning_data[master_id][first_name]
                                            ):
                                                expected = kerning_data[master_id][first_name][second_name]

                                            elif (
                                                first in kerning_data[master_id]
                                                and second_name in kerning_data[master_id][first]
                                            ):
                                                expected = kerning_data[master_id][first][second_name]

                                            elif (
                                                first_name in kerning_data[master_id]
                                                and second in kerning_data[master_id][first_name]
                                            ):
                                                expected = kerning_data[master_id][first_name][second]

                                    difference = found - expected

                                    # Allow 1 unit difference for rounding errors
                                    if difference < -1 or difference > 1:
                                        first_unicode_as_str = f"{int(first_unicode, 16):#0{6}x}"
                                        second_unicode_as_str = f"{int(second_unicode, 16):#0{6}x}"
                                        logging.error(
                                            f"Not in font: dir: {direction}, var: {variations}, 1st:"
                                            f" {first} ({chr(int(first_unicode, 16))} {first_unicode_as_str} '{first_glyph.name}'),"
                                            " 2nd:"
                                            f" {second} ({chr(int(second_unicode, 16))} {second_unicode_as_str} '{second_glyph.name}'),"
                                            f" expected: {expected}, found: {found})"
                                        )
                                        problems.append(
                                            (
                                                variations,
                                                first,  # group or glyph name
                                                chr(int(first_unicode, 16)),  # encoded character
                                                int(first_unicode, 16),  # 1st unicode (decimal)
                                                second,  # group or glyph name
                                                chr(int(second_unicode, 16)),  # encoded character
                                                int(second_unicode, 16),  # 2nd unicode (decimal)
                                                expected,  # expected
                                                found,  # found
                                            )
                                        )
    return problems
