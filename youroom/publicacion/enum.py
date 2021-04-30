from enum import Enum
from django.utils.translation import ugettext_lazy as _


class Categorias(Enum):
    ATICO = 'ATICO'
    BALCON = 'BALCON'
    BANYO = 'BAÑO'
    COBERTIZO = 'COBERTIZO'
    COCINA = 'COCINA'
    COMEDOR = 'COMEDOR'
    CUARTO = 'CUARTO'
    DORMITORIO = 'DORMITORIO'
    ENTRADA = 'ENTRADA'
    ESCALERA = 'ESCALERA'
    ESCRITORIO = 'ESCRITORIO'
    GARAJE = 'GARAJE'
    JARDIN = 'JARDIN'
    LAVANDERIA = 'LAVANDERIA'
    PARED = 'PARED'
    PASILLO = 'PASILLO'
    PATIO = 'PATIO'
    PORCHE = 'PORCHE'
    SALON = 'SALON'
    SOTANO = 'SOTANO'
    VESTIBULO = 'VESTIBULO'
    GIMNASIO = 'GIMNASIO'


    @classmethod
    def choices(cls):
        return (
            (str(cls.ATICO), _('Ático')),
            (str(cls.BALCON), _('Balcón')),
            (str(cls.BANYO), _('Baño')),
            (str(cls.COBERTIZO), _('Cobertizo')),
            (str(cls.COCINA), _('Cocina')),
            (str(cls.COMEDOR), _('Comedor')),
            (str(cls.CUARTO), _('Cuarto')),
            (str(cls.DORMITORIO), _('Dormitorio')),
            (str(cls.ENTRADA), _('Entrada')),
            (str(cls.ESCALERA), _('Escalera')),
            (str(cls.ESCRITORIO), _('Escritorio')),
            (str(cls.GARAJE), _('Garaje')),
            (str(cls.GIMNASIO), _('Gimnasio')),
            (str(cls.JARDIN), _('Jardín')),
            (str(cls.LAVANDERIA), _('Lavandería')),
            (str(cls.PARED), _('Pared')),
            (str(cls.PASILLO), _('Pasillo')),
            (str(cls.PATIO), _('Patio')),
            (str(cls.PORCHE), _('Porche')),
            (str(cls.SALON), _('Salón')),
            (str(cls.SOTANO), _('Sótano')),
            (str(cls.VESTIBULO), _('Vestíbulo')),

        )