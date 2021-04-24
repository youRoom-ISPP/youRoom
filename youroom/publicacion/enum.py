from enum import Enum
from django.utils.translation import ugettext_lazy as _


class Categorias(Enum):
    DORMITORIO = 'DORMITORIO'
    SALON = 'SALON'
    ENTRADITA = 'ENTRADITA'
    ESCRITORIO = 'ESCRITORIO'
    COCINA = 'COCINA'
    ASEO = 'ASEO'
    EXTERIOR = "EXTERIOR"


    @classmethod
    def choices(cls):
        return (
            (str(cls.DORMITORIO), _('Dormitorio')),
            (str(cls.SALON), _('Salón')),
            (str(cls.ENTRADITA), _('Entradita')),
            (str(cls.ESCRITORIO), _('Escritorio')),
            (str(cls.COCINA), _('Cocinita')),
            (str(cls.ASEO), _('Aseo')),
            (str(cls.EXTERIOR), _('Exterior')),
        )