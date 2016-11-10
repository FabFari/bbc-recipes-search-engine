class ParsedEntry:
    def __init__(self, term, doc_id, doc_position):
        self.term = term
        self.docID = doc_id
        self.doc_position = doc_position

    def get_term(self):
        return self.term

    def get_doc_id(self):
        return self.docID

    def get_doc_position(self):
        return self.doc_position

    def set_doc_position(self, new_pos):
        self.doc_position = new_pos

    def get_string(self):
        return str(self.term) + ' ' + str(self.docID) + ' ' + str(self.doc_position)


class LabeledList:
    def __init__(self, label, my_list, value=None):
        self.label = label
        self.my_list = my_list
        if value:
            self.value = value
        else:
            self.value = 0.0

    def get_label(self):
        return self.label

    def get_my_list(self):
        return self.my_list

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def str(self):
        return "{" + str(self.label) + " " + str(self.value) + " " + str(self.my_list) + "}"

    def __repr__(self):
        return "{%s %s %s}" % (self.label, self.value, self.my_list)

    def __str__(self):
        return "{%s %s %s}" % (self.label, self.value, self.my_list)


class DocEntry:
    def __init__(self, id=None, name=None, size=0, title=None, title_size=0, desc=None, img_url=None, size_ingr=0, veggie=False):
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
        return self.id

    def set_id(self, id):
        self.id = id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_size(self):
        return self.size

    def set_size(self, size):
        self.size = size

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def set_title_size(self, size):
        self.title_size = size

    def get_title_size(self):
        return self.title_size

    def get_size_ingr(self):
        return self.size_ingr

    def set_size_ingr(self, len_ingr):
        self.size_ingr = len_ingr

    def get_desc(self):
        return self.desc

    def set_desc(self, desc):
        self.desc = desc

    def get_img_url(self):
        return self.img_url

    def set_img_url(self, img_url):
        self.img_url = img_url

    def is_veggie(self):
        return self.veggie

    def set_veggie(self, veggie):
        self.veggie = veggie



    def str(self):
        return "{" + str(self.id) + " " + str(self.name) + " " + str(self.size) + "}"

    def __repr__(self):
        return "{%s %s %s}" % (self.id, self.name, self.size)

    def __str__(self):
        return "{%s %s %s}" % (self.id, self.name, self.size)