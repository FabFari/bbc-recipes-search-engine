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
    def __init__(self, id, name, size):
        self.id = id
        self.name = name
        self.size = size

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_size(self):
        return self.size

    def str(self):
        return "{" + str(self.id) + " " + str(self.name) + " " + str(self.size) + "}"

    def __repr__(self):
        return "{%s %s %s}" % (self.id, self.name, self.size)

    def __str__(self):
        return "{%s %s %s}" % (self.id, self.name, self.size)