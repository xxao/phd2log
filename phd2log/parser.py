#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import re

from .constants import *
from .calibration import CalibSession, CalibPoint
from .guiding import GuideSession, GuidePoint, GuideInfo
from .calculations import calc_guiding_drifts, calc_guiding_rms


def parse_log(path):
    """Parses given PHD2 log."""
    
    # init sessions
    sessions = []
    
    # read lines
    with open(path, "r") as f:
        lines = iter(f.readlines())
    
    # parse lines
    for line in lines:
        
        # skip empty line
        line = line.strip()
        if not line:
            continue
        
        # parse calibration block
        if line.startswith(LS_CALIB_BEGINS):
            session = parse_calibration(lines, line)
            sessions.append(session)
            continue
        
        # parse guiding block
        if line.startswith(LS_GUIDING_BEGINS):
            session = parse_guiding(lines, line)
            sessions.append(session)
            continue
    
    return sessions


def parse_calibration(lines, line):
    """Parses calibration session data."""
    
    # init session
    session = CalibSession(line)
    
    # parse calibration lines
    for line in lines:
        
        # skip empty line
        line = line.strip()
        if not line:
            continue
        
        # calibration ends
        if line.startswith(LS_CALIB_ENDS):
            break
        
        # parse calibration points
        if any(line.startswith(d + ",") for d in CALIB_DIRS):
            point = CalibPoint(line)
            session.add_point(point)
            continue
    
    return session


def parse_guiding(lines, line):
    """Parses guiding session data."""
    
    # init session
    session = GuideSession(line)
    
    # init buffs
    is_guiding = False
    is_rejected = False
    
    # parse guiding lines
    for line in lines:
        
        # skip empty line
        line = line.strip()
        if not line:
            continue
        
        # guiding ends
        if line.startswith(LS_GUIDING_ENDS):
            break
        if line.startswith(LS_LOG_CLOSED):
            break
        
        # guiding starts
        if line.startswith(LS_GUIDING_HEAD):
            is_guiding = True
            continue
        
        # set rejection
        if line.startswith(LS_INFO_SETTLING_BEGINS):
            is_rejected = True
        elif line.startswith(LS_INFO_SETTLING):
            is_rejected = False
        
        # get info
        if line.startswith(LS_INFO):
            info = GuideInfo(line)
            session.add_info(info)
            continue
        
        # parse guiding point
        if is_guiding:
            point = GuidePoint(line)
            session.add_point(point)
            point.rejected = point.rejected or is_rejected
            continue
        
        # add settings
        session.settings += line + "\n"
        
        # parse main settings
        if line.startswith(LS_GUIDING_SCALE):
            session.pixel_scale = extract_float_param(line, GUIDING_SCALE)
        
        elif line.startswith(LS_GUIDING_EXPOSURE):
            session.exposure = extract_float_param(line, GUIDING_EXPOSURE)
        
        elif line.startswith(LS_GUIDING_X):
            session.x_min_move = extract_float_param(line, GUIDING_MIMO)
        
        elif line.startswith(LS_GUIDING_Y):
            session.y_min_move = extract_float_param(line, GUIDING_MIMO)
    
    # calc drifts
    calc_guiding_drifts(session.points)
    
    # calc global RMS
    rms = calc_guiding_rms(session.points)
    session.ra_rms = rms[0]
    session.dec_rms = rms[1]
    session.tot_rms = rms[2]
    
    return session


def extract_float_param(line, key):
    """Extracts parameter value from given line."""
    
    # init expression
    expr = f"{key} = ([0-9]+(?:\\.[0-9]+)?)\\s?(%?[a-z]*)?"
    
    # search text
    match = re.search(expr, line)
    if not match:
        return None
    
    # convert value to float
    value = float(match.group(1))
    
    # convert percentage
    if match.group(2) == "%":
        value /= 100
    
    # convert milliseconds
    elif match.group(2) == "ms":
        value /= 1e3
    
    # convert microseconds
    elif match.group(2) == "us":
        value /= 1e6
    
    return value
