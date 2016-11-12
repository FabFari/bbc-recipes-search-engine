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
        """To retrieve the ParsedEntry's term

            ParsedEntry's term attribute getter method.
            To get the term in string format.

            :return: The ParsedEntry's term
        """
        return self.term

    def get_doc_id(self):
        """To retrieve the ParsedEntry's doc_id

            ParsedEntry's doc_id attribute getter method.
            To get id of the document the ParsedEntry belongs to.

            :return: The ParsedEntry's doc_id
        """
        return self.docID

    def get_doc_position(self):
        """To retrieve the ParsedEntry's doc_position

            ParsedEntry's doc_position attribute getter method.
            To get the ParsedEntry's position in the belonging document.

            :return: The ParsedEntry's doc_position
        """
        return self.doc_position

    def set_doc_position(self, new_pos):
        """To updated the ParsedEntry's doc_position

            ParsedEntry's doc_position attribute setter method.
            To set the ParsedEntry's position in the belonging document.

            :param new_pos: The new ParsedEntry's doc_position
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
        """To retrieve the LabeledList's my_list

            LabeledList's my_list attribute getter method.
            To get the list the LabeledList wraps.

            :return: The LabeledList's my_list
        """
        return self.my_list

    def get_value(self):
        """To retrieve the LabeledList's value

            LabeledList's value attribute getter method.
            To get the value associated to the list
            wrapped by the LabeledList object.

            :return: The LabeledList's value
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
        """To retrieve the DocEntry's id

            DocEntry's id attribute getter method.
            To get the id associated to the DocEntry's document

            :return: The DocEntry's id
        """
        return self.id

    def set_id(self, id):
        """To update the DocEntry's id

            DocEntry's id attribute setter method.
            To set the id associated to the DocEntry's document

            :param id: The new document id
            :return: Nothing (void)
        """
        self.id = id

    def get_name(self):
        """To retrieve the DocEntry's name

            DocEntry's name attribute getter method.
            To get the filename of the DocEntry's document

            :return: The DocEntry's name
        """
        return self.name

    def set_name(self, name):
        """To update the DocEntry's name

            DocEntry's name attribute setter method.
            To set the filename of the DocEntry's document

            :param name: The new document filename
            :return: Nothing (void)
        """
        self.name = name

    def get_size(self):
        """To retrieve the DocEntry's size

            DocEntry's size attribute getter method.
            To get the size of the DocEntry's document

            :return: The DocEntry's size
        """
        return self.size

    def set_size(self, size):
        self.size = size

    def get_title(self):
        """To retrieve the DocEntry's title

            DocEntry's title attribute getter method.
            To get the title of the DocEntry's document

            :return: The DocEntry's title
        """
        return self.title

    def set_title(self, title):
        self.title = title

    def get_title_size(self):
        """To retrieve the DocEntry's title_size

            DocEntry's title_size attribute getter method.
            To get the title size of the DocEntry's document

            :return: The DocEntry's title_size
        """
        return self.title_size

    def set_title_size(self, size):
        self.title_size = size

    def get_size_ingr(self):
        """To retrieve the DocEntry's size_ingr

            DocEntry's size_ingr attribute getter method.
            To get the ingredient size of the DocEntry's document

            :return: The DocEntry's size_ingr
        """
        return self.size_ingr

    def set_size_ingr(self, len_ingr):
        self.size_ingr = len_ingr

    def get_desc(self):
        """To retrieve the DocEntry's desc

            DocEntry's desc attribute getter method.
            To get the description of the DocEntry's document

            :return: The DocEntry's desc
        """
        return self.desc

    def set_desc(self, desc):
        self.desc = desc

    def get_img_url(self):
        """To retrieve the DocEntry's img_url

            DocEntry's img_url attribute getter method.
            To get the image's url of the DocEntry's document

            :return: The DocEntry's img_url
        """
        return self.img_url

    def set_img_url(self, img_url):
        self.img_url = img_url

    def is_veggie(self):
        """To retrieve the DocEntry's veggie

            DocEntry's veggie attribute getter method.
            To get the dietary information of the DocEntry's document

            :return: The DocEntry's veggie
        """
        return self.veggie

    def set_veggie(self, veggie):
        self.veggie = veggie

    def str(self):
        return "{" + str(self.id) + " " + str(self.name) + " " + str(self.size) + "}"

    def __repr__(self):
        return "{%s %s %s}" % (self.id, self.name, self.size)

    def __str__(self):
        return "{%s %s %s}" % (self.id, self.name, self.size)
