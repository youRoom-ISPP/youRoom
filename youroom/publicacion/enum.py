from enum import Enum
from django.utils.translation import ugettext_lazy as _

class Categorias(Enum):
    DORMITORIO = 'DORMITORIO'
    SALON = 'SALON'
    ENTRADITA = 'ENTRADITA'
    ESCRITORIO = 'ESCRITORIO'
    COCINA = 'COCINA'


    @classmethod
    def choices(cls):
        return (
            (str(cls.DORMITORIO), _('DORMITORIO')),
            (str(cls.SALON), _('SALON')),
            (str(cls.ENTRADITA), _('ENTRADITA')),
            (str(cls.ESCRITORIO), _('ESCRITORIO')),
            (str(cls.COCINA), _('COCINA')),
        )