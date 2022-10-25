import argparse
import kerningvalidator
import sys


def main():
    parser = argparse.ArgumentParser(description="Compare font source file kerning with font binary file kerning.")
    parser.add_argument("-s", dest="source", help="Source font file (.glyphs)")
    parser.add_argument("-b", dest="binary", help="Binary font file (.ttf)")

    args = parser.parse_args()

    missing_kerning = list(kerningvalidator.missing_kerning(args.source, args.binary))
    if missing_kerning:
        sys.exit(1)


if __name__ == "__main__":
    main()
