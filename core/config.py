import os
import yaml
import logging

logger = logging.getLogger(__name__)


def _env_var_constructor(loader, node):
    default = None

    key = loader.construct_scalar(node)
    value = os.getenv(key, default)

    return value


def _join_var_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return "".join(str(x) for x in fields)


yaml.SafeLoader.add_constructor("!ENV", _env_var_constructor)
yaml.SafeLoader.add_constructor("!JOIN", _join_var_constructor)

with open("config.yml", "r", encoding="UTF-8") as f:
    _CONFIG = yaml.safe_load(f)


class ConfigGetter(type):
    subsection = None

    def __getattr__(cls, name):
        name = name.lower()

        try:
            if cls.subsection is not None:
                return _CONFIG[cls.section][cls.subsection][name]
            return _CONFIG[cls.section][name]
        except KeyError as e:
            dotted_path = '.'.join((cls.section, cls.subsection,
                                    name) if cls.subsection is not None else (
                                        cls.section, name))
            logger.info(f"嘗試獲取 `{dotted_path}` 失敗")
            raise AttributeError(repr(name)) from e

    def __getitem__(cls, name):
        return cls.__getattr__(name)

    def __iter__(cls):
        for name in cls.__annotations__:
            yield name, getattr(cls, name)


class Bot(metaclass=ConfigGetter):
    section = "bot"


class Log(metaclass=ConfigGetter):
    section = "log"


class Emojis(metaclass=ConfigGetter):
    section = "styles"
    subsection = "emojis"


class Reactions(metaclass=ConfigGetter):
    section = "styles"
    subsection = "reactions"


class HelpMessages(metaclass=ConfigGetter):
    section = "help_messages"


class Events(metaclass=ConfigGetter):
    section = "events"


class Fun(metaclass=ConfigGetter):
    section = "fun"
