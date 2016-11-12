from json import JSONEncoder
from json import JSONDecoder
from data_structures import LabeledList
from utils.data_structures import DocEntry


class LabeledListEncoder(JSONEncoder):
    """JSONEncoder implementation for class LabeledList

        Summary:
            This class is used to encode a LabeledList object,
            returning the serializable object representation
            for the LabeledList object. It's used to write a
            JSON file starting from a list of LabeledList objects,
            when using it in combination with json.dumps().
    """
    def default(self, obj):
        """To serialize a LabeledList object

            The default method implementation for LabeledListEncoder class.
            It returns the serializable object for obj, or calls the base implementation

            :param obj: The LabeledList object to be turn into a serialized one
            :return: The serialized object for obj
            :raises: TypeError
        """
        if isinstance(obj, LabeledList):
            return {
                '__type__': 'LabeledList',
                'label': obj.get_label(),
                'my_list': obj.get_my_list(),
                'value': obj.get_value(),
            }
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, obj)


class LabeledListDecoder(JSONDecoder):
    """JSONDecoder implementation for class LabeledList

        Summary:
            This class is used to decode a LabeledList object
            starting from a dictionary (serializable object)
            representation of a LabeledList object. It's used to
            deserialize the dictionary objects read from a JSON
            file when using it in combination with json.load().
    """
    def __init__(self, *args, **kargs):
        """LabeledListDecoder __init__ method

            LabeledListDecoder __init__ method.
            Used to specify to the parent class the
            dict_to_object implementation method as
            object_hook, used when deserializing objects,

        :param args: __init__ args
        :param kargs: __init__ kargs
        """
        JSONDecoder.__init__(self, object_hook=self.dict_to_object, *args, **kargs)

    @staticmethod
    def dict_to_object(d):
        """To deserialize dictionary representation of LabeledList objects

            This method is to be used as an object_hook when a dictionary
            object has to be deserialized to obtain a LabeledList one.
            It will be called with the result of every JSON object decoded
            and its return value will be used in place of the given dict.

        :param d: The dictionary object representation to be deserialized
        :return: The LabeledList object for d
        """
        if '__type__' not in d:
            return d

        obj_type = d.pop('__type__')
        try:
            dateobj = LabeledList(**d)
            return dateobj
        except:
            d['__type__'] = obj_type
            return d


class DocEntryEncoder(JSONEncoder):
    """JSONEncoder implementation for class DocEntry

        Summary:
            This class is used to encode a DocEntry object,
            returning the serializable object representation
            for the DocEntry object. It's used to write a
            JSON file starting from a list of DocEntry objects,
            when using it in combination with json.dumps().
    """
    def default(self, obj):
        """To serialize a DocEntry object

            The default method implementation for DocEntryEncoder class.
            It returns the serializable object for obj, or calls the base implementation

            :param obj: The DocEntry object to be turn into a serialized one
            :return: The serialized object for obj
            :raises: TypeError
        """
        if isinstance(obj, DocEntry):
            return {
                '__type__': 'DocEntry',
                'id': obj.get_id(),
                'name': obj.get_name(),
                'size': obj.get_size(),
                'title': obj.get_title(),
                'title_size': obj.get_title_size(),
                'desc': obj.get_desc(),
                'size_ingr': obj.get_size_ingr(),
                'img_url': obj.get_img_url(),
                'veggie': obj.is_veggie(),
            }
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, obj)


class DocEntryDecoder(JSONDecoder):
    """JSONDecoder implementation for class DocEntry

        Summary:
            This class is used to decode a DocEntry object
            starting from a dictionary (serializable object)
            representation of a DocEntry object. It's used to
            deserialize the dictionary objects read from a JSON
            file when using it in combination with json.load().
    """
    def __init__(self, *args, **kargs):
        """DocEntryDecoder __init__ method

            DocEntryDecoder __init__ method.
            Used to specify to the parent class the
            dict_to_object implementation method as
            object_hook, used when deserializing objects,

        :param args: __init__ args
        :param kargs: __init__ kargs
        """
        JSONDecoder.__init__(self, object_hook=self.dict_to_object, *args, **kargs)

    @staticmethod
    def dict_to_object(d):
        """To deserialize dictionary representation of DocEntry objects

            This method is to be used as an object_hook when a dictionary
            object has to be deserialized to obtain a DocEntry one.
            It will be called with the result of every JSON object decoded
            and its return value will be used in place of the given dict.

        :param d: The dictionary object representation to be deserialized
        :return: The DocEntry object for d
        """
        if '__type__' not in d:
            return d

        obj_type = d.pop('__type__')
        try:
            dateobj = DocEntry(**d)
            return dateobj
        except:
            d['__type__'] = obj_type
            return d
