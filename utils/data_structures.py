class ParsedEntry:
    """A single term parsed from documents TSV file

    Summary:
        This class is used to maintain the information of a single
        term parsed from the documents TSV file. It's used to
        construct the posting lists starting from the individual
        terms collected from the documents TSV file.


    Attributes:
        term = the term in string format
        doc_id = numerical id of the term's document
        doc_position = term's position within the document
    """
    def __init__(self, term, doc_id, doc_position):
        """ParsedEntry's __init__ method

            ParsedEntry's __init__ method.

            :param term: ParsedEntry's term
            :param doc_id: ParsedEntry's doc_id
            :param doc_position: ParsedEntry's doc_position
            :return: Nothing (void)
        """
        self.term = term
        self.docID = doc_id
        self.doc_position = doc_position

    def get_term(self):
        """To retrieve the ParsedEntry's term value

            ParsedEntry's term attribute getter method.
            To get the term in string format.

            :return: The ParsedEntry's term value
        """
        return self.term

    def get_doc_id(self):
        """To retrieve the ParsedEntry's doc_id value

            ParsedEntry's doc_id attribute getter method.
            To get id of the document the ParsedEntry belongs to.

            :return: The ParsedEntry's doc_id value
        """
        return self.docID

    def get_doc_position(self):
        """To retrieve the ParsedEntry's doc_position value

            ParsedEntry's doc_position attribute getter method.
            To get the ParsedEntry's position in the belonging document.

            :return: The ParsedEntry's doc_position value
        """
        return self.doc_position

    def set_doc_position(self, new_pos):
        """To updated the ParsedEntry's doc_position value

            ParsedEntry's doc_position attribute setter method.
            To set the ParsedEntry's position in the belonging document.

            :param new_pos: The new ParsedEntry's doc_position value
            :return: Nothing (void)
        """
        self.doc_position = new_pos

    def str(self):
        """To retrieve the ParsedEntry in string format

            Returns all the ParsedEntry information arranged as a string.

            :return: The ParsedEntry's string representation
        """
        return str(self.term) + ' ' + str(self.docID) + ' ' + str(self.doc_position)


class LabeledList:
    """A list wrapper with additional 'label' and 'value' attributes

    Summary:
        This class is used to represent both the terms posting lists
        and the document's entry in the posting lists.
        For a terms posting lists, the label represents the term
        itself and the value represents the term's IDF value, while the
        attribute my_list represents the posting list itself.
        For a document entry in the posting list, the label represents
        the document id and the value represents the TF of the term the
        posting list containing the entry belongs to, while the attribute
        my_list represents the position list of that term in the document.

    Attributes:
        term = the term in string format
        doc_id = numerical id of the term's document
        doc_position = term's position within the document
    """
    def __init__(self, label, my_list, value=None):
        """LabeledList's __init__ method

            LabeledList's __init__ method.

            :param label: ParsedEntry's label
            :param my_list: ParsedEntry's my_list
            :param value: ParsedEntry's value
            :return: Nothing (void)
        """
        self.label = label
        self.my_list = my_list
        if value:
            self.value = value
        else:
            self.value = 0.0

    def get_label(self):
        """To retrieve the LabeledList's label

            LabeledList's label attribute getter method.
            To get the label associated to the list
            wrapped by the LabeledList object.

            :return: The LabeledList's label
        """
        return self.label

    def get_my_list(self):
        """To retrieve the LabeledList's my_list value

            LabeledList's my_list attribute getter method.
            To get the list the LabeledList wraps.

            :return: The LabeledList's my_list value
        """
        return self.my_list

    def get_value(self):
        """To retrieve the LabeledList's value value

            LabeledList's value attribute getter method.
            To get the value associated to the list
            wrapped by the LabeledList object.

            :return: The LabeledList's value value
        """
        return self.value

    def set_value(self, value):
        """To updated the LabeledList's value

            LabeledList's value attribute setter method.
            To set the LabeledList's value associated to
            the list wrapped by the LabeledList object.

            :param value: The new LabeledList's value
            :return: Nothing (void)
        """
        self.value = value

    def str(self):
        """To retrieve the LabeledList in string format

            Returns all the LabeledList information arranged as a string.

            :return: The LabeledList's string representation
        """
        return "{" + str(self.label) + " " + str(self.value) + " " + str(self.my_list) + "}"

    def __repr__(self):
        """LabeledList's __repr__ method

            LabeledList's __repr__ method.

            :return: Unambiguous string representation of LabeledList
        """
        return "{%s %s %s}" % (self.label, self.value, self.my_list)

    def __str__(self):
        """LabeledList's __str__ method

            LabeledList's __str__ method.

            :return: Readable string representation of LabeledList
        """
        return "{%s %s %s}" % (self.label, self.value, self.my_list)


class DocEntry:
    """Useful object representation of a document

    Summary:
        This class is used to represent a document along with
        fields useful for the processing and the results
        presentation of a query ran by the query engine.

    Attributes:
        id = The id of the represented document
        name = The name of the document's file
        size = The size (# tokens) of the document
        title = The title of the document
        desc = The description of the document
        img_url = The url of the document image
        self.veggie = The dietary information of the document
        self.size_ingr = The size (# tokens) of the document's ingredients
        self.title_size = The size (# tokens) of the document's title
    """
    def __init__(self, id=None, name=None, size=0, title=None, title_size=0,
                 desc=None, img_url=None, size_ingr=0, veggie=False):
        """DocEntry's __init__ method

            DocEntry's __init__ method.

            :param id: DocEntry's document id
            :param name: DocEntry's document's filename
            :param size: DocEntry's document's size
            :param title: DocEntry's document's title
            :param title_size: DocEntry's document's title size
            :param desc: DocEntry's document's description
            :param img_url: DocEntry's document's image urls
            :param size_ingr: DocEntry's document's igredient's size
            :param veggie: DocEntry's document's dietary information
            :return: Nothing (void)
        """
        self.id = id
        self.name = name
        self.size = size
        self.title = title
        self.desc = desc
        self.img_url = img_url
        self.veggie = veggie
        self.size_ingr = size_ingr
        self.title_size = title_size

    def get_id(self):
        """To retrieve the DocEntry's id value

            DocEntry's id attribute getter method.
            To get the id associated to the DocEntry's document

            :return: The DocEntry's id value
        """
        return self.id

    def set_id(self, id):
        """To update the DocEntry's id value

            DocEntry's id attribute setter method.
            To set the id associated to the DocEntry's document

            :param id: The new document id value
            :return: Nothing (void)
        """
        self.id = id

    def get_name(self):
        """To retrieve the DocEntry's name value

            DocEntry's name attribute getter method.
            To get the filename of the DocEntry's document

            :return: The DocEntry's name value
        """
        return self.name

    def set_name(self, name):
        """To update the DocEntry's name value

            DocEntry's name attribute setter method.
            To set the filename of the DocEntry's document

            :param name: The new document name value
            :return: Nothing (void)
        """
        self.name = name

    def get_size(self):
        """To retrieve the DocEntry's size value

            DocEntry's size attribute getter method.
            To get the size of the DocEntry's document

            :return: The DocEntry's size value
        """
        return self.size

    def set_size(self, size):
        """To update the DocEntry's size value

            DocEntry's size attribute setter method.
            To set the size of the DocEntry's document

            :param size: The new document size value
            :return: Nothing (void)
        """
        self.size = size

    def get_title(self):
        """To retrieve the DocEntry's title value

            DocEntry's title attribute getter method.
            To get the title of the DocEntry's document

            :return: The DocEntry's title value
        """
        return self.title

    def set_title(self, title):
        """To update the DocEntry's title value

            DocEntry's title attribute setter method.
            To set the title of the DocEntry's document

            :param title: The new document title value
            :return: Nothing (void)
        """
        self.title = title

    def get_title_size(self):
        """To retrieve the DocEntry's title_size value

            DocEntry's title_size attribute getter method.
            To get the title size of the DocEntry's document

            :return: The DocEntry's title_size value
        """
        return self.title_size

    def set_title_size(self, title_size):
        """To update the DocEntry's title_size value

            DocEntry's title_size attribute setter method.
            To set the title's size of the DocEntry's document

            :param title_size: The new document title_size value
            :return: Nothing (void)
        """
        self.title_size = title_size

    def get_size_ingr(self):
        """To retrieve the DocEntry's size_ingr value

            DocEntry's size_ingr attribute getter method.
            To get the ingredient size of the DocEntry's document

            :return: The DocEntry's size_ingr value
        """
        return self.size_ingr

    def set_size_ingr(self, size_ingr):
        """To update the DocEntry's size_ingr value

            DocEntry's name attribute setter method.
            To set the ingredient's size of the DocEntry's document

            :param size_ingr: The new document size_ingr value
            :return: Nothing (void)
        """
        self.size_ingr = size_ingr

    def get_desc(self):
        """To retrieve the DocEntry's desc value

            DocEntry's desc attribute getter method.
            To get the description of the DocEntry's document

            :return: The DocEntry's desc value
        """
        return self.desc

    def set_desc(self, desc):
        """To update the DocEntry's desc value

            DocEntry's desc attribute setter method.
            To set the description of the DocEntry's document

            :param desc: The new document desc value
            :return: Nothing (void)
        """
        self.desc = desc

    def get_img_url(self):
        """To retrieve the DocEntry's img_url value

            DocEntry's img_url attribute getter method.
            To get the image's url of the DocEntry's document

            :return: The DocEntry's img_url value
        """
        return self.img_url

    def set_img_url(self, img_url):
        """To update the DocEntry's img_url value

            DocEntry's img_url attribute setter method.
            To set the image's url of the DocEntry's document

            :param img_url: The new document img_url value
            :return: Nothing (void)
        """
        self.img_url = img_url

    def is_veggie(self):
        """To retrieve the DocEntry's veggie value

            DocEntry's veggie attribute getter method.
            To see if the document is Vegetarian or not.

            :return: The DocEntry's veggie value
        """
        return self.veggie

    def set_veggie(self, veggie):
        """To update the DocEntry's veggie value

            DocEntry's veggie attribute setter method.
            To set the DocEntry's document as vegetarian or not

            :param veggie: The new document veggie value
            :return: Nothing (void)
        """
        self.veggie = veggie

    def str(self):
        """To retrieve the DocEntry in string format

            Returns all the DocEntry information arranged as a string.

            :return: The DocEntry's string representation
        """
        return "{" + str(self.id) + " " + str(self.name) + " " + str(self.size) + "}"

    def __repr__(self):
        """DocEntry's __repr__ method

            DocEntry's __repr__ method.

            :return: Unambiguous string representation of DocEntry
        """
        return "{%s %s %s}" % (self.id, self.name, self.size)

    def __str__(self):
        """DocEntry's __str__ method

            DocEntry's __str__ method.

            :return: Readable string representation of DocEntry
        """
        return "{%s %s %s}" % (self.id, self.name, self.size)
