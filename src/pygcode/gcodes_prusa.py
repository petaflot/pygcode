from .gcodes_base import *

from .gcodes_legacy import *

# ======================= Prusa =======================
# CODE              PARAMETERS          DESCRIPTION
# M862.1            P Q                 Nozzle Diameter
# M862.2            P Q                 Model Code
# M862.3            P Q                 Model Name
# M862.4            P Q                 Firmware Version
# M862.5            P Q                 GCode Level
# M115              V U                 Firmware info
# M73               P R Q S C D         Set/Get print progress
# M205              S T B X Y Z E       Set advanced settings
# M104              S                   Set extruder temperature
# M109              B R S               Wait for extruder temperature
# M140              S                   Set bed temperature
# M190              R S                 Wait for bed temperature
# M204              S T                 Acceleration settings
# M221              S T                 Set extrude factor override percentage
# M106              S                   Set fan speed
# G80               N R V L R F B       Mesh-based Z probe

class GCodePrintChecking(GCode):
    exec_order = 999
    modal_group = MODAL_GROUP_MAP['user_defined']
    param_letters = set('PQ')

class GCodeNozzleDiameterPrintChecking(GCodePrintChecking):
    """M862.1: Nozzle Diameter"""
    word_key = Word('M', 862.1)

class GCodeModelCodePrintChecking(GCodePrintChecking):
    """M862.2: Model Code"""
    word_key = Word('M', 862.2)

class GCodeModelNamePrintChecking(GCodePrintChecking):
    """M862.3: Model Name"""
    word_key = Word('M', 862.3)

class GCodeFirmwareVersionPrintChecking(GCodePrintChecking):
    """M862.4: Firmware Version"""
    word_key = Word('M', 862.4)

class GCodeGcodeLevelPrintChecking(GCodePrintChecking):
    """M862.5: Gcode Level"""
    word_key = Word('M', 862.5)

class GCodeFirmwareInfo(GCode):
    exec_order = 999
    modal_group = MODAL_GROUP_MAP['user_defined']
    param_letters = set('VU')
    word_key = Word('M', 115)

class GCodePrintProgress(GCode):
    exec_order = 999
    modal_group = MODAL_GROUP_MAP['user_defined']
    param_letters = set('PRQSCD')
    word_key = Word('M', 73)

class GCodeSetAdvancedSettings(GCode):
    exec_order = 999
    modal_group = MODAL_GROUP_MAP['user_defined']
    param_letters = set('STBXYZE')
    word_key = Word('M', 205)

class GCodeSetExtruderTemperature(GCode):
    """M104: Set Extruder Temperature"""
    exec_order = 999
    modal_group = MODAL_GROUP_MAP['user_defined']
    word_key = Word('M', 104)
    param_letters = set('S')

class GCodeWaitForExtruderTemperature(GCode):
    exec_order = 999
    modal_group = MODAL_GROUP_MAP['user_defined']
    param_letters = set('BRS')
    word_key = Word('M', 109)

class GCodeSetBedTemperature(GCode):
    exec_order = 999
    modal_group = MODAL_GROUP_MAP['user_defined']
    param_letters = set('S')
    word_key = Word('M', 140)

class GCodeWaitForBedTemperature(GCode):
    exec_order = 999
    modal_group = MODAL_GROUP_MAP['user_defined']
    param_letters = set('RS')
    word_key = Word('M', 190)

class GCodeAccelerationSettings(GCode):
    exec_order = 999
    modal_group = MODAL_GROUP_MAP['user_defined']
    param_letters = set('ST')
    word_key = Word('M', 204)

class GCodeSetExtrudeFactorOverridePercentage(GCode):
    exec_order = 999
    modal_group = MODAL_GROUP_MAP['user_defined']
    param_letters = set('ST')
    word_key = Word('M', 221)

class GCodeSetFanSpeed(GCode):
    exec_order = 999
    modal_group = MODAL_GROUP_MAP['user_defined']
    param_letters = set('S')
    word_key = Word('M', 106)

class GCodeMeshBasedZProbe(GCode):
    exec_order = 999
    modal_group = MODAL_GROUP_MAP['user_defined']
    param_letters = set('NRVLRFB')
    word_key = Word('G', 80)



