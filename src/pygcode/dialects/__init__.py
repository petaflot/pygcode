__all__ = [
    'DEFAULT',

    # registration decorators
    'gcode_dialect',
    'word_dialect',

    # dialects
    'linuxcnc',
    'reprap',
    'prusa',
    'marlin2',
]


# Registration decorators
from .mapping import gcode_dialect
from .mapping import word_dialect

# Dialects
from . import linuxcnc
from . import reprap
from . import prusa
from . import marlin2


_DEFAULT = 'marlin2'


def get_default():
    """
    Get the default gcode interpreter dialect.
    (see :meth:`set_default` for details)
    """
    return _DEFAULT


def set_default(name):
    """
    Set the default gcode interpreter dialect.
    This dialect will be used if no other is specified for particular function
    calls.

    :param name: name of dialect
    :type name: :class:`str`

    .. doctest::

        >>> from pygcode import dialect
        >>> dialect.get_default()
        'linuxcnc'
        >>> dialect.set_default('reprap')
        >>> dialect.get_default()
        'reprap'

    """

    if name not in __all__:
        raise ValueError(f"'{name}' is not a valid dialect")
    _DEFAULT = name
