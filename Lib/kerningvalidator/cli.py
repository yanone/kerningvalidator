import argparse
import kerningvalidator
import sys


def main():
    parser = argparse.ArgumentParser(description="Compare font source file kerning with font binary file kerning.")
    parser.add_argument(dest="glyphs_source", help="Glyphs source font file (.glyphs)")
    parser.add_argument(dest="binary", help="Binary font file (.ttf/.otf)")

    args = parser.parse_args()

    missing_kerning = kerningvalidator.missing_kerning(args.glyphs_source, args.binary)
    if missing_kerning:
        sys.exit(1)


if __name__ == "__main__":
    main()
