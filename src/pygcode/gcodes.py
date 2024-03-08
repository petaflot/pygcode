import sys
from collections import defaultdict
from copy import copy
import six

from .utils import Vector3, Quaternion, quat2coord_system
from .words import Word, text2words

from .exceptions import GCodeParameterError, GCodeWordStrError

# Terminology of a "G-Code"
#   For the purposes of this library, so-called "G" codes do not necessarily
#   use the letter "G" in their word; other letters include M, F, S, and T
# Why?
#   I've seen documentation thrown around using the term "gcode" interchangably
#   for any word that triggers an action, or mode change. The fact that the
#   entire language is called "gcode" obfuscates any other convention.
#   Considering it's much easier for me to call everything GCode, I'm taking
#   the lazy route, so sue me (but seriously, please don't sue me).
#
# Modality groups
#   Modal GCodes:
#       A machine's "mode" can be changed by any gcode with a modal_group.
#       This state is retained by the machine in the blocks to follow until
#       the "mode" is revoked, or changed.
#       A typical example of this is units:
#           G20
#       this will change the machine's "mode" to treat all positions as
#       millimeters; G20 does not have to be on every line, thus the machine's
#       "mode" is in millimeters for that, and every block after it until G21
#       is specified (changing units to inches).
#
#   Modal Groups:
#       Only one mode of each modal group can be active. That is to say, a
#       modal g-code can only change the state of a previously set mode if
#       they're in the same group.
#       For example:
#           G20 (mm), and G21 (inches) are in group 6
#           G1 (linear movement), and G2 (arc movement) are in group 1
#       A machine can't use mm and inches at the same time, just as it can't
#       move in a straight line, and move in an arc simultaneously.
#
#   There are 15 groups:
#       ref: http://linuxcnc.org/docs/html/gcode/overview.html#_modal_groups
#       ref: https://www.haascnc.com/content/dam/haascnc/en/service/manual/operator/english---mill-ngc---operator's-manual---2017.pdf
#
#                 Table 5. G-Code Modal Groups
#       MODAL GROUP MEANING                     MEMBER WORDS
#       Non-modal codes (Group 0)               G4, G10 G28, G30, G53, G92, G92.1, G92.2, G92.3,
#       Motion (Group 1)                        G0, G1, G2, G3, G33, G38.x,
#       Plane selection (Group 2)               G17, G18, G19, G17.1, G18.1, G19.1
#       Distance Mode (Group 3)                 G90, G91
#       Arc IJK Distance Mode (Group 4)         G90.1, G91.1
#       Feed Rate Mode (Group 5)                G93, G94, G95
#       Units (Group 6)                         G20, G21
#       Cutter Diameter Compensation (Group 7)  G40, G41, G42, G41.1, G42.1
#       Tool Length Offset (Group 8)            G43, G43.1, G49
#       Can Cycles (Group 9)                    G73, G76, G80, G81, G82, G83,
#                                               G84, G85, G86, G87, G88, G89
#       Canned Cycles Return Mode (Group 10)    G98, G99
#       Coordinate System (Group 12)            G54, G55, G56, G57, G58, G59,
#                                               G59.1, G59.2, G59.3
#       Control Mode (Group 13)                 G61, G61.1, G64
#       Spindle Speed Mode (Group 14)           G96, G97
#       Lathe Diameter Mode (Group 15)          G7, G8
#
#                 Table 6. M-Code Modal Groups
#       MODAL GROUP MEANING                     MEMBER WORDS
#       Stopping (Group 4)                      M0, M1, M2, M30, M60
#       Spindle (Group 7)                       M3, M4, M5
#       Coolant (Group 8)                       (M7 M8 can both be on), M9
#       Override Switches (Group 9)             M48, M49
#       User Defined (Group 10)                 M100-M199
#

DIALECT_UNKNOWN = [False]
# TODO see https://github.com/petaflot/pygcode/issues/6 for a more complete 
from pygcode.dialects import get_default as get_default_dialect
import pygcode

MODAL_GROUP_MAP = {
    # "G" codes
    'motion': 1,
    'plane_selection': 2,
    'distance': 3,
    'arc_ijk_distance': 4,
    'feed_rate_mode': 5,
    'units': 6,
    'cutter_diameter_comp': 7,
    'tool_length_offset': 8,
    'canned_cycle': 9,
    'canned_cycles_return': 10,
    'coordinate_system': 12,
    'control_mode': 13,
    'spindle_speed_mode': 14,
    'lathe_diameter': 15,

    # "M" codes
    'stopping': 104,
    'spindle': 107,
    'coolant': 108,
    'override_switches': 109,
    'user_defined': 110,

    # Traditionally Non-grouped:
    #   Although these GCodes set the machine's mode, there are no other GCodes to
    #   group with them. So although they're modal, they don't have a defined
    #   modal group.
    #   However, having a modal group assists with:
    #       - validating gcode blocks for conflicting commands
    #       - remembering machine's state with consistency across gcodes
    #   Therefore, I've added F, S, and T GCodes to custom group numbers (> 200)
    'feed_rate': 201,
    'spindle_speed': 202,
    'tool': 203,
}

# Execution Order
#       Order taken http://linuxcnc.org/docs/html/gcode/overview.html#_g_code_order_of_execution
#         (as of 2017-07-03)
#       010: O-word commands (optionally followed by a comment but no other words allowed on the same line)
#       020: Comment (including message)
#       030: Set feed rate mode (G93, G94).
#       040: Set feed rate (F).
#       050: Set spindle speed (S).
#       060: Select tool (T).
#       070: HAL pin I/O (M62-M68).
#       080: Change tool (M6) and Set Tool Number (M61).
#       090: Spindle on or off (M3, M4, M5).
#       100: Save State (M70, M73), Restore State (M72), Invalidate State (M71).
#       110: Coolant on or off (M7, M8, M9).
#       120: Enable or disable overrides (M48, M49,M50,M51,M52,M53).
#       130: User-defined Commands (M100-M199).
#       140: Dwell (G4).
#       150: Set active plane (G17, G18, G19).
#       160: Set length units (G20, G21).
#       170: Cutter radius compensation on or off (G40, G41, G42)
#       180: Cutter length compensation on or off (G43, G49)
#       190: Coordinate system selection (G54, G55, G56, G57, G58, G59, G59.1, G59.2, G59.3).
#       200: Set path control mode (G61, G61.1, G64)
#       210: Set distance mode (G90, G91).
#       220: Set retract mode (G98, G99).
#       230: Go to reference location (G28, G30) or change coordinate system data (G10) or set axis offsets (G92, G92.1, G92.2, G94).
#       240: Perform motion (G0 to G3, G33, G38.x, G73, G76, G80 to G89), as modified (possibly) by G53.
#       250: Stop (M0, M1, M2, M30, M60).

match get_default_dialect():
    case 'marlin2':
        from .gcodes_marlin import *
    case 'prusa':
        from .gcodes_prusa import *
    case _:
        from .gcodes_lecacy import *

# ======================= Utilities =======================

def _subclasses_level(root_class, recursion_level=0):
    """
    Hierarcical list of all classes inheriting from the given root class (recursive)
    :param root_class: class used as trunk of hierarchy (included inoutput)
    :param recursion_level: should always be 0 (unless recursively called)
    :param
    """
    yield (root_class, recursion_level)
    for cls in sorted(root_class.__subclasses__(), key=lambda c: c.__name__):
        for (sub, level) in _subclasses_level(cls, recursion_level+1):
            yield (sub, level)


def _subclasses(root_class):
    """Flat list of all classes inheriting from the given root class (recursive)"""
    for (cls, level) in _subclasses_level(root_class):
        yield cls


def _gcode_class_infostr(base_class=GCode, prefix=''):
    """
    List all ineheriting classes for the given gcode class
    :param base_class: root of hierarcy
    :return: str listing all gcode classes
    """
    info_str = ""
    for (cls, level) in _subclasses_level(base_class):
        word_str = ''
        if cls.word_key:
            word_str = str(cls.word_key)
        info_str += "{prefix}{word} {indent}- {name}: {description}\n".format(
            prefix=prefix,
            word="%-5s" % word_str,
            indent=(level * "  "),
            name=cls.__name__,
            description=cls.__doc__ or "",
        )
    return info_str


# ======================= GCode Word Mapping =======================
_gcode_maps_created = False  # only set when the below values are populated
_gcode_word_map = {} # of the form: {Word('G', 0): GCodeRapidMove, ... }
_gcode_function_list = [] # of the form: [(lambda w: w.letter == 'F', GCodeFeedRate), ... ]


def build_maps():
    """Populate _gcode_word_map and _gcode_function_list"""
    # Ensure Word maps / lists are clear
    global _gcode_word_map
    global _gcode_function_list
    _gcode_word_map = {}
    _gcode_function_list = []

    for cls in _subclasses(GCode):
        try:
            if get_default_dialect() not in cls.dialects: continue
        except AttributeError:
            pass
        if cls.word_key is not None:
            # Map Word instance to g-code class
            if cls.word_key in _gcode_word_map:
                raise RuntimeError("Multiple GCode classes map to '%s'" % str(cls.word_key))
            _gcode_word_map[cls.word_key] = cls
        elif cls.word_matches is not None:
            # Add to list of functions
            _gcode_function_list.append((cls.word_matches, cls))

    global _gcode_maps_created
    _gcode_maps_created = True


# ======================= Words -> GCodes =======================
def word_gcode_class(word, exhaustive=False):
    """
    Map word to corresponding GCode class
    :param word: Word instance
    :param exhausitve: if True, all words are tested; not just 'GMFST'
    :return: class inheriting GCode
    """

    if not _gcode_maps_created:
        build_maps()

    # quickly eliminate parameters
    # TODO: get valid world letters from dialect
    if (not exhaustive) and (word.letter not in 'GMFSTNO'):
        return None

    # by Word Map (faster)
    if word in _gcode_word_map:
        return _gcode_word_map[word]

    # by Function List (slower, so checked last)
    for (match_function, gcode_class) in _gcode_function_list:
        if match_function(word):
            return gcode_class

    return None


def words2gcodes(words):
    """
    Group words into GCodes
    :param words: list of :class:`Word <pygcode.words.Word>` instances
    :type words: :class:`list`
    :return: tuple([<GCode>, <GCode>, ...], list(<unused words>))
    :rtype: :class:`tuple`

    Returns a 2-tuple:

    - list of :class:`GCode <pygocde.gcodes.GCode>` instances
    -
    """

    gcodes = []
    # Lines to consider
    # Conflicts with non G|M codes (ie: S|F|T)
    #   Spindle Control:
    #       - S1000
    #       - M3 S2000
    #   Tool Change:
    #       - T2
    #       - M6 T1
    #
    # Conclusion: words are parameters first, gcodes second

    # First determine which words are GCode candidates
    word_info_list = [
        {
            'index': i, # for internal referencing
            'word': word,
            'gcode_class': word_gcode_class(word), # if not None, word is a candidate
            'param_to_index': None,
        }
        for (i, word) in enumerate(words)
    ]

    # Link parameters to candidates
    # note: gcode candidates may be valid parameters... therefore
    # Also eliminate candidates that are parameters for earlier gcode candidates
    for word_info in word_info_list:
        if word_info['gcode_class'] is None:
            continue # not a gcode candidate, so cannot have parameters
        # which of the words following this gcode candidate are a valid parameter
        for param_info in word_info_list[word_info['index'] + 1:]:
            if param_info['word'].letter in word_info['gcode_class'].param_letters:
                param_info['param_to_index'] = word_info['index']
                param_info['gcode_class'] = None # no longer a valid candidate

    # Map parameters
    parameter_map = defaultdict(list) # {<gcode word index>: [<parameter words>], ... }
    for word_info in word_info_list:
        if word_info['gcode_class']:
            continue # will form a gcode, so must not also be a parameter
        parameter_map[word_info['param_to_index']].append(word_info['word'])

    # Create gcode instances
    for word_info in word_info_list:
        if word_info['gcode_class'] is None:
            continue # not a gcode candidate
        gcode = word_info['gcode_class'](
            word_info['word'],
            *parameter_map[word_info['index']] # gcode parameters
        )
        gcodes.append(gcode)

    return (gcodes, parameter_map[None])


def text2gcodes(text):
    """
    Convert text to GCode instances (must be fully formed; no modal parameters)
    :param text: line from a g-code file
    :return: tuple([<GCode>, <GCode>, ...], list(<unused words>))
    """
    words = list(text2words(text))
    (gcodes, modal_words) = words2gcodes(words)
    if modal_words:
        raise GCodeWordStrError("gcode text not fully formed, unassigned parameters: %r" % modal_words)
    return gcodes


# ======================= Utilities =======================

def split_gcodes(gcode_list, splitter_class, sort_list=True):
    """
    Splits a list of GCode instances into 3, the center list containing the splitter_class gcode
    :param gcode_list: list of GCode instances to split
    :type gcode_list: :class:`list`
    :param splitter_class: class of gcode identifying split from left to right
    :type splitter_class: :class:`GCode`
    :param sort_list: if ``False``, gcodes list is not sorted before processing
    :type sort_list: :class:`bool`
    :return: list of: [[<gcodes before splitter>], [<splitter instance>], [<gcodes after splitter>]]
    :rtype: :class:`list`

    Returns a list with 3 elements

    - gcodes before splitter (may be empty)
    - splitter instance (list with a single element)
    - gcodes after splitter (may be empty)

    For example:

    .. doctest::

        >>> from pygcode import Block
        >>> from pygcode.gcodes import split_gcodes, GCodeCoolantOff
        >>> block = Block('G1 X1 Y2 M9 F100 S200')

        >>> (a, b, c) = split_gcodes(block.gcodes, GCodeCoolantOff)
        >>> a
        [<GCodeFeedRate: F100>, <GCodeSpindleSpeed: S200>]
        >>> b
        [<GCodeCoolantOff: M09>]
        >>> c
        [<GCodeLinearMove: G01{X1, Y2}>]

        >>> # Line with the M09 code removed
        >>> a + c
        [<GCodeFeedRate: F100>, <GCodeSpindleSpeed: S200>, <GCodeLinearMove: G01{X1, Y2}>]

    .. note::

        The above example is sorted in execution order by default, set
        ``sort_list=False`` to override this behaviour.

    """
    # for example:
    #     g_list = sorted([g1, g2, g3, g4])
    #     split_gcodes(g_list, type(g2)) == [[g1], [g2], [g3, g4]]
    # 3 lists are always returned, even if empty; if 2nd list is empty,
    # then the 3rd will be as well.
    if sort_list: # sort by execution order first
        gcode_list = sorted(gcode_list)

    split = [gcode_list, [], []]  # default (if no splitter can be found)

    # Find splitter index (only one can be found)
    split_index = None
    for (i, gcode) in enumerate(gcode_list):
        if isinstance(gcode, splitter_class):
            split_index = i
            break

    # Form split: pivoting around split_index
    if split_index is not None:
        split[0] = gcode_list[:split_index]
        split[1] = [gcode_list[split_index]]
        split[2] = gcode_list[split_index+1:]

    return split


def _gcodes_abs2rel(start_pos, dist_mode=None, axes='XYZ'):
    """
    Decorator to convert returned motion gcode coordinates to incremental.
    Intended to be used internally (mainly because it's a little shonky).
    Function being decorated is only expected to return GCodeRapidMove or
    GCodeLinearMove instances.
    :param start_pos: starting machine position (Position)
    :param dist_mode: machine's distance mode (GCodeAbsoluteDistanceMode or GCodeIncrementalDistanceMode)
    :param axes: axes machine accepts (set)
    """
    # Usage:
    #   m = Machine()  # defaults to absolute distance mode
    #   m.process_gcodes(GCodeRapidMove(X=10, Y=20, Z=3))
    #   m.process_gcodes(GCodeIncrementalDistanceMode())
    #
    #   @_gcodes_abs2rel(start_pos=m.pos, dist_mode=m.mode.distance, axes=m.axes)
    #   def do_stuff():
    #       yield GCodeRapidMove(X=0, Y=30, Z=3)
    #       yield GCodeLinearMove(X=0, Y=30, Z=-5)
    #
    #   gcode_list = do_stuff()
    #   gocde_list[0] # == GCodeRapidMove(X=-10, Y=10)
    #   gocde_list[1] # == GCodeLinearMove(Z=-8)

    SUPPORTED_MOTIONS = (
        GCodeRapidMove, GCodeLinearMove,
    )

    def wrapper(func):

        def inner(*largs, **kwargs):
            # Create Machine (with minimal information)
            from .machine import Machine, Mode, Position
            m = type('AbsoluteCoordMachine', (Machine,), {
                'MODE_CLASS': type('NullMode', (Mode,), {'default_mode': 'G90'}),
                'axes': axes,
            })()
            m.pos = start_pos

            for gcode in func(*largs, **kwargs):
                # Verification & passthrough's
                if not isinstance(gcode, GCode):
                    yield gcode  # whatever this thing is
                else:
                    # Process gcode
                    pos_from = m.pos
                    m.process_gcodes(gcode)
                    pos_to = m.pos

                    if gcode.modal_group != MODAL_GROUP_MAP['motion']:
                        yield gcode  # only deal with motion gcodes
                        continue
                    elif not isinstance(gcode, SUPPORTED_MOTIONS):
                        raise NotImplementedError("%r to iterative coords is not supported (this is only a very simple function)" % gcode)

                    # Convert coordinates to iterative
                    rel_pos = pos_to - pos_from
                    coord_words = [w for w in rel_pos.words if w.value]
                    if coord_words:  # else relative coords are all zero; do nothing
                        yield words2gcodes([gcode.word] + coord_words)[0].pop()


        # Return apropriate function
        if (dist_mode is None) or isinstance(dist_mode, GCodeIncrementalDistanceMode):
            return inner
        else:
            return func  # bypass decorator entirely; nothing to be done
    return wrapper
