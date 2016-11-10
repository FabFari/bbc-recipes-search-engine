from json import JSONEncoder
from json import JSONDecoder
from data_structures import LabeledList
from utils.data_structures import DocEntry

class LabeledListEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, LabeledList):
            # return [obj.get_label(), obj.get_value(), obj.my_list]
            return {
                '__type__': 'LabeledList',
                'label': obj.get_label(),
                'my_list': obj.get_my_list(),
                'value': obj.get_value(),
            }
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, obj)


class LabeledListDecoder(JSONDecoder):
    def __init__(self, *args, **kargs):
        JSONDecoder.__init__(self, object_hook=self.dict_to_object, *args, **kargs)

    @staticmethod
    def dict_to_object(d):
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
    def default(self, obj):
        if isinstance(obj, DocEntry):
            # return [obj.get_label(), obj.get_value(), obj.my_list]
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
    def __init__(self, *args, **kargs):
        JSONDecoder.__init__(self, object_hook=self.dict_to_object, *args, **kargs)

    @staticmethod
    def dict_to_object(d):
        if '__type__' not in d:
            return d

        obj_type = d.pop('__type__')
        try:
            dateobj = DocEntry(**d)
            return dateobj
        except:
            d['__type__'] = obj_type
            return d
