from .gcodes_base import *
from .gcodes import DIALECT_UNKNOWN
from .utils import Vector3, Quaternion, quat2coord_system

# ======================= Motion =======================
#   (X Y Z A B C U V W apply to all motions)
# CODE          PARAMETERS      DESCRIPTION
# G0                            Rapid Move
# G1                            Linear Move
# G2, G3        I J K or R, P   Arc Move
# G4            P               Dwell
# G5            I J P Q         Cubic Spline
# G5.1          I J             Quadratic Spline
# G5.2          P L             NURBS
# G10                           Retract
# G11                           Recover
# G38.2 - G38.5                 Straight Probe
# G33           K               Spindle Synchronized Motion
# G33.1         K               Rigid Tapping

class GCodeRapidMove(GCodeMotion):
    """G0: Rapid Move"""
    word_key = Word('G', 0)

    def _process(self, machine):
        machine.move_to(rapid=True, **self.get_param_dict(letters=machine.axes))


class GCodeLinearMove(GCodeMotion):
    """G1: Linear Move"""
    word_key = Word('G', 1)



class GCodeArcMoveCW(GCodeArcMove):
    """G2: Arc Move (clockwise)"""
    word_key = Word('G', 2)


class GCodeArcMoveCCW(GCodeArcMove):
    """G3: Arc Move (counter-clockwise)"""
    word_key = Word('G', 3)


class GCodeDwell(GCodeMotion):
    """G4: Dwell"""
    param_letters = set('P')  # doesn't accept axis parameters
    word_key = Word('G', 4)
    modal_group = None  # one of the few motion commands that isn't modal
    exec_order = 140

    def _process(self, machine):
        pass  # no movements made


class GCodeCublcSpline(GCodeMotion):
    """G5: Cubic Spline"""
    param_letters = GCodeMotion.param_letters | set('IJPQ')
    word_key = Word('G', 5)


class GCodeQuadraticSpline(GCodeMotion):
    """G5.1: Quadratic Spline"""
    param_letters = GCodeMotion.param_letters | set('IJ')
    word_key = Word('G', 5.1)


class GCodeNURBS(GCodeMotion):
    """G5.2: Non-uniform rational basis spline (NURBS)"""
    param_letters = GCodeMotion.param_letters | set('PL')
    word_key = Word('G', 5.2)


class GCodeNURBSEnd(GCodeNURBS):
    """G5.3: end NURBS mode"""
    word_key = Word('G', 5.3)

class GCodeStraightProbe(GCodeMotion):
    """G38.2-G38.5: Straight Probe"""
    @classmethod
    def word_matches(cls, w):
        return (w.letter == 'G') and (38.2 <= w.value <= 38.5)
    default_word = Word('G', 38.2)


class GCodeSpindleSyncMotion(GCodeMotion):
    """G33: Spindle Synchronized Motion"""
    param_letters = GCodeMotion.param_letters | set('K')
    word_key = Word('G', 33)


class GCodeRigidTapping(GCodeMotion):
    """G33.1: Rigid Tapping"""
    param_letters = GCodeMotion.param_letters | set('K')
    word_key = Word('G', 33.1)


# ======================= Canned Cycles =======================
#      (X Y Z or U V W apply to canned cycles, depending on active plane)
# CODE              PARAMETERS          DESCRIPTION
# G81               R L (P)             Drilling Cycle
# G82               R L (P)             Drilling Cycle, Dwell
# G83               R L Q               Drilling Cycle, Peck
# G73               R L Q               Drilling Cycle, Chip Breaking
# G85               R L (P)             Boring Cycle, Feed Out
# G89               R L (P)             Boring Cycle, Dwell, Feed Out
# G76               P Z I J R K Q H L E Threading Cycle
# G80                                   Cancel Canned Cycle

class GCodeDrillingCycle(GCodeCannedCycle):
    """G81: Drilling Cycle"""
    param_letters = GCodeCannedCycle.param_letters | set('RLP')
    word_key = Word('G', 81)
    modal_param_letters = GCodeCannedCycle.param_letters | set('RP')


class GCodeDrillingCycleDwell(GCodeCannedCycle):
    """G82: Drilling Cycle, Dwell"""
    param_letters = GCodeCannedCycle.param_letters | set('RLP')
    word_key = Word('G', 82)
    modal_param_letters = GCodeCannedCycle.param_letters | set('RP')


class GCodeDrillingCyclePeck(GCodeCannedCycle):
    """G83: Drilling Cycle, Peck"""
    param_letters = GCodeCannedCycle.param_letters | set('RLQ') | set('IJK')
    word_key = Word('G', 83)
    modal_param_letters = GCodeCannedCycle.param_letters | set('RQ')


class GCodeDrillingCycleChipBreaking(GCodeCannedCycle):
    """G73: Drilling Cycle, ChipBreaking"""
    param_letters = GCodeCannedCycle.param_letters | set('RLQ')
    word_key = Word('G', 73)
    modal_param_letters = GCodeCannedCycle.param_letters | set('RQ')


class GCodeBoringCycleFeedOut(GCodeCannedCycle):
    """G85: Boring Cycle, Feed Out"""
    param_letters = GCodeCannedCycle.param_letters | set('RLP')
    word_key = Word('G', 85)
    modal_param_letters = GCodeCannedCycle.param_letters | set('RP')


class GCodeBoringCycleDwellFeedOut(GCodeCannedCycle):
    """G89: Boring Cycle, Dwell, Feed Out"""
    param_letters = GCodeCannedCycle.param_letters | set('RLP')
    word_key = Word('G', 89)
    modal_param_letters = GCodeCannedCycle.param_letters | set('RP')


class GCodeThreadingCycle(GCodeCannedCycle):
    """G76: Threading Cycle"""
    param_letters = GCodeCannedCycle.param_letters | set('PZIJRKQHLE')
    word_key = Word('G', 76)

class GCodeCancelCannedCycle(GCodeCannedCycle):
    """ G80: Cancel Canned Cycle """
    dialects = DIALECT_UNKNOWN
    param_letters = set()
    word_key = Word('G', 80)
    # Modal Group
    #   Technically G80 belongs to the motion modal group, however it's often
    #   expressed in the same line as another motion command.
    #   This is alowed, but executed just prior to any other motion command
    #       eg: G00 G80
    #   will leave the machine in rapid motion mode
    #   Just running G80 will leave machine with no motion mode.
    exec_order = 241


# ======================= Distance Mode =======================
# CODE              PARAMETERS          DESCRIPTION
# G90, G91                              Distance Mode
# G90.1, G91.1                          Arc Distance Mode
# G7                                    Lathe Diameter Mode
# G8                                    Lathe Radius Mode

class GCodeAbsoluteDistanceMode(GCodeDistanceMode):
    """G90: Absolute Distance Mode"""
    word_key = Word('G', 90)
    modal_group = MODAL_GROUP_MAP['distance']


class GCodeIncrementalDistanceMode(GCodeDistanceMode):
    """G91: Incremental Distance Mode"""
    word_key = Word('G', 91)
    modal_group = MODAL_GROUP_MAP['distance']


class GCodeAbsoluteArcDistanceMode(GCodeDistanceMode):
    """G90.1: Absolute Distance Mode for Arc IJK Parameters"""
    word_key = Word('G', 90.1)
    modal_group = MODAL_GROUP_MAP['arc_ijk_distance']


class GCodeIncrementalArcDistanceMode(GCodeDistanceMode):
    """G91.1: Incremental Distance Mode for Arc IJK Parameters"""
    word_key = Word('G', 91.1)
    modal_group = MODAL_GROUP_MAP['arc_ijk_distance']


class GCodeLatheDiameterMode(GCodeDistanceMode):
    """G7: Lathe Diameter Mode"""
    word_key = Word('G', 7)
    modal_group = MODAL_GROUP_MAP['lathe_diameter']


class GCodeLatheRadiusMode(GCodeDistanceMode):
    """G8: Lathe Radius Mode"""
    word_key = Word('G', 8)
    modal_group = MODAL_GROUP_MAP['lathe_diameter']


# ======================= Feed Rate Mode =======================
# CODE              PARAMETERS          DESCRIPTION
# G93, G94, G95                         Feed Rate Mode

class GCodeInverseTimeMode(GCodeFeedRateMode):
    """G93: Inverse Time Mode"""
    word_key = Word('G', 93)


class GCodeUnitsPerMinuteMode(GCodeFeedRateMode):
    """G94: Units Per MinuteMode"""
    word_key = Word('G', 94)


class GCodeUnitsPerRevolution(GCodeFeedRateMode):
    """G95: Units Per Revolution"""
    word_key = Word('G', 95)


# ======================= Spindle Control =======================
# CODE              PARAMETERS          DESCRIPTION
# M3, M4, M5        S                   Spindle Control
# M19                                   Orient Spindle
# G96, G97          S D                 Spindle Control Mode

class GCodeStartSpindle(GCodeSpindle):
    """M3,M4: Start Spindle Clockwise"""
    modal_group = MODAL_GROUP_MAP['spindle']


class GCodeStartSpindleCW(GCodeStartSpindle):
    """M3: Start Spindle Clockwise"""
    #param_letters = set('S')  # S is it's own gcode, makes no sense to be here
    word_key = Word('M', 3)

class GCodeStartSpindleCCW(GCodeStartSpindle):
    """M4: Start Spindle Counter-Clockwise"""
    #param_letters = set('S')  # S is it's own gcode, makes no sense to be here
    word_key = Word('M', 4)


class GCodeStopSpindle(GCodeSpindle):
    """M5: Stop Spindle"""
    #param_letters = set('S')  # S is it's own gcode, makes no sense to be here
    word_key = Word('M', 5)
    modal_group = MODAL_GROUP_MAP['spindle']


class GCodeOrientSpindle(GCodeSpindle):
    """M19: Orient Spindle"""
    word_key = Word('M', 19)


class GCodeSpindleSpeedMode(GCodeSpindle):
    word_letter = 'G'
    modal_group = MODAL_GROUP_MAP['spindle_speed_mode']


class GCodeSpindleConstantSurfaceSpeedMode(GCodeSpindleSpeedMode):
    """G96: Spindle Constant Surface Speed"""
    param_letters = set('DS')
    word_key = Word('G', 96)


class GCodeSpindleRPMMode(GCodeSpindleSpeedMode):
    """G97: Spindle RPM Speed"""
    param_letters = set('D')
    word_key = Word('G', 97)



# ======================= Coolant =======================
# CODE              PARAMETERS          DESCRIPTION
# M7, M8, M9                            Coolant Control

class GCodeCoolantMistOn(GCodeCoolant):
    """M7: turn mist coolant on"""
    word_key = Word('M', 7)


class GCodeCoolantFloodOn(GCodeCoolant):
    """M8: turn flood coolant on"""
    word_key = Word('M', 8)


class GCodeCoolantOff(GCodeCoolant):
    """M9: turn all coolant off"""
    word_key = Word('M', 9)


# ======================= Tool Length =======================
# CODE              PARAMETERS          DESCRIPTION
# G43               H                   Tool Length Offset
# G43.1                                 Dynamic Tool Length Offset
# G43.2             H                   Apply additional Tool Length Offset
# G49                                   Cancel Tool Length Compensation

class GCodeToolLengthOffset(GCodeToolLength):
    """G43: Tool Length Offset"""
    param_letters = set('H')
    word_key = Word('G', 43)


class GCodeDynamicToolLengthOffset(GCodeToolLength):
    """G43.1: Dynamic Tool Length Offset"""
    word_key = Word('G', 43.1)


class GCodeAddToolLengthOffset(GCodeToolLength):
    """G43.2: Appkly Additional Tool Length Offset"""
    param_letters = set('H')
    word_key = Word('G', 43.2)


class GCodeCancelToolLengthOffset(GCodeToolLength):
    """G49: Cancel Tool Length Compensation"""
    word_key = Word('G', 49)


# ======================= Stopping (Program Control) =======================
# CODE              PARAMETERS          DESCRIPTION
# M0, M1                                Program Pause
# M2, M30                               Program End
# M60                                   Pallet Change Pause

class GCodePauseProgram(GCodeProgramControl):
    """M0: Program Pause"""
    word_key = Word('M', 0)


class GCodePauseProgramOptional(GCodeProgramControl):
    """M1: Program Pause (optional)"""
    word_key = Word('M', 1)


class GCodeEndProgram(GCodeProgramControl):
    """M2: Program End"""
    word_key = Word('M', 2)


class GCodeEndProgramPalletShuttle(GCodeProgramControl):
    """M30: exchange pallet shuttles and end the program"""
    word_key = Word('M', 30)


class GCodePalletChangePause(GCodeProgramControl):
    """M60: Pallet Change Pause"""
    word_key = Word('M', 60)


# ======================= Units =======================
# CODE              PARAMETERS          DESCRIPTION
# G20, G21                              Units

class GCodeUseInches(GCodeUnit):
    """G20: use inches for length units"""
    word_key = Word('G', 20)
    unit_id = 0


class GCodeUseMillimeters(GCodeUnit):
    """G21: use millimeters for length units"""
    word_key = Word('G', 21)
    unit_id = 1


# ======================= Plane Selection =======================
#       (affects G2, G3, G81-G89, G40-G42)
# CODE              PARAMETERS          DESCRIPTION
# G17 - G19.1                           Plane Select

class GCodeSelectXYPlane(GCodePlaneSelect):
    """G17: select XY plane (default)"""
    word_key = Word('G', 17)
    quat = Quaternion()  # no effect
    normal_axis = 'Z'
    plane_axes = set('XY')
    normal = Vector3(0., 0., 1.)


class GCodeSelectZXPlane(GCodePlaneSelect):
    """G18: select ZX plane"""
    word_key = Word('G', 18)
    quat = quat2coord_system(
        Vector3(1., 0., 0.), Vector3(0., 1., 0.),
        Vector3(0., 0., 1.), Vector3(1., 0., 0.)
    )
    normal_axis = 'Y'
    plane_axes = set('ZX')
    normal = Vector3(0., 1., 0.)


class GCodeSelectYZPlane(GCodePlaneSelect):
    """G19: select YZ plane"""
    word_key = Word('G', 19)
    quat = quat2coord_system(
        Vector3(1., 0., 0.), Vector3(0., 1., 0.),
        Vector3(0., 1., 0.), Vector3(0., 0., 1.)
    )
    normal_axis = 'X'
    plane_axes = set('YZ')
    normal = Vector3(1., 0., 0.)


class GCodeSelectUVPlane(GCodePlaneSelect):
    """G17.1: select UV plane"""
    word_key = Word('G', 17.1)


class GCodeSelectWUPlane(GCodePlaneSelect):
    """G18.1: select WU plane"""
    word_key = Word('G', 18.1)


class GCodeSelectVWPlane(GCodePlaneSelect):
    """G19.1: select VW plane"""
    word_key = Word('G', 19.1)


# ======================= Cutter Radius Compensation =======================
# CODE              PARAMETERS          DESCRIPTION
# G40                                   Compensation Off
# G41,G42           D                   Cutter Compensation
# G41.1, G42.1      D L                 Dynamic Cutter Compensation

class GCodeCutterRadiusCompOff(GCodeCutterRadiusComp):
    """G40: Cutter Radius Compensation Off"""
    word_key = Word('G', 40)


class GCodeCutterCompLeft(GCodeCutterRadiusComp):
    """G41: Cutter Radius Compensation (left)"""
    param_letters = set('D')
    word_key = Word('G', 41)


class GCodeCutterCompRight(GCodeCutterRadiusComp):
    """G42: Cutter Radius Compensation (right)"""
    param_letters = set('D')
    word_key = Word('G', 42)


class GCodeDynamicCutterCompLeft(GCodeCutterRadiusComp):
    """G41.1: Dynamic Cutter Radius Compensation (left)"""
    param_letters = set('DL')
    word_key = Word('G', 41.1)


class GCodeDynamicCutterCompRight(GCodeCutterRadiusComp):
    """G42.1: Dynamic Cutter Radius Compensation (right)"""
    param_letters = set('DL')
    word_key = Word('G', 42.1)

# ======================= Path Control Mode =======================
# CODE              PARAMETERS          DESCRIPTION
# G61 G61.1                             Exact Path Mode
# G64               P Q                 Path Blending


class GCodeExactPathMode(GCodePathControlMode):
    """G61: Exact path mode"""
    word_key = Word('G', 61)


class GCodeExactStopMode(GCodePathControlMode):
    """G61.1: Exact stop mode"""
    word_key = Word('G', 61.1)


class GCodePathBlendingMode(GCodePathControlMode):
    """G64: Path Blending"""
    param_letters = set('PQ')
    word_key = Word('G', 64)


# ======================= Return Mode in Canned Cycles =======================
# CODE              PARAMETERS          DESCRIPTION
# G98                                   Canned Cycle Return Level to previous
# G99                                   Canned Cycle Return to the level set by R

class GCodeCannedCycleReturnPrevLevel(GCodeCannedReturnMode):
    """G98: Canned Cycle Return to the level set prior to cycle start"""
    # "retract to the position that axis was in just before this series of one or more contiguous canned cycles was started"
    word_key = Word('G', 98)


class GCodeCannedCycleReturnToR(GCodeCannedReturnMode):
    """G99: Canned Cycle Return to the level set by R"""
    # "retract to the position specified by the R word of the canned cycle"
    word_key = Word('G', 99)


# ======================= Other Modal Codes =======================
# CODE              PARAMETERS          DESCRIPTION
# F                                     Set Feed Rate
# S                                     Set Spindle Speed
# T                                     Select Tool
# M48, M49                              Speed and Feed Override Control
# M50               P0 (off) or P1 (on) Feed Override Control
# M51               P0 (off) or P1 (on) Spindle Speed Override Control
# M52               P0 (off) or P1 (on) Adaptive Feed Control
# M53               P0 (off) or P1 (on) Feed Stop Control
# G54-G59.3                             Select Coordinate System

class GCodeFeedRate(GCodeOtherModal):
    """F: Set Feed Rate"""
    word_letter = 'F'
    word_value_configurable = True
    @classmethod
    def word_matches(cls, w):
        return w.letter == 'F'
    default_word = Word('F', 0)
    modal_group = MODAL_GROUP_MAP['feed_rate']
    exec_order = 40


class GCodeSpindleSpeed(GCodeOtherModal):
    """S: Set Spindle Speed"""
    word_letter = 'S'
    word_value_configurable = True
    @classmethod
    def word_matches(cls, w):
        return w.letter == 'S'
    default_word = Word('S', 0)
    # Modal Group: (see description in GCodeFeedRate)
    modal_group = MODAL_GROUP_MAP['spindle_speed']
    exec_order = 50


class GCodeSelectTool(GCodeOtherModal):
    """T: Select Tool"""
    word_letter = 'T'
    word_value_configurable = True
    @classmethod
    def word_matches(cls, w):
        return w.letter == 'T'
    default_word = Word('T', 0)
    # Modal Group: (see description in GCodeFeedRate)
    modal_group = MODAL_GROUP_MAP['tool']
    exec_order = 60


class GCodeSpeedAndFeedOverrideOn(GCodeOtherModal):
    """M48: Speed and Feed Override Control On"""
    word_letter = 'M'
    word_key = Word('M', 48)
    modal_group = MODAL_GROUP_MAP['override_switches']
    exec_order = 120


class GCodeSpeedAndFeedOverrideOff(GCodeOtherModal):
    """M49: Speed and Feed Override Control Off"""
    word_letter = 'M'
    word_key = Word('M', 49)
    modal_group = MODAL_GROUP_MAP['override_switches']
    exec_order = 120


class GCodeFeedOverride(GCodeOtherModal):
    """M50: Feed Override Control"""
    word_letter = 'M'
    param_letters = set('P')
    word_key = Word('M', 50)
    exec_order = 120


class GCodeSpindleSpeedOverride(GCodeOtherModal):
    """M51: Spindle Speed Override Control"""
    word_letter = 'M'
    param_letters = set('P')
    word_key = Word('M', 51)
    exec_order = 120


class GCodeAdaptiveFeed(GCodeOtherModal):
    """M52: Adaptive Feed Control"""
    word_letter = 'M'
    param_letters = set('P')
    word_key = Word('M', 52)
    exec_order = 120


class GCodeFeedStop(GCodeOtherModal):
    """M53: Feed Stop Control"""
    word_letter = 'M'
    param_letters = set('P')
    word_key = Word('M', 53)
    exec_order = 120


class GCodeSelectCoordinateSystem1(GCodeSelectCoordinateSystem):
    """Select Coordinate System 1"""
    word_key = Word('G', 54)
    coord_system_id = 1


class GCodeSelectCoordinateSystem2(GCodeSelectCoordinateSystem):
    """Select Coordinate System 2"""
    word_key = Word('G', 55)
    coord_system_id = 2


class GCodeSelectCoordinateSystem3(GCodeSelectCoordinateSystem):
    """Select Coordinate System 3"""
    word_key = Word('G', 56)
    coord_system_id = 3


class GCodeSelectCoordinateSystem4(GCodeSelectCoordinateSystem):
    """Select Coordinate System 4"""
    word_key = Word('G', 57)
    coord_system_id = 4


class GCodeSelectCoordinateSystem5(GCodeSelectCoordinateSystem):
    """Select Coordinate System 5"""
    word_key = Word('G', 58)
    coord_system_id = 5


class GCodeSelectCoordinateSystem6(GCodeSelectCoordinateSystem):
    """Select Coordinate System 6"""
    word_key = Word('G', 59)
    coord_system_id = 6


class GCodeSelectCoordinateSystem7(GCodeSelectCoordinateSystem):
    """Select Coordinate System 7"""
    coord_system_id = 7
    word_key = Word('G', 59.1)


class GCodeSelectCoordinateSystem8(GCodeSelectCoordinateSystem):
    """Select Coordinate System 8"""
    word_key = Word('G', 59.2)
    coord_system_id = 8


class GCodeSelectCoordinateSystem9(GCodeSelectCoordinateSystem):
    """G9: Select Coordinate System 9"""
    word_key = Word('G', 59.3)
    coord_system_id = 9


# ======================= Flow-control Codes =======================
# CODE              PARAMETERS          DESCRIPTION
# o sub                                 Subroutines, sub/endsub call        [unsupported]
# o while                               Looping, while/endwhile do/while    [unsupported]
# o if                                  Conditional, if/else/endif          [unsupported]
# o repeat                              Repeat a loop of code               [unsupported]
# []                                    Indirection                         [unsupported]
# o call                                Call named file                     [unsupported]
# M70                                   Save modal state                    [unsupported]
# M71                                   Invalidate stored state             [unsupported]
# M72                                   Restore modal state                 [unsupported]
# M73                                   Save and Auto-restore modal state   [unsupported]


# ======================= Input/Output Codes =======================
# CODE              PARAMETERS          DESCRIPTION
# M62 - M65         P                   Digital Output Control
# M66               P E L Q             Wait on Input
# M67               T                   Analog Output, Synchronized
# M68               T                   Analog Output, Immediate

class GCodeDigitalOutputOnSyncd(GCodeDigitalOutput):
    """M62: turn on digital output synchronized with motion"""
    word_key = Word('M', 62)


class GCodeDigitalOutputOffSyncd(GCodeDigitalOutput):
    """M63: turn off digital output synchronized with motion"""
    word_key = Word('M', 63)


class GCodeDigitalOutputOn(GCodeDigitalOutput):
    """M64: turn on digital output immediately"""
    word_key = Word('M', 64)


class GCodeDigitalOutputOff(GCodeDigitalOutput):
    """M65: turn off digital output immediately"""
    word_key = Word('M', 65)


class GCodeWaitOnInput(GCodeIO):
    """M66: Wait on Input"""
    param_letters = set('PELQ')
    word_key = Word('M', 66)


class GCodeAnalogOutput(GCodeIO):
    """Analog Output"""
    param_letters = set('T')


class GCodeAnalogOutputSyncd(GCodeAnalogOutput):
    """M67: Analog Output, Synchronized"""
    word_key = Word('M', 67)


class GCodeAnalogOutputImmediate(GCodeAnalogOutput):
    """M68: Analog Output, Immediate"""
    word_key = Word('M', 68)


# ======================= Non-modal Codes =======================
# CODE              PARAMETERS          DESCRIPTION
# M6                T                   Tool Change
# M61               Q                   Set Current Tool
# G10 L1            P Q R               Set Tool Table
# G10 L10           P                   Set Tool Table
# G10 L11           P                   Set Tool Table
# G10 L2            P R ABCXYZ          Set Coordinate System
# G10 L20           P ABCXYZ            Set Coordinate System
# G28, G28.1                            Go/Set Predefined Position
# G29                                   Marlin2: Bed Leveling
# G30                                   Marlin2: Single Z-Probe
# G30, G30.1                            Go/Set Predefined Position
# G53                                   Move in Machine Coordinates
# G92               ABCXYZUVW           Coordinate System Offset
# G92.1, G92.2                          Reset G92 Offsets
# G92.3                                 Restore G92 Offsets
# M101 - M199       P Q                 User Defined Commands

class GCodeToolChange(GCodeNonModal):
    """M6: Tool Change"""
    param_letters = set('T')
    word_key = Word('M', 6)
    word_letter = 'M'
    exec_order = 80


class GCodeToolSetCurrent(GCodeNonModal):
    """M61: Set Current Tool"""
    param_letters = set('Q')
    word_key = Word('M', 61)
    word_letter = 'M'
    exec_order = 80

class GCodeSet(GCodeNonModal):
    """G10: Set stuff"""
    dialects = DIALECT_UNKNOWN
    param_letters = set('LPQRABCXYZ')
    word_key = Word('G', 10)
    exec_order = 230


class GCodeGotoPredefinedPosition(GCodeNonModal):
    """G28,G30: Goto Predefined Position (rapid movement)"""
    param_letters = set('W')
    @classmethod
    def word_matches(cls, w):
        return (w.letter == 'G') and (w.value in [28, 30])
    default_word = Word('G', 28)
    exec_order = 230


class GCodeSetPredefinedPosition(GCodeNonModal):
    """G28.1,G30.1: Set Predefined Position"""  # redundancy in language there, but I'll let it slide
    param_letters = set('W')
    @classmethod
    def word_matches(cls, w):
        return (w.letter == 'G') and (w.value in [28.1, 30.1])
    default_word = Word('G', 28.1)
    exec_order = 230

class GCodeMoveInMachineCoords(GCodeNonModal):
    """G53: Move in Machine Coordinates"""
    word_key = Word('G', 53)
    exec_order = 240


class GCodeCoordSystemOffset(GCodeNonModal):
    """G92: Coordinate System Offset"""
    param_letters = set('XYZABCUVW')
    word_key = Word('G', 92)
    exec_order = 230


class GCodeResetCoordSystemOffset(GCodeNonModal):
    """G92.1,G92.2: Reset Coordinate System Offset"""
    @classmethod
    def word_matches(cls, w):
        return (w.letter == 'G') and (w.value in [92.1, 92.2])
    default_word = Word('G', 92.1)
    exec_order = 230

    # TODO: machine.state.offset *= 0


class GCodeRestoreCoordSystemOffset(GCodeNonModal):
    """G92.3: Restore Coordinate System Offset"""
    word_key = Word('G', 92.3)
    exec_order = 230


class GCodeUserDefined(GCodeNonModal):
    """M101-M199: User Defined Commands"""
    word_letter = 'M'
    # To create user g-codes, inherit from this class
    param_letters = set('PQ')
    #@classmethod
    #def word_matches(cls, w):
    #    return (w.letter == 'M') and (101 <= w.value <= 199)
    #default_word = Word('M', 101)
    exec_order = 130
    modal_group = MODAL_GROUP_MAP['user_defined']

