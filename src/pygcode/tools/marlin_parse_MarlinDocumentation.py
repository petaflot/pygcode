#!/usr/bin/env python
# vim: number ts=4
"""
    generate src/pygcode/gcode_marlin.py based on official documentation
"""
from string import ascii_letters

class_types = {
    # unused: GCodeDistanceMode
    # unused: GCodePathControlMode
    # unused: GCodeProgramControl
	'g000': 'GCodeMotion', # LinearMove
	'g002': 'GCodeArcMove', # ArcOrCircleMove
	'g004': 'GCode', # Dwell
	'g005': 'GCodeMotion', # BzierCubicSpline
	'g006': 'GCodeMotion', # DirectStepperMove
	'g010': 'GCode', # Retract
	'g011': 'GCode', # Recover
	'g012': 'GCodeMotion', # CleanTheNozzle
	'g017': 'GCodePlaneSelect', # CncWorkspacePlanes
	'g020': 'GCodeUnit', # InchUnits
	'g021': 'GCodeUnit', # MillimeterUnits
	'g026': 'GCodeMotion', # MeshValidationPattern
	'g027': 'GCodeMotion', # ParkToolhead
	'g028': 'GCodeMotion', # AutoHome
	'g029': 'GCodeMotion', # BedLeveling
	'g029g1': 'GCodeMotion', # BedLevelingPoint
	'g029m2': 'GCodeMotion', # BedLevelingBilinear
	'g029g2': 'GCodeMotion', # BedLevelingLinear
	'g029m1': 'GCodeMotion', # BedLevelingManual
	'g029m3': 'GCodeMotion', # BedLevelingUnified
	'g030': 'GCodeMotion', # SingleZProbe
	'g031': 'GCodeMotion', # DockSled
	'g032': 'GCodeMotion', # UndockSled
	'g033': 'GCodeMotion', # DeltaAutoCalibration
	'g034b': 'GCodeMotion', # MechanicalGantryCalibration
	'g034a': 'GCodeMotion', # ZSteppersAutoAlignment
	'g035': 'GCodeMotion', # TrammingAssistant
	'g038': 'GCodeMotion', # ProbeTarget
	'g042': 'GCodeSelectCoordinateSystem', # MoveToMeshCoordinate
	'g053': 'GCodeSelectCoordinateSystem', # MoveInMachineCoordinates
	'g054': 'GCodeSelectCoordinateSystem', # WorkspaceCoordinateSystem
	'g060': 'GCode', # SaveCurrentPosition
	'g061': 'GCodeMotion', # ReturnToSavedPosition
	'g076': 'GCodeOtherModal', # ProbeTemperatureCalibration
	'g080': 'GCode', # CancelCurrentMotionMode
	'g090': 'GCodeOtherModal', # AbsolutePositioning
	'g091': 'GCodeOtherModal', # RelativePositioning
	'g092': 'GCodeOtherModal', # SetPosition
	'g425': 'GCodeOtherModal', # BacklashCalibration
	'm0000': 'GCodeOtherModal', # UnconditionalStop
	'm0003': 'GCodeSpindle', # SpindleCwLaserOn
	'm0004': 'GCodeSpindle', # SpindleCcwLaserOn
	'm0005': 'GCodeSpindle', # SpindleLaserOff
	'm0007': 'GCodeCoolant', # CoolantControls
	'm0010': 'GCodeDigitalOutput', # VacuumBlowerControl
	'm0016': 'GCodeOtherModal', # ExpectedPrinterCheck
	'm0017': 'GCodeOtherModal', # EnableSteppers
	'm0018': 'GCodeOtherModal', # DisableSteppers
	'm0020': 'GCodeIO', # ListSdCard
	'm0021': 'GCodeIO', # InitSdCard
	'm0022': 'GCodeIO', # ReleaseSdCard
	'm0023': 'GCodeIO', # SelectSdFile
	'm0024': 'GCodeOtherModal', # StartOrResumeSdPrint
	'm0025': 'GCodeOtherModal', # PauseSdPrint
	'm0026': 'GCodeIO', # SetSdPosition
	'm0027': 'GCodeNonModal', # ReportSdPrintStatus
	'm0028': 'GCodeIO', # StartSdWrite
	'm0029': 'GCodeIO', # StopSdWrite
	'm0030': 'GCodeIO', # DeleteSdFile
	'm0031': 'GCode', # PrintTime
	'm0032': 'GCodeIO', # SelectAndStart
	'm0033': 'GCodeIO', # GetLongPath
	'm0034': 'GCodeIO', # SdcardSorting
	'm0042': 'GCodeDigitalOutput', # SetPinState
	'm0043': 'GCodeIO', # DebugPins
	'm0043b': 'GCodeDigitalOutput', # TogglePins
	'm0048': 'GCodeMotion', # ProbeRepeatabilityTest
	'm0073': 'GCode', # SetPrintProgress
	'm0075': 'GCodeOtherModal', # StartPrintJobTimer
	'm0076': 'GCodeOtherModal', # PausePrintJobTimer
	'm0077': 'GCodeOtherModal', # StopPrintJobTimer
	'm0078': 'GCode', # PrintJobStats
	'm0080': 'GCodeOtherModal', # PowerOn
	'm0081': 'GCodeOtherModal', # PowerOff
	'm0082': 'GCodeOtherModal', # EAbsolute
	'm0083': 'GCodeOtherModal', # ERelative
	'm0085': 'GCodeOtherModal', # InactivityShutdown
	'm0086': 'GCodeOtherModal', # HotendIdleTimeout
	'm0087': 'GCodeOtherModal', # DisableHotendIdleTimeout
	'm0092': 'GCodeUnit', # SetAxisStepsPerUnit
	'm0100': 'GCodeNonModal', # FreeMemory
	'm0102': 'GCodeOtherModal', # ConfigureBedDistanceSensor
	'm0104': 'GCodeOtherModal', # SetHotendTemperature
	'm0105': 'GCodeNonModal', # ReportTemperatures
	'm0106': 'GCodeDigitalOutput', # SetFanSpeed
	'm0107': 'GCodeDigitalOutput', # FanOff
	'm0108': 'GCodeOtherModal', # BreakAndContinue
	'm0109': 'GCode', # WaitForHotendTemperature
	'm0110': 'GCodeOtherModal', # SetLineNumber
	'm0111': 'GCodeOtherModal', # DebugLevel
	'm0112': 'GCodeOtherModal', # FullShutdown
	'm0113': 'GCode', # HostKeepalive
	'm0114': 'GCodeNonModal', # GetCurrentPosition
	'm0115': 'GCodeNonModal', # FirmwareInfo
	'm0117': 'GCodeIO', # SetLcdMessage
	'm0118': 'GCodeIO', # SerialPrint
	'm0119': 'GCodeIO', # EndstopStates
	'm0120': 'GCodeIO', # EnableEndstops
	'm0121': 'GCodeIO', # DisableEndstops
	'm0122': 'GCodeIO', # TmcDebugging
	'm0123': 'GCodeIO', # FanTachometers
	'm0125': 'GCodeMotion', # ParkHead
	'm0126': 'GCodeDigitalOutput', # BaricudaOpen
	'm0127': 'GCodeDigitalOutput', # BaricudaClose
	'm0128': 'GCodeDigitalOutput', # BaricudaOpen
	'm0129': 'GCodeDigitalOutput', # BaricudaClose
	'm0140': 'GCodeOtherModal', # SetBedTemperature
	'm0141': 'GCodeOtherModal', # SetChamberTemperature
	'm0143': 'GCodeCoolant', # SetLaserCoolerTemperature
	'm0145': 'GCodeOtherModal', # SetMaterialPreset
	'm0149': 'GCodeUnit', # SetTemperatureUnits
	'm0150': 'GCodeDigitalOutput', # SetRgbWColor
	'm0154': 'GCodeNonModal', # PositionAutoReport
	'm0155': 'GCodeNonModal', # TemperatureAutoReport
	'm0163': 'GCodeOtherModal', # SetMixFactor
	'm0164': 'GCodeOtherModal', # SaveMix
	'm0165': 'GCodeOtherModal', # SetMix
	'm0166': 'GCodeOtherModal', # GradientMix
	'm0190': 'GCode', # WaitForBedTemperature
	'm0191': 'GCode', # WaitForChamberTemperature
	'm0192': 'GCode', # WaitForProbeTemperature
	'm0193': 'GCodeCoolant', # SetLaserCoolerTemperature
	'm0200': 'GCodeOtherModal', # SetFilamentDiameter
	'm0201': 'GCodeNonModal', # PrintTravelMoveLimits
	'm0203': 'GCodeFeedRateMode', # SetMaxFeedrate
	'm0204': 'GCodeOtherModal', # SetStartingAcceleration
	'm0205': 'GCodeOtherModal', # SetAdvancedSettings
	'm0206': 'GCodeOtherModal', # SetHomeOffsets
	'm0207': 'GCodeOtherModal', # SetFirmwareRetraction
	'm0208': 'GCodeOtherModal', # FirmwareRecover
	'm0209': 'GCodeOtherModal', # SetAutoRetract
	'm0211': 'GCodeOtherModal', # SoftwareEndstops
	'm0217': 'GCodeOtherModal', # FilamentSwapParameters
	'm0218': 'GCodeOtherModal', # SetHotendOffset
	'm0220': 'GCodeFeedRateMode', # SetFeedratePercentage
	'm0221': 'GCodeOtherModal', # SetFlowPercentage
	'm0226': 'GCodeIO', # WaitForPinState
	'm0240': 'GCodeIO', # TriggerCamera
	'm0250': 'GCodeIO', # LcdContrast
	'm0255': 'GCodeIO', # LcdSleepBacklightTimeout
	'm0256': 'GCodeIO', # LcdBrightness
	'm0260': 'GCodeDigitalOutput', # ICSend
	'm0261': 'GCodeIO', # ICRequest
	'm0280': 'GCodeIO', # ServoPosition
	'm0281': 'GCodeOtherModal', # EditServoAngles
	'm0282': 'GCodeOtherModal', # DetachServo
	'm0290': 'GCodeMotion', # Babystep
	'm0300': 'GCodeDigitalOutput', # PlayTone
	'm0301': 'GCodeOtherModal', # SetHotendPid
	'm0302': 'GCodeOtherModal', # ColdExtrude
	'm0303': 'GCodeOtherModal', # PidAutotune
	'm0304': 'GCodeOtherModal', # SetBedPid
	'm0305': 'GCodeOtherModal', # UserThermistorParameters
	'm0306': 'GCodeOtherModal', # ModelPredictiveTempControl
	'm0350': 'GCodeOtherModal', # SetMicroStepping
	'm0351': 'GCodeOtherModal', # SetMicrostepPins
	'm0355': 'GCodeDigitalOutput', # CaseLightControl
	'm0360': 'GCodeMotion', # ScaraThetaA
	'm0361': 'GCodeMotion', # ScaraThetaB
	'm0362': 'GCodeMotion', # ScaraPsiA
	'm0363': 'GCodeMotion', # ScaraPsiB
	'm0364': 'GCodeMotion', # ScaraPsiC
	'm0380': 'GCodeDigitalOutput', # ActivateSolenoid
	'm0381': 'GCodeDigitalOutput', # DeactivateSolenoids
	'm0400': 'GCodeOtherModal', # FinishMoves
	'm0401': 'GCodeDigitalOutput', # DeployProbe
	'm0402': 'GCodeDigitalOutput', # StowProbe
	'm0403': 'GCodeOtherModal', # MmuFilamentType
	'm0404': 'GCodeOtherModal', # SetFilamentDiameter
	'm0405': 'GCodeOtherModal', # FilamentWidthSensorOn
	'm0406': 'GCodeOtherModal', # FilamentWidthSensorOff
	'm0407': 'GCodeNonModal', # FilamentWidth
	'm0410': 'GCodeOtherModal', # Quickstop
	'm0412': 'GCodeOtherModal', # FilamentRunout
	'm0413': 'GCodeOtherModal', # PowerLossRecovery
	'm0420': 'GCodeNonModal', # BedLevelingState
	'm0421': 'GCodeOtherModal', # SetMeshValue
	'm0422': 'GCodeOtherModal', # SetZMotorXy
	'm0423': 'GCodeOtherModal', # XTwistCompensation
	'm0425': 'GCodeOtherModal', # BacklashCompensation
	'm0428': 'GCodeOtherModal', # HomeOffsetsHere
	'm0430': 'GCodeOtherModal', # PowerMonitor
	'm0486': 'GCodeOtherModal', # CancelObjects
	'm0493': 'GCodeOtherModal', # FixedTimeMotion
	'm0500': 'GCodeNonModal', # SaveSettings
	'm0501': 'GCodeOtherModal', # RestoreSettings
	'm0502': 'GCodeOtherModal', # FactoryReset
	'm0503': 'GCodeNonModal', # ReportSettings
	'm0504': 'GCodeNonModal', # ValidateEepromContents
	'm0510': 'GCodeOtherModal', # LockMachine
	'm0511': 'GCodeOtherModal', # UnlockMachine
	'm0512': 'GCodeNonModal', # SetPasscode
	'm0524': 'GCodeOtherModal', # AbortSdPrint
	'm0540': 'GCodeNonModal', # EndstopsAbortSd
	'm0569': 'GCodeOtherModal', # SetTmcSteppingMode
	'm0575': 'GCodeOtherModal', # SerialBaudRate
	'm0592': 'GCodeOtherModal', # NonlinearExtrusionControl
	'm0593': 'GCodeOtherModal', # ZvInputShaping
	'm0600': 'GCode', # FilamentChange
	'm0603': 'GCodeOtherModal', # ConfigureFilamentChange
	'm0605': 'GCodeOtherModal', # MultiNozzleMode
	'm0665': 'GCodeOtherModal', # DeltaConfiguration
	'm0665b': 'GCodeOtherModal', # ScaraConfiguration
	'm0666b': 'GCodeOtherModal', # SetDualEndstopOffsets
	'm0666a': 'GCodeOtherModal', # SetDeltaEndstopAdjustments
	'm0672': 'GCodeOtherModal', # DuetSmartEffectorSensitivity
	'm0701': 'GCodeOtherModal', # LoadFilament
	'm0702': 'GCodeOtherModal', # UnloadFilament
	'm0710': 'GCodeOtherModal', # ControllerFanSettings
	'm7219': 'GCodeDigitalOutput', # MaxControl
	'm0808': 'GCodeOtherModal', # RepeatMarker
	'm0810': 'GCodeOtherModal', # GCodeMacros
	'm0851': 'GCodeOtherModal', # XyzProbeOffset
	'm0852': 'GCodeOtherModal', # BedSkewCompensation
	'm0860': 'GCodeOtherModal', # ICPositionEncoders
	'm0871': 'GCodeOtherModal', # ProbeTemperatureConfig
	'm0876': 'GCode', # HandlePromptResponse
	'm0900': 'GCodeOtherModal', # LinearAdvanceFactor
	'm0906': 'GCodeOtherModal', # StepperMotorCurrent
	'm0907': 'GCodeOtherModal', # SetMotorCurrent
	'm0908': 'GCodeOtherModal', # SetTrimpotPins
	'm0909': 'GCodeNonModal', # DacPrintValues
	'm0910': 'GCodeNonModal', # CommitDacToEeprom
	'm0911': 'GCode', # TmcOtPreWarnCondition
	'm0912': 'GCode', # ClearTmcOtPreWarn
	'm0913': 'GCodeOtherModal', # SetHybridThresholdSpeed
	'm0914': 'GCodeOtherModal', # TmcBumpSensitivity
	'm0915': 'GCode', # TmcZAxisCalibration
	'm0916': 'GCode', # LThermalWarningTest
	'm0917': 'GCode', # LOvercurrentWarningTest
	'm0918': 'GCode', # LSpeedWarningTest
	'm0919': 'GCodeOtherModal', # TmcChopperTiming
	'm0928': 'GCodeIO', # StartSdLogging
	'm0951': 'GCodeOtherModal', # MagneticParkingExtruder
	'm0993': 'GCodeIO', # BackUpFlashSettingsToSd
	'm0994': 'GCodeIO', # RestoreFlashFromSd
	'm0995': 'GCodeIO', # TouchScreenCalibration
	'm0997': 'GCode', # FirmwareUpdate
	'm0999': 'GCodeOtherModal', # StopRestart
	't0000': 'GCodeOtherModal', # SelectOrReportTool
	't0001': 'GCode', # MmuSpecialCommands
}

extra_attributes = {
    'g020': ['unit_id = 0'], # InchUnits
    'g021': ['unit_id = 1'], # MillimeterUnits
}

def sanitize(string):
    return ''.join([char if char in ascii_letters else '' for char in string])

def code_val(string):
    try:
        return int(string[1:])
    except ValueError:
        try:
            return float(string[1:])
        except ValueError:
            return string.strip("'")[1:]

def extract_data(filename):
    param_letters = []
    with open(filename,'r') as file:
        for line in file.readlines():
            comment = ''
            if line.startswith('tag: '):
                tag = line[5:].rstrip()
                name_suffix = ''
                try:
                    letter, code = line[5].upper(), int(line[6:].lstrip('0'))
                except ValueError as e:
                    try:
                        letter, code = line[5].upper(), line[6:].lstrip('0')
                        if code == '\n':    code = 0
                        else:               raise ValueError
                    except ValueError:
                        code = int(code[:-2].rstrip(ascii_letters))
                        comment = f"# NOTE: {line}"
                        name_suffix = line.rstrip('\n')[6:].replace(str(code), '').lstrip('0')
                code = int(code)
            elif line.startswith('title: '):
                title = line[7:].rstrip()
                class_name = sanitize(title.title())
            elif line.startswith('codes: '):
                codes = line[8:-2].replace(' ','').split(',')
            elif line.startswith('brief: '):
                brief = line.rstrip()[7:]
            elif line.startswith('- tag: '):
                param_letters.append(line[-2])

    #print(f"\t'{tag}': 'GCode', # {class_name}")
    out = ""

    out += f'''class {comment}GCode{class_name}{name_suffix}({class_types[tag]}):
    """{', '.join(codes)}: {brief}"""
    param_letters = "{''.join(param_letters)}"
    dialects = ['marlin2']
'''

    if len(codes) > 1:
        out += f'''
    @classmethod
    def word_matches(cls, w):
        return (w.letter == '{letter}') and (w.value in {[code_val(v) for v in codes]})
    default_word = Word('{letter}', {code})
'''
    else:
        out += f"    word_key = Word('{letter}', {code})\n"

    try:
        for extra_attr in extra_attributes[tag]:
            out += f"    {extra_attr}"
    except KeyError:
        pass

    return class_name, out



if __name__ == '__main__':
    from sys import argv, stderr
    all_classes = []

    print("# DO NOT EDIT - file generated with pygcode/src/pygcode/tools/marlin_parse_MarlinDocumentation.py\nfrom .gcodes_base import *\n")
    print("# TODO: manual changes have been made! see pygcode/src/pygcode/gcode_marlin.patch", file=stderr)

    for filename in argv[1:]:
        name, body = extract_data(filename)
        if name in all_classes:
            print(f"# TODO: duplicate class name GCode{name}", file=stderr)
            print(f"# TODO: duplicate class name GCode{name}")
            pass
        else:
            all_classes.append(name)
        print(body)

