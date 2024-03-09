from .gcodes import MODAL_GROUP_MAP
from .words import Word, text2words
import six

"""
    These class types can be used by external programs to classify the type of instructions
    see class comments and marlin_gcode.py for examples.

    The granularity of the class naming, while it has no functional use while parsing, can however
    be useful when it will come to translating from one dialect to another.

    When unsure what class a command should be a (semantic) subclass off, we try to keeps together
    things that are related to each other (ie. SD card stuff)
"""

class GCode(object):
    """ base gcode class ; prefer not to use it """
    # Defining Word
    word_key = None # Word instance to use in lookup
    word_matches = None # function (secondary)
    default_word = None
    word_letter = 'G'
    word_value_configurable = False  # if set, word value can be the first parameter

    # Parameters associated to this gcode
    param_letters = set()

    # Modal stuff
    modal_group = None
    modal_param_letters = set() # by default: no parameters are retained in modal state

    # Execution Order
    exec_order = 999  # if not otherwise specified, run last

    def __init__(self, *words, **params):
        """
        :param word: Word instance defining gcode (eg: Word('G0') for rapid movement)
        :param params: list of Word instances (eg: Word('X-1.2') as x-coordinate)
        """
        gcode_word_list = words[:1]
        param_words = words[1:]
        if gcode_word_list:
            gcode_word = gcode_word_list[0]
            if self.word_value_configurable and isinstance(gcode_word, six.integer_types + (float,)):
                gcode_word = Word(self.word_letter, gcode_word)  # cast to Word()
        else:
            gcode_word = self._default_word()
        assert isinstance(gcode_word, Word), "invalid gcode word %r" % gcode_word
        self.word = gcode_word
        self.params = {}

        # Whitespace as prefix
        #   if True, str(self) will repalce self.word code with whitespace
        self._whitespace_prefix = False

        # Add Given Parameters
        for param_word in param_words:
            self.add_parameter(param_word)
        for (k, v) in params.items():
            self.add_parameter(Word(k, v))

    def __repr__(self):
        param_str = ''
        if self.params:
            param_str = "{%s}" % (', '.join([
                "{}".format(self.params[k])
                for k in sorted(self.params.keys())
            ]))
        return "<{class_name}: {gcode}{params}>".format(
            class_name=self.__class__.__name__,
            gcode=self.word,
            params=param_str,
        )

    def __str__(self):
        """String representation of gcode, as it would be seen in a .gcode file"""
        param_str = ''
        if self.params:
            param_str += ' ' + ' '.join([
                "{}".format(self.params[k])
                for k in sorted(self.params.keys())
            ])
        word_str = str(self.word)
        if self._whitespace_prefix:
            word_str = ' ' * len(word_str)
        return "{word_str}{parameters}".format(
            word_str=word_str,
            parameters=param_str,
        )
    
    def __hash__(self):
        """Hash representation of the gcode, for set and dictionary usage"""
        try:
            return hash(self.word_key)
        except TypeError:
            return hash(self.word_letter) # May also want to retrieve additional value info
        

    def _default_word(self):
        if self.default_word:
            return copy(self.default_word)
        elif self.word_key:
            return copy(self.word_key)
        raise AssertionError("class %r has no default word" % self.__class__)

    # Equality
    def __eq__(self, other):
        return (
            (self.word == other.word) and
            (self.params == other.params)
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    # Sort by execution order
    def __lt__(self, other):
        return self.exec_order < other.exec_order

    def __le__(self, other):
        return self.exec_order <= other.exec_order

    def __gt__(self, other):
        return self.exec_order > other.exec_order

    def __ge__(self, other):
        return self.exec_order >= other.exec_order

    # Parameters
    def add_parameter(self, word):
        """
        Add given word as a parameter for this gcode
        :param word: Word instance
        """
        assert isinstance(word, Word), "invalid parameter class: %r" % word
        if word.letter not in self.param_letters:
            raise GCodeParameterError("invalid parameter for %s: %s" % (self.__class__.__name__, str(word)))
        if word.letter in self.params:
            raise GCodeParameterError("parameter defined twice: %s -> %s" % (self.params[word.letter], word))

        self.params[word.letter] = word

    # Assert Parameters
    def assert_params(self):
        """
        Assert validity of gcode's parameters.
        This verification is irrespective of machine, or machine's state;
        verification is g-code language-based verification
        :raises: GCodeParameterError
        """
        # to be overridden in inheriting classes
        pass

    def __getattr__(self, key):
        # Return parameter values (if valid parameter for gcode)
        if key in self.param_letters:
            if key in self.params:
                return self.params[key].value
            else:
                return None # parameter is valid for GCode, but undefined

        raise AttributeError("'{cls}' object has no attribute '{key}'".format(
            cls=self.__class__.__name__,
            key=key
        ))

    def __setattr__(self, key, value):
        if key in self.param_letters:
            if key in self.params:
                self.params[key].value = value
            else:
                self.add_parameter(Word(key, value))

        else:
            self.__dict__[key] = value

    @property
    def description(self):
        return self.__doc__

    def modal_copy(self):
        """Copy of GCode instance containing only parameters listed in modal_param_letters"""
        return self.__class__(self.word, *[
            w for (l, w) in self.params.items()
            if l in self.modal_param_letters
        ])

    def get_param_dict(self, letters=None, lc=False):
        """
        Get gcode parameters as a dict
        gcode parameter like "X3.1, Y-2" would return {'X': 3.1, 'Y': -2}
        :param letters: iterable whitelist of letters to include as dict keys
        :param lc: lower case parameter letters
        :return: dict of gcode parameters' (letter, value) pairs
        """
        letter_mod = lambda x: x
        if lc:
            letter_mod = lambda x: x.lower()
        return dict(
            (letter_mod(w.letter), w.value) for w in self.params.values()
            if (letters is None) or (w.letter in letters)
        )

    # Process GCode
    def process(self, machine):
        """
        Process a GCode on the given Machine
        :param machine: Machine instance, to change state
        :return: GCodeEffect instance; effect the gcode just had on machine
        """
        from .machine import Machine  # importing up (done live to avoid dependency loop)
        assert isinstance(machine, Machine), "invalid machine type: %r" % machine

        # Set mode
        self._process_mode(machine)

        # GCode specific
        self._process(machine)

    def _process_mode(self, machine):
        """Set machine's state"""
        machine.set_mode(self)

    def _process(self, machine):
        """Process this GCode (to be overridden)"""
        pass


# ======================= Non Operational =======================
# CODE          PARAMETERS      DESCRIPTION
# N#                            Define line number (oldschool)
# O<name>                       Define program name

class GCodeDefinition(GCode):
    pass


class GCodeLineNumber(GCodeDefinition):
    """N: Line Number"""
    word_letter = 'N'
    word_value_configurable = True
    exec_order = 0

    @classmethod
    def word_matches(cls, w):
        return w.letter == 'N'

    @property
    def number(self):
        return self.word.value


class GCodeProgramName(GCodeDefinition):
    """O: Program Name"""
    word_letter = 'O'
    word_value_configurable = True
    exec_order = 1

    @classmethod
    def word_matches(cls, w):
        return w.letter == 'O'

    @property
    def name(self):
        return self.word.value


# ======================= Motion =======================
class GCodeMotion(GCode):
    """ any command that will move the machine and has XYZ... parameters attached
        ie. the host is able to kow the machine position after such a command """
    param_letters = set('XYZABCUVW')
    modal_group = MODAL_GROUP_MAP['motion']
    exec_order = 242

    def _process(self, machine):
        machine.move_to(**self.get_param_dict(letters=machine.axes))


class GCodeArcMove(GCodeMotion):
    """Arc Move"""
    param_letters = GCodeMotion.param_letters | set('IJKRP')

    def assert_params(self):
        param_letters = set(self.params.keys())
        # Parameter groups
        params_xyz = set('XYZ') & set(param_letters)
        params_ijk = set('IJK') & set(param_letters)
        params_r = set('R') & set(param_letters)
        params_ijkr = params_ijk | params_r

        # --- Parameter Groups
        # XYZ: at least 1
        if not params_xyz:
            raise GCodeParameterError("no XYZ parameters set for destination: %r" % arc_gcode)
        # IJK or R: only in 1 group
        if params_ijk and params_r:
            raise GCodeParameterError("both IJK and R parameters defined: %r" % arc_gcode)
        # IJKR: at least 1
        if not params_ijkr:
            raise GCodeParameterError("neither IJK or R parameters defined: %r" % arc_gcode)

        # --- Parameter Values
        if params_r and (self.R == 0):
            raise GCodeParameterError("cannot plot a circle with a radius of zero: %r" % arc_gcode)

# ======================= Canned Cycles =======================
class GCodeCannedCycle(GCode):
    param_letters = set('XYZUVW')
    modal_group = MODAL_GROUP_MAP['canned_cycle']
    exec_order = 242

    def _process(self, machine):
        moveto_coords = self.get_param_dict(letters=machine.axes)
        if isinstance(machine.mode.canned_cycles_return, GCodeCannedCycleReturnToR):
            # canned return is to this.R, not this.Z (plane dependent)
            moveto_coords.update({
                machine.mode.plane_selection.normal_axis: self.R,
            })
        else:  # default: GCodeCannedCycleReturnPrevLevel
            # Remove this.Z (plane dependent) value (ie: no machine movement on this axis)
            moveto_coords.pop(machine.mode.plane_selection.normal_axis, None)

        # Process action 'L' times
        if hasattr(self, 'L'):
            loop_count = self.L
            if (loop_count is None) or (loop_count <= 0):
                loop_count = 1
            for i in range(loop_count):
                machine.move_to(**moveto_coords)


# ======================= Return Mode in Canned Cycles =======================
class GCodeCannedReturnMode(GCode):
    modal_group = MODAL_GROUP_MAP['canned_cycles_return']
    exec_order = 220


# ======================= Distance Mode =======================
class GCodeDistanceMode(GCode):
    """ for points of reference to use, and things such as working by radius or diameter (somewhat modal) """
    exec_order = 210


# ======================= Feed Rate Mode =======================
class GCodeFeedRateMode(GCode):
    """ how feedrates will be interpreted """
    modal_group = MODAL_GROUP_MAP['feed_rate_mode']
    exec_order = 30


# ======================= Spindle/Tool Control =======================
class GCodeToolState(GCode):
    word_letter = 'M'
    exec_order = 90


# ======================= Coolant & Heaters =======================
class GCodeCoolantHeaters(GCode):
    """ all cooling, heating and ventilation systems EXCEPT nozzle temperatures (see GCodeToolState) """
    word_letter = 'M'
    modal_group = MODAL_GROUP_MAP['coolant']
    exec_order = 110


# ======================= Tool Geometry =======================
class GCodeToolGeometry(GCode):
    """ tool lengths and offsets """
    modal_group = MODAL_GROUP_MAP['tool_length_offset']
    exec_order = 180


# ======================= Stopping (Program Control) =======================
class GCodeProgramControl(GCode):
    word_letter = 'M'
    modal_group = MODAL_GROUP_MAP['stopping']
    exec_order = 250

# ======================= Units =======================
class GCodeUnit(GCode):
    """ selects a unit system (somewhat modal) """
    modal_group = MODAL_GROUP_MAP['units']
    exec_order = 160

# ======================= Plane Selection =======================
class GCodePlaneSelect(GCode):
    modal_group = MODAL_GROUP_MAP['plane_selection']
    exec_order = 150

    # -- Plane Orientation Quaternion
    # Such that...
    #   vectorXY = Vector3(<your coords in X/Y plane>)
    #   vectorZX = GCodeSelectZXPlane.quat * vectorXY
    #   vectorZX += some_offset_vector
    #   vectorXY = GCodeSelectZXPlane.quat.conjugate() * vectorZX
    # note: all quaternions use the XY plane as a basis
    # To transform from ZX to YZ planes via these quaternions, you must
    # first translate it to XY, like so:
    #   vectorYZ = GCodeSelectYZPlane.quat * (GCodeSelectZXPlane.quat.conjugate() * vectorZX)
    quat = None  # Quaternion

    # -- Plane Axis Information
    # Vector normal to plane (such that XYZ axes follow the right-hand rule)
    normal_axis = None  # Letter of normal axis (upper case)
    # Axes of plane
    plane_axes = set()
    normal = None  # Vector3

# ======================= Cutter Radius Compensation =======================
class GCodeCutterRadiusComp(GCodeToolGeometry):
    modal_group = MODAL_GROUP_MAP['cutter_diameter_comp']
    exec_order = 170

# ======================= Path Control Mode =======================
class GCodePathControlMode(GCode):
    """ codes that will affect the path and motion either by allowing greater deviation
    from the theoretical path or by inducing greater deviation (includes acceleration and jerk)"""
    modal_group = MODAL_GROUP_MAP['control_mode']
    exec_order = 200

# ======================= Other Modal Codes =======================
class GCodeOtherModal(GCode):
    pass


class GCodeSelectCoordinateSystem(GCodeOtherModal):
    """Select Coordinate System"""
    modal_group = MODAL_GROUP_MAP['coordinate_system']
    exec_order = 190
    coord_system_id = None  # overridden in inheriting classes


# ======================= Flow-control Codes =======================
class GCodeIO(GCode):
    """ pretty much anything that reads and writes on digital pins and not related to motion and temperatures """
    word_letter = 'M'
    exec_order = 70


class GCodeDigitalOutput(GCodeIO):
    """Digital Output Control"""
    param_letters = set('P')


# ======================= Non-modal Codes =======================
class GCodeNonModal(GCode):
    pass


# ======================= Machine Configuration and Calibration Codes =======================
class GCodeMachineRoutines(GCode):
    """ standard routines that WILL induce movement such as homing, tool changes.. """

class GCodeAssistedRoutines(GCodeMachineRoutines):
    """ machine routines that require user intervention """

class GCodeCalibrationRoutines(GCode):
    """ machine routines that are used for calibration purposes """

class GCodeMachineConfig(GCode):
    """ configuration parameters that will not significantly alter the machine behaviour """

class GCodeMachineState(GCode):
    """ mostly for commands that report the machine state to the host """
