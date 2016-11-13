import sys
import unicodedata
# Translation dictionary. Translation entries are
# added to this dictionary as needed.

CHAR_REPLACEMENT = {
    # latin-1 characters that don't have a unicode decomposition
    0xc6: u"AE",  # LATIN CAPITAL LETTER AE
    0xd0: u"D",  # LATIN CAPITAL LETTER ETH
    0xd8: u"OE",  # LATIN CAPITAL LETTER O WITH STROKE
    0xde: u"Th",  # LATIN CAPITAL LETTER THORN
    0xdf: u"ss",  # LATIN SMALL LETTER SHARP S
    0xe6: u"ae",  # LATIN SMALL LETTER AE
    0xf0: u"d",  # LATIN SMALL LETTER ETH
    0xf8: u"oe",  # LATIN SMALL LETTER O WITH STROKE
    0xfe: u"th",  # LATIN SMALL LETTER THORN
    0x2018: u"'",  # LEFT SINGLE QUOTATION MARK
    0x2019: u"'",  # RIGHT SINGLE QUOTATION MARK
    0x201c: u'"',  # LEFT DOUBLE QUOTATION MARK
    0x201d: u'"',  # RIGHT DOUBLE QUOTATION MARK
    0x215D: u".625",  # VULGAR FRACTION FIVE EIGHTHS
    0x215A: u".83",  # VULGAR FRACTION FIVE SIXTHS
    0x2158: u".8",  # VULGAR FRACTION FOUR FIFTHS
    0x215B: u".125",  # VULGAR FRACTION ONE EIGHTH
    0x2155: u".2",  # VULGAR FRACTION ONE FIFTH
    0x00BD: u".5",  # VULGAR FRACTION ONE HALF
    0x00BC: u".25",  # VULGAR FRACTION ONE QUARTER
    0x2159: u".16",  # VULGAR FRACTION ONE SIXTH
    0x2153: u".33",  # VULGAR FRACTION ONE THIRD
    0x215E: u".875",  # VULGAR FRACTION SEVEN EIGHTHS
    0x215C: u".375",  # VULGAR FRACTION THREE EIGHTHS
    0x2157: u".6",  # VULGAR FRACTION THREE FIFTHS
    0x00BE: u".75",  # VULGAR FRACTION THREE QUARTERS
    0x2156: u".4",  # VULGAR FRACTION TWO FIFTHS
    0x2154: u".66",  # VULGAR FRACTION TWO THIRDS
}


class UnicodeMapper(dict):
    """A class that provide replacement for unicode special characters

    Summary:
        This class is used to map a unicode character code (the key) to a
        replacement code (either a character code or a unicode string).
        It's used in the preprocessing phase to get rid of unicode characters
        not directly mapped to ones available also in ASCII.
    """

    def mapchar(self, key):
        """To convert a unicode special character to an ASCII compatible unicode string

            It's used to convert a unicode special character into a unicode
            string that can be directly converted to an ASCII one.
            To support the conversion it uses an hardcoded dictionary easily
            extensible with new unicode character codes.

            :param key: The unicode character code to be converted
            :return: The tag resulting from the conversion
        """
        ch = self.get(key)
        if ch is not None:
            return ch

        de = unicodedata.decomposition(unichr(key))
        if key not in CHAR_REPLACEMENT and de:
            try:
                ch = int(de.split(None, 1)[0], 16)
            except (IndexError, ValueError):
                ch = key
        else:
            ch = CHAR_REPLACEMENT.get(key, key)
        self[key] = ch
        return ch

    if sys.version >= "2.5":
        # use __missing__ where available
        __missing__ = mapchar
    else:
        # otherwise, use standard __getitem__ hook (this is slower,
        # since it's called for each character)
        __getitem__ = mapchar


def unicode_to_ascii(unicodestring):
    """To convert a unicode string to an ASCII one

    Converts a unicode string into an ASCII representation, converting
    all non-ascii characters into close approximations where possible.

    Special thanks to http://effbot.org/zone/unicode-convert.htm

    :param unicodestring: The unicode string to be translated
    :return: The ASCII translated version of the input string
    """
    charmap = UnicodeMapper()
    return unicodestring.translate(charmap).encode("ascii", "ignore")
