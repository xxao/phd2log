#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from datetime import datetime, timedelta
from .constants import *


class GuideSession(object):
    """Holds guiding session info."""
    
    
    def __init__(self, line):
        """Initializes a new instance of GuideSession."""
        
        self.time = datetime.strptime(line.replace(LS_GUIDING_BEGINS, ""), "%Y-%m-%d %H:%M:%S")
        
        self.entries = []
        self.info = []
        self.points = []
        
        self.settings = ""
        
        self.exposure = None
        self.pixel_scale = None
        self.x_min_move = None
        self.y_min_move = None
        
        self.ra_rms = None
        self.dec_rms = None
        self.tot_rms = None
    
    
    def __str__(self):
        """Returns string representation."""
        
        # format length
        seconds = self.length
        hours = seconds // 3600
        seconds = seconds % 3600
        minutes = seconds // 60
        seconds = seconds % 60
        
        # get RMS
        rms_px = self.tot_rms
        rms_arcsec = self.tot_rms * self.pixel_scale
        
        return f"Guiding - {self.time} | {hours:.0f}h {minutes:.0f}m {seconds:.0f}s | rms {rms_arcsec:.2f}\" ({rms_px:.2f}px) "
    
    
    def add_info(self, point):
        """Adds new info into session."""
        
        # add point
        self.entries.append(point)
        self.info.append(point)
        
        # set default time
        if len(self.entries) == 1:
            point.time = self.time
            point.stamp = point.time.timestamp()
        else:
            last = self.entries[-2]
            point.frame = last.frame
            point.seconds = last.seconds
            point.time = self.time + timedelta(seconds=last.seconds)
            point.stamp = point.time.timestamp()
    
    
    def add_point(self, point):
        """Adds new point into session."""
        
        # add point
        self.entries.append(point)
        self.points.append(point)
        
        # set time and scale
        point.time = self.time + timedelta(seconds=point.seconds)
        point.stamp = point.time.timestamp()
        point.scale = self.pixel_scale
        
        # get previous info points
        i = -1
        while len(self.entries) + i > 0 and isinstance(self.entries[i-1], GuideInfo):
            i -= 1
        
        # adjust time
        f = 1 / (abs(i+1)+1)
        for d, info in enumerate(self.entries[i:-1]):
            info.frame += (d+1) * f
            info.seconds += (d+1) * f * (point.seconds - info.seconds)
            info.time = self.time + timedelta(seconds=info.seconds)
            info.stamp = info.time.timestamp()
    
    
    @property
    def length(self):
        """Gets total length of the session in seconds."""
        
        return self.points[-1].seconds - self.points[0].seconds


class GuidePoint(object):
    """Holds guiding point info."""
    
    
    def __init__(self, line):
        """Initializes a new instance of Guiding."""
        
        values = line.split(",")
        
        self.line = line
        self.frame = int(values[0])
        self.seconds = float(values[1])
        self.time = None
        self.stamp = None
        
        self.mount = values[2].replace('"', "")
        self.dx = float(values[3]) if values[3] else None
        self.dy = float(values[4]) if values[4] else None
        self.ra_raw_distance = float(values[5]) if values[5] else None
        self.dec_raw_distance = float(values[6]) if values[6] else None
        self.ra_guide_distance = float(values[7]) if values[7] else None
        self.dec_guide_distance = float(values[8]) if values[8] else None
        self.ra_duration = int(values[9]) if values[9] else None
        self.ra_direction = values[10] if values[10] else None
        self.dec_duration = int(values[11]) if values[11] else None
        self.dec_direction = values[12] if values[12] else None
        self.x_step = float(values[13]) if values[13] else None
        self.y_step = float(values[14]) if values[14] else None
        self.star_mass = int(values[15])
        self.star_snr = float(values[16])
        
        self.error_code = int(values[17])
        self.error_info = GUIDE_ERRORS.get(self.error_code, None)
        
        self.rejected = False
        self.ra_drift = 0
        self.dec_drift = 0


class GuideInfo(object):
    """Holds guiding info message."""
    
    
    def __init__(self, line):
        """Initializes a new instance of GuideInfo."""
        
        self.line = line
        self.frame = 0
        self.seconds = 0
        self.time = 0
        self.stamp = None
        
        self.category = None
        self.value = None
        
        # settling
        if line.startswith(LS_INFO_SETTLING):
            self.category = INFO_CAT_SETTLING
            self.value = line.replace(LS_INFO_SETTLING, "")
        
        # dither
        elif line.startswith(LS_INFO_DITHER):
            self.category = INFO_CAT_DITHER
            coords = line.replace(LS_INFO_DITHER, "").split(",")
            self.value = f"{coords[0].strip()}, {coords[1].strip()}"
        
        # lock
        elif line.startswith(LS_INFO_LOCK):
            self.category = INFO_CAT_LOCK
            coords = line.replace(LS_INFO_LOCK, "").split(",")
            self.value = f"{coords[0].strip()}, {coords[1].strip()}"
        
        # param
        elif line.startswith(LS_INFO_PARAM_CHANGED):
            self.category = INFO_CAT_PARAM
            self.value = line.replace(LS_INFO_PARAM_CHANGED, "")
        
        else:
            print(line)
