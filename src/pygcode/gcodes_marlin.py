# DO NOT EDIT - file generated with pygcode/src/pygcode/tools/marlin_parse_MarlinDocumentation.py
from .gcodes_base import *

class GCodeLinearMove(GCodeMotion):
    """G0, G1: Add a straight line movement to the planner"""
    param_letters = "XYZEFS"
    dialects = ['marlin2']

    @classmethod
    def word_matches(cls, w):
        return (w.letter == 'G') and (w.value in [0, 1])
    default_word = Word('G', 0)

class GCodeArcOrCircleMove(GCodeArcMove):
    """G2, G3: Add an arc or circle movement to the planner"""
    param_letters = "XYZIJREFPS"
    dialects = ['marlin2']

    @classmethod
    def word_matches(cls, w):
        return (w.letter == 'G') and (w.value in [2, 3])
    default_word = Word('G', 2)

class GCodeDwell(GCode):
    """G4: Pause the planner"""
    param_letters = "SP"
    dialects = ['marlin2']
    word_key = Word('G', 4)

class GCodeBzierCubicSpline(GCodeMotion):
    """G5: Cubic B-spline with XYE destination and IJPQ offsets"""
    param_letters = "XYEFIJPQS"
    dialects = ['marlin2']
    word_key = Word('G', 5)

class GCodeDirectStepperMove(GCodeMotion):
    """G6: Perform a direct, uninterpolated, and non-kinematic synchronized move"""
    param_letters = "IRSXYZE"
    dialects = ['marlin2']
    word_key = Word('G', 6)

class GCodeRetract(GCode):
    """G10: Retract the filament"""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('G', 10)

class GCodeRecover(GCode):
    """G11: Recover the filament with firmware-based retract."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('G', 11)

class GCodeCleanTheNozzle(GCodeMotion):
    """G12: Perform the nozzle cleaning procedure."""
    param_letters = "PRSTXYZ"
    dialects = ['marlin2']
    word_key = Word('G', 12)

class GCodeCncWorkspacePlanes(GCodePlaneSelect):
    """G17, G18, G19: Select CNC workspace plane"""
    param_letters = ""
    dialects = ['marlin2']

    @classmethod
    def word_matches(cls, w):
        return (w.letter == 'G') and (w.value in [17, 18, 19])
    default_word = Word('G', 17)

class GCodeInchUnits(GCodeUnit):
    """G20: Set Units to Inches."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('G', 20)
    unit_id = 0
class GCodeMillimeterUnits(GCodeUnit):
    """G21: Set Units to Millimeters."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('G', 21)
    unit_id = 1
class GCodeMeshValidationPattern(GCodeMotion):
    """G26: Test the mesh and adjust."""
    param_letters = "BCDFHIKLOPQRSUXY"
    dialects = ['marlin2']
    word_key = Word('G', 26)

class GCodeParkToolhead(GCodeMotion):
    """G27: Park the current toolhead"""
    param_letters = "P"
    dialects = ['marlin2']
    word_key = Word('G', 27)

class GCodeAutoHome(GCodeMotion):
    """G28: Auto home one or more axes."""
    param_letters = "LORXYZ"
    dialects = ['marlin2']
    word_key = Word('G', 28)

#class GCodeBedLevelingPointg1(GCodeMotion):
#    """G29: Probe the bed and enable leveling compensation."""
#    param_letters = "ACOQEDJV"
#    dialects = ['marlin2']
#    word_key = Word('G', 29)

class GCodeBedLevelingBilinearm2(GCodeMotion):
    """G29: Probe the bed and enable leveling compensation."""
    param_letters = "ACOQXYZWSEDHFBLRJV"
    dialects = ['marlin2']
    word_key = Word('G', 29)

#class GCodeBedLevelingLinearg2(GCodeMotion):
#    """G29: Probe the bed and enable leveling compensation."""
#    param_letters = "ACOQXYPSEDTHFBLRJV"
#    dialects = ['marlin2']
#    word_key = Word('G', 29)

#class GCodeBedLevelingManualm1(GCodeMotion):
#    """G29: Measure Z heights in a grid, enable leveling compensation"""
#    param_letters = "SIJXYZ"
#    dialects = ['marlin2']
#    word_key = Word('G', 29)

#class GCodeBedLeveling(GCodeMotion):
#    """G29: Probe the bed and enable leveling compensation"""
#    param_letters = ""
#    dialects = ['marlin2']
#    word_key = Word('G', 29)

#class GCodeBedLevelingUnifiedm3(GCodeMotion):
#    """G29: Probe the bed and enable leveling compensation."""
#    param_letters = "ABCDEFHIJKLPQRSTUVWXY"
#    dialects = ['marlin2']
#    word_key = Word('G', 29)

class GCodeSingleZProbe(GCodeMotion):
    """G30: Probe bed at current XY location"""
    param_letters = "CXYE"
    dialects = ['marlin2']
    word_key = Word('G', 30)

class GCodeDockSled(GCodeMotion):
    """G31: Dock the Z probe sled."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('G', 31)

class GCodeUndockSled(GCodeMotion):
    """G32: Undock the Z probe sled."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('G', 32)

class GCodeDeltaAutoCalibration(GCodeMotion):
    """G33: Calibrate various Delta parameters"""
    param_letters = "CEFPTVOR"
    dialects = ['marlin2']
    word_key = Word('G', 33)

#class GCodeMechanicalGantryCalibrationb(GCodeMotion):
#    """G34: Modern replacement for Průša's TMC_Z_CALIBRATION"""
#    param_letters = "SZ"
#    dialects = ['marlin2']
#    word_key = Word('G', 34)

class GCodeZSteppersAutoAlignmenta(GCodeMotion):
    """G34: Align multiple Z steppers using a bed probe"""
    param_letters = "ITAE"
    dialects = ['marlin2']
    word_key = Word('G', 34)

class GCodeTrammingAssistant(GCodeMotion):
    """G35: Run a procedure to tram the bed"""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('G', 35)

class GCodeProbeTarget(GCodeMotion):
    """G38.2, G38.3, G38.4, G38.5: Probe towards (or away from) a workpiece"""
    param_letters = "XYZF"
    dialects = ['marlin2']

    @classmethod
    def word_matches(cls, w):
        return (w.letter == 'G') and (w.value in [38.2, 38.3, 38.4, 38.5])
    default_word = Word('G', 38)

class GCodeMoveToMeshCoordinate(GCodeSelectCoordinateSystem):
    """G42: Move to a specific point in the leveling mesh"""
    param_letters = "IJF"
    dialects = ['marlin2']
    word_key = Word('G', 42)

class GCodeMoveInMachineCoordinates(GCodeSelectCoordinateSystem):
    """G53: Apply native workspace to the current move."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('G', 53)

class GCodeWorkspaceCoordinateSystem(GCodeSelectCoordinateSystem):
    """G54, G55, G56, G57, G58, G59, G59.1, G59.2, G59.3: Select a workspace coordinate system"""
    param_letters = ""
    dialects = ['marlin2']

    @classmethod
    def word_matches(cls, w):
        return (w.letter == 'G') and (w.value in [54, 55, 56, 57, 58, 59, 59.1, 59.2, 59.3])
    default_word = Word('G', 54)

class GCodeSaveCurrentPosition(GCode):
    """G60: Save current position to specified slot"""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('G', 60)

class GCodeReturnToSavedPosition(GCodeMotion):
    """G61: Return to saved position of specified slot"""
    param_letters = "FSXYZE"
    dialects = ['marlin2']
    word_key = Word('G', 61)

class GCodeProbeTemperatureCalibration(GCodeOtherModal):
    """G76: Calibrate probe temperature compensation"""
    param_letters = "BP"
    dialects = ['marlin2']
    word_key = Word('G', 76)

class GCodeCancelCurrentMotionMode(GCode):
    """G80: Cancel the current motion mode"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('G', 80)

class GCodeAbsolutePositioning(GCodeOtherModal):
    """G90: Set the interpreter to absolute positions"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('G', 90)

class GCodeRelativePositioning(GCodeOtherModal):
    """G91: Set the interpreter to relative positions"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('G', 91)

class GCodeSetPosition(GCodeOtherModal):
    """G92: Set the current position of one or more axes."""
    param_letters = "XYZE"
    dialects = ['marlin2']
    word_key = Word('G', 92)

class GCodeBacklashCalibration(GCodeOtherModal):
    """G425: Use a conductive object to calibrate XYZ backlash"""
    param_letters = "BTVU"
    dialects = ['marlin2']
    word_key = Word('G', 425)

class GCodeUnconditionalStop(GCodeOtherModal):
    """M0, M1: Stop and wait for user"""
    param_letters = "SPg"
    dialects = ['marlin2']

    @classmethod
    def word_matches(cls, w):
        return (w.letter == 'M') and (w.value in [0, 1])
    default_word = Word('M', 0)

class GCodeSpindleCwLaserOn(GCodeSpindle):
    """M3: Set the spindle CW speed or laser power"""
    param_letters = "SOI"
    dialects = ['marlin2']
    word_key = Word('M', 3)

class GCodeSpindleCcwLaserOn(GCodeSpindle):
    """M4: Set the spindle CCW speed or laser power"""
    param_letters = "SOI"
    dialects = ['marlin2']
    word_key = Word('M', 4)

class GCodeSpindleLaserOff(GCodeSpindle):
    """M5: Turn off spindle or laser"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 5)

class GCodeCoolantControls(GCodeCoolant):
    """M7, M8, M9: Turn mist or flood coolant on / off"""
    param_letters = ""
    dialects = ['marlin2']

    @classmethod
    def word_matches(cls, w):
        return (w.letter == 'M') and (w.value in [7, 8, 9])
    default_word = Word('M', 7)

class GCodeVacuumBlowerControl(GCodeDigitalOutput):
    """M10, M11: Enable and disable the Cutter Vacuum or Laser Blower Motor."""
    param_letters = ""
    dialects = ['marlin2']

    @classmethod
    def word_matches(cls, w):
        return (w.letter == 'M') and (w.value in [10, 11])
    default_word = Word('M', 10)

class GCodeExpectedPrinterCheck(GCodeOtherModal):
    """M16: Prevent G-code usage on the wrong machine"""
    param_letters = "g"
    dialects = ['marlin2']
    word_key = Word('M', 16)

class GCodeEnableSteppers(GCodeOtherModal):
    """M17: Enable steppers"""
    param_letters = "'"
    dialects = ['marlin2']
    word_key = Word('M', 17)

class GCodeDisableSteppers(GCodeOtherModal):
    """M18, M84: Disable steppers (same as M84)."""
    param_letters = "S'"
    dialects = ['marlin2']

    @classmethod
    def word_matches(cls, w):
        return (w.letter == 'M') and (w.value in [18, 84])
    default_word = Word('M', 18)

class GCodeListSdCard(GCodeIO):
    """M20: List the contents of the SD Card."""
    param_letters = "FLT"
    dialects = ['marlin2']
    word_key = Word('M', 20)

class GCodeInitSdCard(GCodeIO):
    """M21: Attempt to detect an SD card in the slot."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 21)

class GCodeReleaseSdCard(GCodeIO):
    """M22: Simulate ejection of the SD card"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 22)

class GCodeSelectSdFile(GCodeIO):
    """M23: Select an SD file to be executed"""
    param_letters = "e"
    dialects = ['marlin2']
    word_key = Word('M', 23)

class GCodeStartOrResumeSdPrint(GCodeOtherModal):
    """M24: Start or resume a file selected with M23"""
    param_letters = "ST"
    dialects = ['marlin2']
    word_key = Word('M', 24)

class GCodePauseSdPrint(GCodeOtherModal):
    """M25: Pause printing from the SD card"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 25)

class GCodeSetSdPosition(GCodeIO):
    """M26: Set the SD read position"""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 26)

class GCodeReportSdPrintStatus(GCodeNonModal):
    """M27: Print SD progress to serial"""
    param_letters = "SC"
    dialects = ['marlin2']
    word_key = Word('M', 27)

class GCodeStartSdWrite(GCodeIO):
    """M28: Start writing to a file on the SD card"""
    param_letters = "1e"
    dialects = ['marlin2']
    word_key = Word('M', 28)

class GCodeStopSdWrite(GCodeIO):
    """M29: Stop writing the file, end logging."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 29)

class GCodeDeleteSdFile(GCodeIO):
    """M30: Delete a specified file from SD."""
    param_letters = "e"
    dialects = ['marlin2']
    word_key = Word('M', 30)

class GCodePrintTime(GCode):
    """M31: Report the current print time."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 31)

class GCodeSelectAndStart(GCodeIO):
    """M32: Begin an SD print from a file."""
    param_letters = "PS"
    dialects = ['marlin2']
    word_key = Word('M', 32)

class GCodeGetLongPath(GCodeIO):
    """M33: Convert a short pathname to a long pathname."""
    param_letters = "h"
    dialects = ['marlin2']
    word_key = Word('M', 33)

class GCodeSdcardSorting(GCodeIO):
    """M34: Set SDCard file sorting options."""
    param_letters = "SF"
    dialects = ['marlin2']
    word_key = Word('M', 34)

class GCodeSetPinState(GCodeDigitalOutput):
    """M42: Set an analog or digital pin to a specified state."""
    param_letters = "ITPS"
    dialects = ['marlin2']
    word_key = Word('M', 42)

class GCodeDebugPins(GCodeIO):
    """M43: Get information about pins / set pins"""
    param_letters = "PWETSIRL"
    dialects = ['marlin2']
    word_key = Word('M', 43)

class GCodeProbeRepeatabilityTest(GCodeMotion):
    """M48: Measure Z Probe repeatability."""
    param_letters = "CELPSVXY"
    dialects = ['marlin2']
    word_key = Word('M', 48)

class GCodeSetPrintProgress(GCode):
    """M73: Set current print progress percentage for LCD."""
    param_letters = "PR"
    dialects = ['marlin2']
    word_key = Word('M', 73)

class GCodeStartPrintJobTimer(GCodeOtherModal):
    """M75: Start the print job timer."""
    param_letters = "g"
    dialects = ['marlin2']
    word_key = Word('M', 75)

class GCodePausePrintJobTimer(GCodeOtherModal):
    """M76: Pause the print job timer."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 76)

class GCodeStopPrintJobTimer(GCodeOtherModal):
    """M77: Stop the print job timer."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 77)

class GCodePrintJobStats(GCode):
    """M78: Print statistics about print jobs."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 78)

class GCodePowerOn(GCodeOtherModal):
    """M80: Turn on the power supply"""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 80)

class GCodePowerOff(GCodeOtherModal):
    """M81: Turn off the power supply."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 81)

class GCodeEAbsolute(GCodeOtherModal):
    """M82: Set E to absolute positioning."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 82)

class GCodeERelative(GCodeOtherModal):
    """M83: Set E to relative positioning."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 83)

class GCodeInactivityShutdown(GCodeOtherModal):
    """M85: Set the inactivity timeout."""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 85)

class GCodeHotendIdleTimeout(GCodeOtherModal):
    """M86: Set the hotend idle timeout."""
    param_letters = "STEB"
    dialects = ['marlin2']
    word_key = Word('M', 86)

class GCodeDisableHotendIdleTimeout(GCodeOtherModal):
    """M87: Disable the hotend idle timeout."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 87)

class GCodeSetAxisStepsPerUnit(GCodeUnit):
    """M92: Set the number of steps-per-mm, per-inch, or per-degree"""
    param_letters = "XYZET"
    dialects = ['marlin2']
    word_key = Word('M', 92)

class GCodeFreeMemory(GCodeNonModal):
    """M100: Observe memory used by code"""
    param_letters = "DFIC"
    dialects = ['marlin2']
    word_key = Word('M', 100)

class GCodeConfigureBedDistanceSensor(GCodeOtherModal):
    """M102: Set parameters for the Bed Distance Sensor."""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 102)

class GCodeSetHotendTemperature(GCodeOtherModal):
    """M104: Set a new target hot end temperature."""
    param_letters = "ISFBT"
    dialects = ['marlin2']
    word_key = Word('M', 104)

class GCodeReportTemperatures(GCodeNonModal):
    """M105: Send a temperature report to the host."""
    param_letters = "RT"
    dialects = ['marlin2']
    word_key = Word('M', 105)

class GCodeSetFanSpeed(GCodeDigitalOutput):
    """M106: Turn on fan and set speed"""
    param_letters = "ISPT"
    dialects = ['marlin2']
    word_key = Word('M', 106)

class GCodeFanOff(GCodeDigitalOutput):
    """M107: Turn off a fan"""
    param_letters = "P"
    dialects = ['marlin2']
    word_key = Word('M', 107)

class GCodeBreakAndContinue(GCodeOtherModal):
    """M108: Break out of the current waiting loop"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 108)

class GCodeWaitForHotendTemperature(GCode):
    """M109: Wait for the hot end to reach its target."""
    param_letters = "ISRFBT"
    dialects = ['marlin2']
    word_key = Word('M', 109)

class GCodeSetLineNumber(GCodeOtherModal):
    """M110: Set the current line number."""
    param_letters = "N"
    dialects = ['marlin2']
    word_key = Word('M', 110)

class GCodeDebugLevel(GCodeOtherModal):
    """M111: Report and optionally set the debug flags."""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 111)

class GCodeFullShutdown(GCodeOtherModal):
    """M112: Shut everything down and halt the machine."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 112)

class GCodeHostKeepalive(GCode):
    """M113: Get or set the host keepalive interval."""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 113)

class GCodeGetCurrentPosition(GCodeNonModal):
    """M114: Report the current tool position to the host."""
    param_letters = "DER"
    dialects = ['marlin2']
    word_key = Word('M', 114)

class GCodeFirmwareInfo(GCodeNonModal):
    """M115: Print the firmware info and capabilities."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 115)

class GCodeSetLcdMessage(GCodeIO):
    """M117: Set the message line on the LCD."""
    param_letters = "g"
    dialects = ['marlin2']
    word_key = Word('M', 117)

class GCodeSerialPrint(GCodeIO):
    """M118: Send text to serial"""
    param_letters = "g11n"
    dialects = ['marlin2']
    word_key = Word('M', 118)

class GCodeEndstopStates(GCodeIO):
    """M119: Report endstop and probe states to the host."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 119)

class GCodeEnableEndstops(GCodeIO):
    """M120: Enable endstops and keep them enabled even when not homing."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 120)

class GCodeDisableEndstops(GCodeIO):
    """M121: Disable endstops and keep them disabled when not homing."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 121)

class GCodeTmcDebugging(GCodeIO):
    """M122: Get TMC Debug Info"""
    param_letters = "IXYZEVSP"
    dialects = ['marlin2']
    word_key = Word('M', 122)

class GCodeFanTachometers(GCodeIO):
    """M123: Report fan speeds from tachometers"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 123)

class GCodeParkHead(GCodeMotion):
    """M125: Save current position and move to filament change position."""
    param_letters = "LXYZP"
    dialects = ['marlin2']
    word_key = Word('M', 125)

class GCodeBaricuda1Open(GCodeDigitalOutput):
    """M126: Open the valve for Baricuda 1."""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 126)

class GCodeBaricuda1Close(GCodeDigitalOutput):
    """M127: Close the valve for Baricuda 1."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 127)

class GCodeBaricuda2Open(GCodeDigitalOutput):
    """M128: Open the valve for Baricuda 2."""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 128)

class GCodeBaricuda2Close(GCodeDigitalOutput):
    """M129: Close the valve for Baricuda 2."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 129)

class GCodeSetBedTemperature(GCodeOtherModal):
    """M140: Set a new target bed temperature."""
    param_letters = "IS"
    dialects = ['marlin2']
    word_key = Word('M', 140)

class GCodeSetChamberTemperature(GCodeOtherModal):
    """M141: Set a new target chamber temperature."""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 141)

class GCodeSetLaserCoolerTemperature(GCodeCoolant):
    """M143: Set a new target laser coolant temperature."""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 143)

class GCodeSetMaterialPreset(GCodeOtherModal):
    """M145: Set material presets in the LCD menu."""
    param_letters = "SHBF"
    dialects = ['marlin2']
    word_key = Word('M', 145)

class GCodeSetTemperatureUnits(GCodeUnit):
    """M149: Set temperature units to Celsius, Fahrenheit, or Kelvin."""
    param_letters = "CFK"
    dialects = ['marlin2']
    word_key = Word('M', 149)

class GCodeSetRgbWColor(GCodeDigitalOutput):
    """M150: Set the color of the RGB(W) LED, backlight, or LED strip."""
    param_letters = "RUBWPISK"
    dialects = ['marlin2']
    word_key = Word('M', 150)

class GCodePositionAutoReport(GCodeNonModal):
    """M154: Periodically auto-report position to serial"""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 154)

class GCodeTemperatureAutoReport(GCodeNonModal):
    """M155: Auto-report temperatures to host periodically."""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 155)

class GCodeSetMixFactor(GCodeOtherModal):
    """M163: Set a single mix factor for a mixing extruder."""
    param_letters = "SP"
    dialects = ['marlin2']
    word_key = Word('M', 163)

class GCodeSaveMix(GCodeOtherModal):
    """M164: Save the current mix as a virtual tool."""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 164)

class GCodeSetMix(GCodeOtherModal):
    """M165: Set all mix factors for the mixing extruder."""
    param_letters = "ABCDHI"
    dialects = ['marlin2']
    word_key = Word('M', 165)

class GCodeGradientMix(GCodeOtherModal):
    """M166: Set a Gradient Mix"""
    param_letters = "AZIJST"
    dialects = ['marlin2']
    word_key = Word('M', 166)

class GCodeWaitForBedTemperature(GCode):
    """M190: Wait for the bed to reach target temperature."""
    param_letters = "ISRT"
    dialects = ['marlin2']
    word_key = Word('M', 190)

class GCodeWaitForChamberTemperature(GCode):
    """M191: Wait for the chamber to reach target temperature."""
    param_letters = "SR"
    dialects = ['marlin2']
    word_key = Word('M', 191)

class GCodeWaitForProbeTemperature(GCode):
    """M192: Wait for the probe temperature sensor to reach a target"""
    param_letters = "RS"
    dialects = ['marlin2']
    word_key = Word('M', 192)

class GCodeSetLaserCoolerTemperatureAndWait(GCodeCoolant):
    """M193: Set a new target laser coolant temperature."""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 193)

class GCodeSetFilamentDiameterVolumetric(GCodeOtherModal):
    """M200: Set the diameter for volumetric extrusion."""
    param_letters = "DLST"
    dialects = ['marlin2']
    word_key = Word('M', 200)

class GCodePrintTravelMoveLimits(GCodeNonModal):
    """M201: Set acceleration / frequency limits for print and travel moves."""
    param_letters = "XYZETFS"
    dialects = ['marlin2']
    word_key = Word('M', 201)

class GCodeSetMaxFeedrate(GCodeFeedRateMode):
    """M203: Set maximum feedrate for one or more axes."""
    param_letters = "XYZET"
    dialects = ['marlin2']
    word_key = Word('M', 203)

class GCodeSetStartingAcceleration(GCodeOtherModal):
    """M204: Set the starting acceleration for moves by type."""
    param_letters = "PRTS"
    dialects = ['marlin2']
    word_key = Word('M', 204)

class GCodeSetAdvancedSettings(GCodeOtherModal):
    """M205: Set some advanced settings related to movement."""
    param_letters = "XYZEBSTJ"
    dialects = ['marlin2']
    word_key = Word('M', 205)

class GCodeSetHomeOffsets(GCodeOtherModal):
    """M206: Apply a persistent offset"""
    param_letters = "PTXYZ"
    dialects = ['marlin2']
    word_key = Word('M', 206)

class GCodeSetFirmwareRetraction(GCodeOtherModal):
    """M207: Set options for firmware-based retraction."""
    param_letters = "SWFZ"
    dialects = ['marlin2']
    word_key = Word('M', 207)

class GCodeFirmwareRecover(GCodeOtherModal):
    """M208: Firmware-retraction recover settings."""
    param_letters = "SWFR"
    dialects = ['marlin2']
    word_key = Word('M', 208)

class GCodeSetAutoRetract(GCodeOtherModal):
    """M209: Enable / disable auto-retraction."""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 209)

class GCodeSoftwareEndstops(GCodeOtherModal):
    """M211: Set and/or get the software endstops state"""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 211)

class GCodeFilamentSwapParameters(GCodeOtherModal):
    """M217: Set length and speed for filament swapping"""
    param_letters = "QSBEPRUFGALWXYVZ"
    dialects = ['marlin2']
    word_key = Word('M', 217)

class GCodeSetHotendOffset(GCodeOtherModal):
    """M218: Set the offset of a hotend (from hotend 0)."""
    param_letters = "TXYZ"
    dialects = ['marlin2']
    word_key = Word('M', 218)

class GCodeSetFeedratePercentage(GCodeFeedRateMode):
    """M220: Set the global feedrate percentage."""
    param_letters = "SBR"
    dialects = ['marlin2']
    word_key = Word('M', 220)

class GCodeSetFlowPercentage(GCodeOtherModal):
    """M221: Set the flow percentage, which applies to all E moves."""
    param_letters = "ST"
    dialects = ['marlin2']
    word_key = Word('M', 221)

class GCodeWaitForPinState(GCodeIO):
    """M226: Wait for a pin to have a given state."""
    param_letters = "PS"
    dialects = ['marlin2']
    word_key = Word('M', 226)

class GCodeTriggerCamera(GCodeIO):
    """M240: Trigger a camera shutter"""
    param_letters = "ABDFIJPRSXYZ"
    dialects = ['marlin2']
    word_key = Word('M', 240)

class GCodeLcdContrast(GCodeIO):
    """M250: Set and/or get the LCD contrast."""
    param_letters = "C"
    dialects = ['marlin2']
    word_key = Word('M', 250)

class GCodeLcdSleepBacklightTimeout(GCodeIO):
    """M255: Set and/or get the LCD Sleep Timeout."""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 255)

class GCodeLcdBrightness(GCodeIO):
    """M256: Set and/or get the LCD brightness."""
    param_letters = "B"
    dialects = ['marlin2']
    word_key = Word('M', 256)

class GCodeICSend(GCodeDigitalOutput):
    """M260: Send data to the I2C bus."""
    param_letters = "ABRS"
    dialects = ['marlin2']
    word_key = Word('M', 260)

class GCodeICRequest(GCodeIO):
    """M261: Request and echo bytes from the I2C bus."""
    param_letters = "ABS"
    dialects = ['marlin2']
    word_key = Word('M', 261)

class GCodeServoPosition(GCodeIO):
    """M280: Set or get a servo position."""
    param_letters = "PS"
    dialects = ['marlin2']
    word_key = Word('M', 280)

class GCodeEditServoAngles(GCodeOtherModal):
    """M281: Set servo deploy and/or stow angles"""
    param_letters = "PLU"
    dialects = ['marlin2']
    word_key = Word('M', 281)

class GCodeDetachServo(GCodeOtherModal):
    """M282: Detach a servo until its next move"""
    param_letters = "P"
    dialects = ['marlin2']
    word_key = Word('M', 282)

class GCodeBabystep(GCodeMotion):
    """M290: Babystep one or more axes"""
    param_letters = "XYZSP"
    dialects = ['marlin2']
    word_key = Word('M', 290)

class GCodePlayTone(GCodeDigitalOutput):
    """M300: Play a single tone, buzz, or beep."""
    param_letters = "PS"
    dialects = ['marlin2']
    word_key = Word('M', 300)

class GCodeSetHotendPid(GCodeOtherModal):
    """M301: Set PID values for a hotend."""
    param_letters = "EPIDCLF"
    dialects = ['marlin2']
    word_key = Word('M', 301)

class GCodeColdExtrude(GCodeOtherModal):
    """M302: Set minimum extrusion temperature, allow cold extrusion."""
    param_letters = "SP"
    dialects = ['marlin2']
    word_key = Word('M', 302)

class GCodePidAutotune(GCodeOtherModal):
    """M303: Auto-tune the PID system to find stable values."""
    param_letters = "ECSUD"
    dialects = ['marlin2']
    word_key = Word('M', 303)

class GCodeSetBedPid(GCodeOtherModal):
    """M304: Set PID values for the heated bed."""
    param_letters = "PID"
    dialects = ['marlin2']
    word_key = Word('M', 304)

class GCodeUserThermistorParameters(GCodeOtherModal):
    """M305: Set (or report) custom thermistor parameters"""
    param_letters = "PRTBC"
    dialects = ['marlin2']
    word_key = Word('M', 305)

class GCodeModelPredictiveTempControl(GCodeOtherModal):
    """M306: Set MPC values for a hotend."""
    param_letters = "ACEFHPRST"
    dialects = ['marlin2']
    word_key = Word('M', 306)

class GCodeSetMicroStepping(GCodeOtherModal):
    """M350: Set micro-stepping for drivers that support it"""
    param_letters = "BSXYZE"
    dialects = ['marlin2']
    word_key = Word('M', 350)

class GCodeSetMicrostepPins(GCodeOtherModal):
    """M351: Directly set the micro-stepping pins"""
    param_letters = "SBXYZE"
    dialects = ['marlin2']
    word_key = Word('M', 351)

class GCodeCaseLightControl(GCodeDigitalOutput):
    """M355: Turn the case light on or off, set brightness"""
    param_letters = "PS"
    dialects = ['marlin2']
    word_key = Word('M', 355)

class GCodeScaraThetaA(GCodeMotion):
    """M360: Move to Theta A"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 360)

class GCodeScaraThetaB(GCodeMotion):
    """M361: Move to Theta-B"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 361)

class GCodeScaraPsiA(GCodeMotion):
    """M362: Move to Psi-A"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 362)

class GCodeScaraPsiB(GCodeMotion):
    """M363: Move to Psi-B"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 363)

class GCodeScaraPsiC(GCodeMotion):
    """M364: Move to Psi-C"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 364)

class GCodeActivateSolenoid(GCodeDigitalOutput):
    """M380: Activate"""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 380)

class GCodeDeactivateSolenoids(GCodeDigitalOutput):
    """M381: Deactivate all extruder solenoids"""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 381)

class GCodeFinishMoves(GCodeOtherModal):
    """M400: Wait for all moves to finish"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 400)

class GCodeDeployProbe(GCodeDigitalOutput):
    """M401: Deploy the bed probe"""
    param_letters = "HS"
    dialects = ['marlin2']
    word_key = Word('M', 401)

class GCodeStowProbe(GCodeDigitalOutput):
    """M402: Stow the bed probe"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 402)

class GCodeMmuFilamentType(GCodeOtherModal):
    """M403: Set filament type for Multi-Material Unit 2.0"""
    param_letters = "EF"
    dialects = ['marlin2']
    word_key = Word('M', 403)

class GCodeSetFilamentDiameter(GCodeOtherModal):
    """M404: Set the nominal diameter for filament width sensor auto-flow"""
    param_letters = "W"
    dialects = ['marlin2']
    word_key = Word('M', 404)

class GCodeFilamentWidthSensorOn(GCodeOtherModal):
    """M405: Enable filament width sensor flow control"""
    param_letters = "D"
    dialects = ['marlin2']
    word_key = Word('M', 405)

class GCodeFilamentWidthSensorOff(GCodeOtherModal):
    """M406: Disable filament width sensor flow control"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 406)

class GCodeFilamentWidth(GCodeNonModal):
    """M407: Report the measured filament width"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 407)

class GCodeQuickstop(GCodeOtherModal):
    """M410: Stop all steppers instantly"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 410)

class GCodeFilamentRunout(GCodeOtherModal):
    """M412: Get/set filament runout detection parameters"""
    param_letters = "DHSR"
    dialects = ['marlin2']
    word_key = Word('M', 412)

class GCodePowerLossRecovery(GCodeOtherModal):
    """M413: Enable / disable power-loss recovery"""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 413)

class GCodeBedLevelingState(GCodeNonModal):
    """M420: Get and/or set bed leveling state and parameters"""
    param_letters = "LSVTZC"
    dialects = ['marlin2']
    word_key = Word('M', 420)

class GCodeSetMeshValue(GCodeOtherModal):
    """M421: Set a single mesh Z height"""
    param_letters = "IJXYZQCN"
    dialects = ['marlin2']
    word_key = Word('M', 421)

class GCodeSetZMotorXy(GCodeOtherModal):
    """M422: Set a Z motor position for G34 Auto-Alignment"""
    param_letters = "RSWXY"
    dialects = ['marlin2']
    word_key = Word('M', 422)

class GCodeXTwistCompensation(GCodeOtherModal):
    """M423: Modify, reset, and report X-Axis Twist Compensation data"""
    param_letters = "RAIXZ"
    dialects = ['marlin2']
    word_key = Word('M', 423)

class GCodeBacklashCompensation(GCodeOtherModal):
    """M425: Enable and tune backlash compensation"""
    param_letters = "FSXYZZ"
    dialects = ['marlin2']
    word_key = Word('M', 425)

class GCodeHomeOffsetsHere(GCodeOtherModal):
    """M428: Set home offsets based on current position"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 428)

class GCodePowerMonitor(GCodeOtherModal):
    """M430: Read and display current (A), voltage (V), and power (W)"""
    param_letters = "IVW"
    dialects = ['marlin2']
    word_key = Word('M', 430)

class GCodeCancelObjects(GCodeOtherModal):
    """M486: Identify and cancel objects"""
    param_letters = "CPSTU"
    dialects = ['marlin2']
    word_key = Word('M', 486)

class GCodeFixedTimeMotion(GCodeOtherModal):
    """M493: Enable/disable and configure Fixed-Time Motion, Linear Advance, and Input Shaping"""
    param_letters = "SPKDABFH"
    dialects = ['marlin2']
    word_key = Word('M', 493)

class GCodeSaveSettings(GCodeNonModal):
    """M500: Save settings to EEPROM."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 500)

class GCodeRestoreSettings(GCodeOtherModal):
    """M501: Restore settings from EEPROM."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 501)

class GCodeFactoryReset(GCodeOtherModal):
    """M502: Restore all settings to factory defaults."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 502)

class GCodeReportSettings(GCodeNonModal):
    """M503: Report all settings that may be saved to EEPROM."""
    param_letters = "SC"
    dialects = ['marlin2']
    word_key = Word('M', 503)

class GCodeValidateEepromContents(GCodeNonModal):
    """M504: Validate the contents of the EEPROM."""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 504)

class GCodeLockMachine(GCodeOtherModal):
    """M510: Lock the machine if it has a passcode"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 510)

class GCodeUnlockMachine(GCodeOtherModal):
    """M511: Unlock the machine if it has a passcode"""
    param_letters = "P"
    dialects = ['marlin2']
    word_key = Word('M', 511)

class GCodeSetPasscode(GCodeNonModal):
    """M512: Set a numeric passcode for locking the machine"""
    param_letters = "PS"
    dialects = ['marlin2']
    word_key = Word('M', 512)

class GCodeAbortSdPrint(GCodeOtherModal):
    """M524: Abort an SD print started with [`M24`](/docs/gcode/M024.html)"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 524)

class GCodeEndstopsAbortSd(GCodeNonModal):
    """M540: Abort SD printing when an endstop is triggered."""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 540)

class GCodeSetTmcSteppingMode(GCodeOtherModal):
    """M569: Toggle stealthChop"""
    param_letters = "XYZEIT"
    dialects = ['marlin2']
    word_key = Word('M', 569)

class GCodeSerialBaudRate(GCodeOtherModal):
    """M575: Change the serial baud rate"""
    param_letters = "PB"
    dialects = ['marlin2']
    word_key = Word('M', 575)

class GCodeNonlinearExtrusionControl(GCodeOtherModal):
    """M592: Get or set Nonlinear Extrusion parameters"""
    param_letters = "ABC"
    dialects = ['marlin2']
    word_key = Word('M', 592)

class GCodeZvInputShaping(GCodeOtherModal):
    """M593: Get or set Marlin's integrated ZV Input Shaping parameters"""
    param_letters = "DFXY"
    dialects = ['marlin2']
    word_key = Word('M', 593)

class GCodeFilamentChange(GCode):
    """M600: Automatically change filament"""
    param_letters = "TEULXYZBR"
    dialects = ['marlin2']
    word_key = Word('M', 600)

class GCodeConfigureFilamentChange(GCodeOtherModal):
    """M603: Configure automatic filament change parameters"""
    param_letters = "TUL"
    dialects = ['marlin2']
    word_key = Word('M', 603)

class GCodeMultiNozzleMode(GCodeOtherModal):
    """M605: Set the behavior mode for a multiple nozzle setup"""
    param_letters = "SXRPE"
    dialects = ['marlin2']
    word_key = Word('M', 605)

#class GCodeDeltaConfiguration(GCodeOtherModal):
#    """M665: Set delta geometry values"""
#    param_letters = "HLRSXYZABC"
#    dialects = ['marlin2']
#    word_key = Word('M', 665)

class GCodeScaraConfigurationb(GCodeOtherModal):
    """M665: Set SCARA geometry values"""
    param_letters = "SPTAXBY"
    dialects = ['marlin2']
    word_key = Word('M', 665)

class GCodeSetDualEndstopOffsetsb(GCodeOtherModal):
    """M666: Set dual endstop offsets"""
    param_letters = "XYZ"
    dialects = ['marlin2']
    word_key = Word('M', 666)

#class GCodeSetDeltaEndstopAdjustmentsa(GCodeOtherModal):
#    """M666: Set Delta endstop adjustments"""
#    param_letters = "XYZ"
#    dialects = ['marlin2']
#    word_key = Word('M', 666)

class GCodeDuetSmartEffectorSensitivity(GCodeOtherModal):
    """M672: Set Duet Smart Effector sensitivity"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 672)

class GCodeLoadFilament(GCodeOtherModal):
    """M701: Load filament"""
    param_letters = "TZL"
    dialects = ['marlin2']
    word_key = Word('M', 701)

class GCodeUnloadFilament(GCodeOtherModal):
    """M702: Unload filament"""
    param_letters = "TZU"
    dialects = ['marlin2']
    word_key = Word('M', 702)

class GCodeControllerFanSettings(GCodeOtherModal):
    """M710: Set or report controller fan settings"""
    param_letters = "SIARD"
    dialects = ['marlin2']
    word_key = Word('M', 710)

class GCodeMaxControl(GCodeDigitalOutput):
    """M7219: Control Max7219 Segmented LEDs"""
    param_letters = "CDRIFPUVXY"
    dialects = ['marlin2']
    word_key = Word('M', 7219)

class GCodeRepeatMarker(GCodeOtherModal):
    """M808: Set or go to a marker for looping G-code"""
    param_letters = "L"
    dialects = ['marlin2']
    word_key = Word('M', 808)

class GCodeGCodeMacros(GCodeOtherModal):
    """M810, M811, M812, M813, M814, M815, M816, M817, M818, M819: Set/execute one of ten G-code macros"""
    param_letters = "g"
    dialects = ['marlin2']

    @classmethod
    def word_matches(cls, w):
        return (w.letter == 'M') and (w.value in [810, 811, 812, 813, 814, 815, 816, 817, 818, 819])
    default_word = Word('M', 810)

class GCodeXyzProbeOffset(GCodeOtherModal):
    """M851: Set the Z probe XYZ offset from nozzle"""
    param_letters = "XYZ"
    dialects = ['marlin2']
    word_key = Word('M', 851)

class GCodeBedSkewCompensation(GCodeOtherModal):
    """M852: Misalignment in the XYZ axes."""
    param_letters = "IJKS"
    dialects = ['marlin2']
    word_key = Word('M', 852)

class GCodeICPositionEncoders(GCodeOtherModal):
    """M860, M861, M862, M863, M864, M865, M866, M867, M868, M869: I2C position encoders for closed loop control"""
    param_letters = "IOXYZEUPSRST"
    dialects = ['marlin2']

    @classmethod
    def word_matches(cls, w):
        return (w.letter == 'M') and (w.value in [860, 861, 862, 863, 864, 865, 866, 867, 868, 869])
    default_word = Word('M', 860)

class GCodeProbeTemperatureConfig(GCodeOtherModal):
    """M871: Configure probe temperature compensation"""
    param_letters = "VIBPER"
    dialects = ['marlin2']
    word_key = Word('M', 871)

class GCodeHandlePromptResponse(GCode):
    """M876: Handle Host prompt responses"""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 876)

class GCodeLinearAdvanceFactor(GCodeOtherModal):
    """M900: Get and set Linear Advance K value"""
    param_letters = "KLST"
    dialects = ['marlin2']
    word_key = Word('M', 900)

class GCodeStepperMotorCurrent(GCodeOtherModal):
    """M906: Set the motor current (in milliamps)"""
    param_letters = "EITXYZ"
    dialects = ['marlin2']
    word_key = Word('M', 906)

class GCodeSetMotorCurrent(GCodeOtherModal):
    """M907: Set motor current via digital trimpot"""
    param_letters = "BCDESXYZ"
    dialects = ['marlin2']
    word_key = Word('M', 907)

class GCodeSetTrimpotPins(GCodeOtherModal):
    """M908: Set a digital trimpot directly"""
    param_letters = "PS"
    dialects = ['marlin2']
    word_key = Word('M', 908)

class GCodeDacPrintValues(GCodeNonModal):
    """M909: Report DAC current values to host"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 909)

class GCodeCommitDacToEeprom(GCodeNonModal):
    """M910: Commit digipot/DAC value to external EEPROM"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 910)

class GCodeTmcOtPreWarnCondition(GCode):
    """M911: Driver overtemperature pre-warn condition"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 911)

class GCodeClearTmcOtPreWarn(GCode):
    """M912: Clear overtemperature pre-warn condition flag"""
    param_letters = "IXYZE"
    dialects = ['marlin2']
    word_key = Word('M', 912)

class GCodeSetHybridThresholdSpeed(GCodeOtherModal):
    """M913: TMC driver switching to spreadCycle"""
    param_letters = "ITXYZE"
    dialects = ['marlin2']
    word_key = Word('M', 913)

class GCodeTmcBumpSensitivity(GCodeOtherModal):
    """M914: Set sensorless homing sensitivity"""
    param_letters = "IXYZ"
    dialects = ['marlin2']
    word_key = Word('M', 914)

class GCodeTmcZAxisCalibration(GCode):
    """M915: Align ends of the Z axis and test torque"""
    param_letters = "SZ"
    dialects = ['marlin2']
    word_key = Word('M', 915)

class GCodeLThermalWarningTest(GCode):
    """M916: Find L6474 drive level (KVAL_HOLD) threshold"""
    param_letters = "JXYZEFTKD"
    dialects = ['marlin2']
    word_key = Word('M', 916)

class GCodeLOvercurrentWarningTest(GCode):
    """M917: Find L6474 minimum current thresholds"""
    param_letters = "JXYZEFITK"
    dialects = ['marlin2']
    word_key = Word('M', 917)

class GCodeLSpeedWarningTest(GCode):
    """M918: Find L6474 speed threshold"""
    param_letters = "JXYZEITKM"
    dialects = ['marlin2']
    word_key = Word('M', 918)

class GCodeTmcChopperTiming(GCodeOtherModal):
    """M919: Set Chopper Timing values for TMC stepper drivers"""
    param_letters = "OPSITXYZABCUVW"
    dialects = ['marlin2']
    word_key = Word('M', 919)

class GCodeStartSdLogging(GCodeIO):
    """M928: Log serial input to an SD file"""
    param_letters = "e"
    dialects = ['marlin2']
    word_key = Word('M', 928)

class GCodeMagneticParkingExtruder(GCodeOtherModal):
    """M951: Set / report Magnetic Parking Extruder settings"""
    param_letters = "LRIJHDC"
    dialects = ['marlin2']
    word_key = Word('M', 951)

class GCodeBackUpFlashSettingsToSd(GCodeIO):
    """M993: Create a backup of SPI Flash to SD"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 993)

class GCodeRestoreFlashFromSd(GCodeIO):
    """M994: Restore a backup from SD to SPI Flash"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 994)

class GCodeTouchScreenCalibration(GCodeIO):
    """M995: Touch screen calibration for TFT display"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 995)

class GCodeFirmwareUpdate(GCode):
    """M997: Perform in-application firmware update"""
    param_letters = ""
    dialects = ['marlin2']
    word_key = Word('M', 997)

class GCodeStopRestart(GCodeOtherModal):
    """M999: Return the machine to Running state"""
    param_letters = "S"
    dialects = ['marlin2']
    word_key = Word('M', 999)

class GCodeSelectOrReportTool(GCodeOtherModal):
    """T0, T1, T2, T3, T4, T5, T6, T7: Set or report the current extruder or other tool"""
    param_letters = "FS"
    dialects = ['marlin2']

    @classmethod
    def word_matches(cls, w):
        return (w.letter == 'T') and (w.value in [0, 1, 2, 3, 4, 5, 6, 7])
    default_word = Word('T', 0)

class GCodeMmuSpecialCommands(GCode):
    """'T?', Tc, Tx: MMU2 special filament loading commands"""
    param_letters = ""
    dialects = ['marlin2']

    @classmethod
    def word_matches(cls, w):
        return (w.letter == 'T') and (w.value in ['?', 'c', 'x'])
    default_word = Word('T', 1)

