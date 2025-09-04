#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# log starts
LS_LOG_CLOSED = "Log closed at"

# calibration line starts
LS_CALIB_BEGINS = "Calibration Begins at "
LS_CALIB_ENDS = "Calibration complete"
LS_CALIB_HEAD = "Direction,Step,dx,dy,x,y,Dist"

# guiding line starts
LS_GUIDING_BEGINS = "Guiding Begins at "
LS_GUIDING_ENDS = "Guiding Ends"
LS_GUIDING_HEAD = "Frame,Time,mount"
LS_GUIDING_SCALE = "Pixel scale"
LS_GUIDING_EXPOSURE = "Exposure"
LS_GUIDING_X = "X guide"
LS_GUIDING_Y = "Y guide"

# info line starts
LS_INFO = "INFO: "
LS_INFO_LOCK = "INFO: SET LOCK POSITION, new lock pos = "
LS_INFO_SETTLING = "INFO: SETTLING STATE CHANGE, "
LS_INFO_SETTLING_BEGINS = "INFO: SETTLING STATE CHANGE, Settling started"
LS_INFO_DITHER = "INFO: DITHER by "
LS_INFO_PARAM_CHANGED = "INFO: Guiding parameter change, "

# guiding params
GUIDING_SCALE = "Pixel scale"
GUIDING_EXPOSURE = "Exposure"
GUIDING_MIMO = "Minimum move"

# calibration directions
CALIB_DIR_NORTH = "North"
CALIB_DIR_SOUTH = "South"
CALIB_DIR_WEST = "West"
CALIB_DIR_EAST = "East"
CALIB_DIR_BACKLASH = "Backlash"

CALIB_DIRS = (
    CALIB_DIR_NORTH,
    CALIB_DIR_SOUTH,
    CALIB_DIR_WEST,
    CALIB_DIR_EAST,
    CALIB_DIR_BACKLASH)

# info categories
INFO_CAT_SETTLING = "Settling"
INFO_CAT_DITHER = "Dither"
INFO_CAT_LOCK = "Lock"
INFO_CAT_PARAM = "Parameter"
INFO_CAT_ERROR = "Error"

# units
UNITS_PX = "px"
UNITS_ARCSEC = "arc-sec"

# guide errors
GUIDE_ERRORS = {
    0: None,
    1: "Star saturated",
    2: "Star has low SNR",
    3: "Star has low mass",
    4: "Star has low HFD",
    5: "Star has high HFD",
    6: "Star drifted",
    7: "Star mass changed",
    8: "Unexpected error",
}
