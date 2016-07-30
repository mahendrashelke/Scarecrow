import inspect
import json


class Config:
    """The config object, created from a json file"""
    def __init__(self, file, **options):
        self.file = file
        self.encoding = options.pop('encoding', None)
        self.object_hook = options.pop('object_hook', _ConfigDecoder().decode)
        self.encoder = options.pop('encoder', _ConfigEncoder)

        try:
            with open(self.file, 'r', encoding=self.encoding) as fp:
                self._data = json.load(fp, object_hook=self.object_hook)
        except FileNotFoundError:
            self._data = {}

    def save(self):
        """Saves the config on disk"""
        with open(self.file, 'w', encoding=self.encoding) as fp:
            json.dump(self._data, fp, ensure_ascii=True, cls=self.encoder)

    # utility

    def __contains__(self, *args, **kwargs):
        return self._data.__contains__(*args, **kwargs)

    def __len__(self):
        return self._data.__len__()

    def __getattr__(self, item, default=None):
        return getattr(self._data, item, default)

    def set(self, key, val):
        self._data[key] = val


class ConfigElement:
    pass


class _ConfigEncoder(json.JSONEncoder):
    """Default JSON encoder."""
    def default(self, o):
        if isinstance(o, ConfigElement):
            d = o.__dict__.copy()
            d['__class__'] = o.__class__.__qualname__
            return d

        return json.JSONEncoder.default(self, o)


class _ConfigDecoder:
    """Default JSON decoder, do not instantiate as the inspect magic involved is not tailored for it."""
    def __init__(self):
        # Back once to reach Config.__init__
        # Back twice to reach the caller
        self._globals = inspect.currentframe().f_back.f_back.f_globals

    def decode(self, o):
        if '__class__' in o:
            name = o['__class__']

            # Get the top level class in the given name
            parts = name.split('.')
            cls = self._globals[parts[0]]

            # Walk the rest of the dotted path if any
            for part in parts[1:]:
                cls = cls.__dict__[part]

            del o['__class__']
            return cls(**o)
        else:
            return o
