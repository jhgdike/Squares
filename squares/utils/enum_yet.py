from enum import Enum


class EnumYet(Enum):

    @classmethod
    def all(cls):
        return [(x.value, x.label) for x in cls if hasattr(x, 'label')]

    def __str__(self):
        return getattr(self, 'label', self.name)

    __repr__ = __str__
