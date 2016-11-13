from nltk.corpus import wordnet as wn


def is_noun(tag):
    """To test if a tag is a Penn noun tag

        To test if a tag is a Penn noun tag.
        It returns True if the input tag belongs
        to the specified noun tags set.

        :param tag: The tag to be tested
        :return: True or False (boolean)
    """
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']


def is_verb(tag):
    """To test if a tag is a Penn verb tag

        To test if a tag is a Penn verb tag.
        It returns True if the input tag belongs
        to the specified verb tags set.

        :param tag: The tag to be tested
        :return: True or False (boolean)
    """
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


def is_adverb(tag):
    """To test if a tag is a Penn adverb tag

        To test if a tag is a Penn adverb tag.
        It returns True if the input tag belongs
        to the specified adverb tags set.

        :param tag: The tag to be tested
        :return: True or False (boolean)
    """
    return tag in ['RB', 'RBR', 'RBS']


def is_adjective(tag):
    """To test if a tag is a Penn adjective tag

        To test if a tag is a Penn adjective tag.
        It returns True if the input tag belongs
        to the specified adjective tags set.

        :param tag: The tag to be tested
        :return: True or False (boolean)
    """
    return tag in ['JJ', 'JJR', 'JJS']


def penn_to_wn(tag):
    """To convert a Penn tag to a Wordnet tag

        Tries to convert a Penn tag to a Wordnet tag.
        If a conversion is not available, a noun tag
        is returned instead, since as default the
        lemmization and stemming operations considers
        eveything as a noun (if not otherwise specified).
        Meant to be used to make the wordnet lemmization
        process more accurate.

        :param tag: The tag to be converted
        :return: The tag resulting from the conversion
    """
    if is_adjective(tag):
        return wn.ADJ
    elif is_noun(tag):
        return wn.NOUN
    elif is_adverb(tag):
        return wn.ADV
    elif is_verb(tag):
        return wn.VERB
    # Otherwise name as default
    return wn.NOUN
