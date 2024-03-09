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
	'g002': 'GCodeArcMove', # GCodeMotion > ArcOrCircleMove
	'g004': 'GCode', # Dwell
	'g005': 'GCodeMotion', # BezierCubicSpline
	'g006': 'GCodeMotion', # DirectStepperMove
	'g010': 'GCodeMachineRoutines', # Retract
	'g011': 'GCodeMachineRoutines', # Recover
	'g012': 'GCodeMachineRoutines', # CleanTheNozzle
	'g017': 'GCodePlaneSelect', # CncWorkspacePlanes
	'g020': 'GCodeUnit', # InchUnits
	'g021': 'GCodeUnit', # MillimeterUnits
	'g026': 'GCodeAssistedRoutines', # MeshValidationPattern
	'g027': 'GCodeMachineRoutines', # ParkToolhead
	'g028': 'GCodeMachineRoutines', # AutoHome
	'g029': 'GCodeMachineRoutines', # BedLeveling
	'g029g1': 'GCodeMachineRoutines', # BedLevelingPoint
	'g029m2': 'GCodeMachineRoutines', # BedLevelingBilinear
	'g029g2': 'GCodeMachineRoutines', # BedLevelingLinear
	'g029m1': 'GCodeMachineRoutines', # BedLevelingManual
	'g029m3': 'GCodeMachineRoutines', # BedLevelingUnified
	'g030': 'GCodeMachineRoutines', # SingleZProbe
	'g031': 'GCodeMachineRoutines', # DockSled
	'g032': 'GCodeMachineRoutines', # UndockSled
	'g033': 'GCodeMachineRoutines', # DeltaAutoCalibration
	'g034b': 'GCodeMachineRoutines', # MechanicalGantryCalibration
	'g034a': 'GCodeMachineRoutines', # ZSteppersAutoAlignment
	'g035': 'GCodeAssistedRoutines', # TrammingAssistant
	'g038': 'GCodeMachineRoutines', # ProbeTarget
	'g042': 'GCodeMotion', # MoveToMeshCoordinate
	'g053': 'GCodeMotion', # MoveInMachineCoordinates
	'g054': 'GCodeSelectCoordinateSystem', # WorkspaceCoordinateSystem
	'g060': 'GCodeOtherModal', # SaveCurrentPosition
	'g061': 'GCodeMotion', # ReturnToSavedPosition
	'g076': 'GCodeMachineRoutines', # ProbeTemperatureCalibration
	'g080': 'GCodeOtherModal', # CancelCurrentMotionMode
	'g090': 'GCodeOtherModal', # AbsolutePositioning
	'g091': 'GCodeOtherModal', # RelativePositioning
	'g092': 'GCodeOtherModal', # SetPosition
	'g425': 'GCodeMachineRoutines', # BacklashCalibration
	'm0000': 'GCodeProgramControl', # UnconditionalStop
	'm0003': 'GCodeToolState', # SpindleCwLaserOn
	'm0004': 'GCodeToolState', # SpindleCcwLaserOn
	'm0005': 'GCodeToolState', # SpindleLaserOff
	'm0007': 'GCodeCoolantHeaters', # CoolantControls
	'm0010': 'GCodeIO', # VacuumBlowerControl
	'm0016': 'GCodeOtherModal', # ExpectedPrinterCheck
	'm0017': 'GCodeOtherModal', # EnableSteppers
	'm0018': 'GCodeOtherModal', # DisableSteppers
	'm0020': 'GCodeIO', # ListSdCard
	'm0021': 'GCodeIO', # InitSdCard
	'm0022': 'GCodeIO', # ReleaseSdCard
	'm0023': 'GCodeIO', # SelectSdFile
	'm0024': 'GCodeProgramControl', # StartOrResumeSdPrint
	'm0025': 'GCodeProgramControl', # PauseSdPrint
	'm0026': 'GCodeProgramControl', # SetSdPosition
	'm0027': 'GCodeMachineState', # ReportSdPrintStatus
	'm0028': 'GCodeIO', # StartSdWrite
	'm0029': 'GCodeIO', # StopSdWrite
	'm0030': 'GCodeIO', # DeleteSdFile
	'm0031': 'GCodeMachineState', # ReportPrintTime
	'm0032': 'GCodeProgramControl', # SelectAndStart
	'm0033': 'GCodeIO', # GetLongPath
	'm0034': 'GCodeIO', # SdcardSorting
	'm0042': 'GCodeIO', # SetPinState
	'm0043': 'GCodeIO', # DebugPins
	'm0043b': 'GCodeIO', # TogglePins
	'm0048': 'GCodeMachineRoutines', # ProbeRepeatabilityTest
	'm0073': 'GCodeNonModal', # SetPrintProgress
	'm0075': 'GCodeProgramControl', # StartPrintJobTimer
	'm0076': 'GCodeProgramControl', # PausePrintJobTimer
	'm0077': 'GCodeProgramControl', # StopPrintJobTimer
	'm0078': 'GCodeMachineState', # PrintJobStats
	'm0080': 'GCodeOtherModal', # PowerOn
	'm0081': 'GCodeOtherModal', # PowerOff
	'm0082': 'GCodeOtherModal', # EAbsolute
	'm0083': 'GCodeOtherModal', # ERelative
	'm0085': 'GCodeOtherModal', # InactivityShutdown
	'm0086': 'GCodeOtherModal', # HotendIdleTimeout
	'm0087': 'GCodeOtherModal', # DisableHotendIdleTimeout
	'm0092': 'GCodeOtherModal', # SetAxisStepsPerUnit
	'm0100': 'GCodeMachineState', # FreeMemory
	'm0102': 'GCodeMachineRoutines', # ConfigureBedDistanceSensor
	'm0104': 'GCodeToolState', # SetHotendTemperature
	'm0105': 'GCodeMachineState', # ReportTemperatures
	'm0106': 'GCodeCoolantHeaters', # SetFanSpeed
	'm0107': 'GCodeCoolantHeaters', # FanOff
	'm0108': 'GCodeProgramControl', # BreakAndContinue
	'm0109': 'GCodeToolState', # WaitForHotendTemperature
	'm0110': 'GCodeOtherModal', # SetLineNumber
	'm0111': 'GCodeOtherModal', # DebugLevel
	'm0112': 'GCodeOtherModal', # FullShutdown
	'm0113': 'GCodeMachineState', # HostKeepalive
	'm0114': 'GCodeMachineState', # GetCurrentPosition
	'm0115': 'GCodeMachineState', # FirmwareInfo
	'm0117': 'GCodeMachineState', # SetLcdMessage
	'm0118': 'GCodeMachineState', # SerialPrint
	'm0119': 'GCodeMachineState', # EndstopStates
	'm0120': 'GCodeOtherModal', # EnableEndstops
	'm0121': 'GCodeOtherModal', # DisableEndstops
	'm0122': 'GCodeMachineState', # TmcDebugging
	'm0123': 'GCodeMachineState', # FanTachometers
	'm0125': 'GCodeMachineRoutines', # ParkHead
	'm0126': 'GCodeDigitalOutput', # Baricuda1Open
	'm0127': 'GCodeDigitalOutput', # Baricuda1Close
	'm0128': 'GCodeDigitalOutput', # Baricuda2Open
	'm0129': 'GCodeDigitalOutput', # Baricuda2Close
	'm0140': 'GCodeCoolantHeaters', # SetBedTemperature
	'm0141': 'GCodeCoolantHeaters', # SetChamberTemperature
	'm0143': 'GCodeCoolantHeaters', # SetLaserCoolerTemperature
	'm0145': 'GCodeNonModal', # SetMaterialPreset
	'm0149': 'GCodeUnit', # SetTemperatureUnits
	'm0150': 'GCodeDigitalOutput', # SetRgbWColor
	'm0154': 'GCodeNonModal', # PositionAutoReport
	'm0155': 'GCodeMachineState', # TemperatureAutoReport
	'm0163': 'GCodeOtherModal', # SetMixFactor
	'm0164': 'GCodeOtherModal', # SaveMix
	'm0165': 'GCodeOtherModal', # SetMix
	'm0166': 'GCodeOtherModal', # GradientMix
	'm0190': 'GCodeCoolantHeaters', # WaitForBedTemperature
	'm0191': 'GCodeCoolantHeaters', # WaitForChamberTemperature
	'm0192': 'GCodeToolState', # WaitForProbeTemperature
	'm0193': 'GCodeCoolantHeaters', # SetLaserCoolerTemperature
	'm0200': 'GCodeOtherModal', # SetFilamentDiameter
	'm0201': 'GCodePathControlMode', # PrintTravelMoveLimits
	'm0203': 'GCodePathControlMode', # SetMaxFeedrate
	'm0204': 'GCodePathControlMode', # SetStartingAcceleration
	'm0205': 'GCodePathControlMode', # SetAdvancedSettings
	'm0206': 'GCodeMachineConfig', # SetHomeOffsets
	'm0207': 'GCodeMachineConfig', # FirmwareRetractionSettings
	'm0208': 'GCodeMachineConfig', # FirmwareRecoverSettings
	'm0209': 'GCodeMachineConfig', # SetAutoRetract
	'm0211': 'GCodeOtherModal', # SoftwareEndstops
	'm0217': 'GCodeMachineConfig', # FilamentSwapParameters
	'm0218': 'GCodeToolGeometry', # SetHotendOffset
	'm0220': 'GCodeFeedRateMode', # SetFeedratePercentage
	'm0221': 'GCodeFeedRateMode', # SetFlowPercentage
	'm0226': 'GCodeIO', # WaitForPinState
	'm0240': 'GCodeDigitalOutput', # TriggerCamera
	'm0250': 'GCodeDigitalOutput', # LcdContrast
	'm0255': 'GCodeDigitalOutput', # LcdSleepBacklightTimeout
	'm0256': 'GCodeDigitalOutput', # LcdBrightness
	'm0260': 'GCodeIO', # I2CSend
	'm0261': 'GCodeIO', # I2CRequest
	'm0280': 'GCodeIO', # ServoPosition
	'm0281': 'GCodeIO', # EditServoAngles
	'm0282': 'GCodeIO', # DetachServo
	'm0290': 'GCodeMotion', # Babystep
	'm0300': 'GCodeDigitalOutput', # PlayTone
	'm0301': 'GCodeMachineConfig', # SetHotendPid
	'm0302': 'GCodeOtherModal', # ColdExtrude
	'm0303': 'GCodeCalibrationRoutines', # PidAutotune
	'm0304': 'GCodeMachineConfig', # SetBedPid
	'm0305': 'GCodeMachineConfig', # UserThermistorParameters
	'm0306': 'GCodeMachineConfig', # ModelPredictiveTempControl
	'm0350': 'GCodeMachineConfig', # SetMicroStepping
	'm0351': 'GCodeMachineConfig', # SetMicrostepPins
	'm0355': 'GCodeDigitalOutput', # CaseLightControl
	'm0360': 'GCodeCalibrationRoutines', # ScaraThetaA
	'm0361': 'GCodeCalibrationRoutines', # ScaraThetaB
	'm0362': 'GCodeCalibrationRoutines', # ScaraPsiA
	'm0363': 'GCodeCalibrationRoutines', # ScaraPsiB
	'm0364': 'GCodeCalibrationRoutines', # ScaraPsiC
	'm0380': 'GCodeDigitalOutput', # ActivateSolenoid
	'm0381': 'GCodeDigitalOutput', # DeactivateSolenoids
	'm0400': 'GCodeNonModal', # FinishMoves
	'm0401': 'GCodeDigitalOutput', # DeployProbe
	'm0402': 'GCodeDigitalOutput', # StowProbe
	'm0403': 'GCodeMachineConfig', # Mmu2FilamentType
	'm0404': 'GCodeMachineConfig', # SetFilamentDiameter
	'm0405': 'GCodeMachineConfig', # FilamentWidthSensorOn
	'm0406': 'GCodeMachineConfig', # FilamentWidthSensorOff
	'm0407': 'GCodeMachineConfig', # FilamentWidth
	'm0410': 'GCodeProgramControl', # Quickstop
	'm0412': 'GCodeMachineConfig', # FilamentRunout
	'm0413': 'GCodeMachineConfig', # PowerLossRecovery
	'm0420': 'GCodeMachineConfig', # BedLevelingState
	'm0421': 'GCodeMachineConfig', # SetMeshValue
	'm0422': 'GCodeMachineConfig', # SetZMotorXy
	'm0423': 'GCodeMachineConfig', # XTwistCompensation
	'm0425': 'GCodeMachineConfig', # BacklashCompensation
	'm0428': 'GCodeMachineConfig', # HomeOffsetsHere
	'm0430': 'GCodeNonModal', # PowerMonitor
	'm0486': 'GCodeProgramControl', # CancelObjects
	'm0493': 'GCodePathControlMode', # FixedTimeMotion
	'm0500': 'GCodeMachineConfig', # SaveSettings
	'm0501': 'GCodeMachineConfig', # RestoreSettings
	'm0502': 'GCodeMachineConfig', # FactoryReset
	'm0503': 'GCodeMachineConfig', # ReportSettings
	'm0504': 'GCodeNonModal', # ValidateEepromContents
	'm0510': 'GCodeOtherModal', # LockMachine
	'm0511': 'GCodeOtherModal', # UnlockMachine
	'm0512': 'GCodeMachineConfig', # SetPasscode
	'm0524': 'GCodeProgramControl', # AbortSdPrint
	'm0540': 'GCodeMachineConfig', # EndstopsAbortSd
	'm0569': 'GCodeMachineConfig', # SetTmcSteppingMode
	'm0575': 'GCodeMachineConfig', # SerialBaudRate
	'm0592': 'GCodeMachineConfig', # NonlinearExtrusionControl
	'm0593': 'GCodeCalibrationRoutines', # ZvInputShaping
	'm0600': 'GCodeMachineRoutines', # FilamentChange
	'm0603': 'GCodeMachineConfig', # ConfigureFilamentChange
	'm0605': 'GCodeMachineConfig', # MultiNozzleMode
	'm0665': 'GCodeMachineConfig', # DeltaConfiguration
	'm0665b': 'GCodeMachineConfig', # ScaraConfiguration
	'm0666b': 'GCodeMachineConfig', # SetDualEndstopOffsets
	'm0666a': 'GCodeMachineConfig', # SetDeltaEndstopAdjustments
	'm0672': 'GCodeMachineConfig', # DuetSmartEffectorSensitivity
	'm0701': 'GCodeMachineRoutines', # LoadFilament
	'm0702': 'GCodeMachineRoutines', # UnloadFilament
	'm0710': 'GCodeMachineConfig', # ControllerFanSettings
	'm7219': 'GCodeDigitalOutput', # MAX7219Control
	'm0808': 'GCodeProgramControl', # RepeatMarker
	'm0810': 'GCodeProgramControl', # GCodeMacros
	'm0851': 'GCodeToolGeometry', # XyzProbeOffset
	'm0852': 'GCodeMachineConfig', # BedSkewCompensation
	'm0860': 'GCodeMachineConfig', # I2CPositionEncoders
	'm0871': 'GCodeMachineConfig', # ProbeTemperatureConfig
	'm0876': 'GCodeMachineConfig', # HandlePromptResponse
	'm0900': 'GCodeMachineConfig', # LinearAdvanceFactor
	'm0906': 'GCodeMachineConfig', # TrinamicStepperMotorCurrent
	'm0907': 'GCodeMachineConfig', # TrimpotStepperMotorCurrent
	'm0908': 'GCodeMachineConfig', # SetTrimpotPins
	'm0909': 'GCodeMachineState', # ReportDacStepperCurrent
	'm0910': 'GCodeMachineState', # CommitDacToEeprom
	'm0911': 'GCodeMachineState', # TmcOtPreWarnCondition
	'm0912': 'GCodeMachineState', # ClearTmcOtPreWarn
	'm0913': 'GCodeMachineConfig', # SetHybridThresholdSpeed
	'm0914': 'GCodeMachineConfig', # TmcBumpSensitivity
	'm0915': 'GCodeCalibrationRoutines', # TmcZAxisCalibration
	'm0916': 'GCodeCalibrationRoutines', # L6474ThermalWarningTest
	'm0917': 'GCodeCalibrationRoutines', # L6474OvercurrentWarningTest
	'm0918': 'GCodeCalibrationRoutines', # L6474SpeedWarningTest
	'm0919': 'GCodeMachineConfig', # TmcChopperTiming
	'm0928': 'GCodeIO', # StartSdLogging
	'm0951': 'GCodeMachineConfig', # MagneticParkingExtruder
	'm0993': 'GCodeIO', # BackUpFlashSettingsToSd
	'm0994': 'GCodeIO', # RestoreFlashFromSd
	'm0995': 'GCodeIO', # TouchScreenCalibration
	'm0997': 'GCodeMachineConfig', # FirmwareUpdate
	'm0999': 'GCodeOtherModal', # StopRestart
	't0000': 'GCodeOtherModal', # SelectOrReportTool
	't0001': 'GCodeOtherModal', # MmuSpecialCommands
}

extra_attributes = {
    'g020': ['unit_id = 0'], # InchUnits
    'g021': ['unit_id = 1'], # MillimeterUnits
}

valid_chars = ascii_letters + '_' + ''.join(str(i) for i in range(10))

def sanitize(string):
    """ clean a string so it's suitable to act as a class name
    NOTE: does not replace accented characters by their closest equivalent """
    x = lambda w: w[0].upper() + w[1:]
    return ''.join([char if char in valid_chars else '' for char in ''.join([x(word) for word in string.split(' ')])])

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
                class_name = sanitize(title)
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
    print("# NOTE: it is likely manual changes have been made to the previous output! see pygcode/src/pygcode/gcode_marlin.patch", file=stderr)

    for filename in argv[1:]:
        name, body = extract_data(filename)
        if name in all_classes:
            print(f"# TODO: duplicate class name GCode{name}", file=stderr)
            print(f"# TODO: duplicate class name GCode{name}")
            pass
        else:
            all_classes.append(name)
        print(body)

