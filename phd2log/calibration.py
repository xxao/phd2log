#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from datetime import datetime
from .constants import *


class CalibSession(object):
    """Holds calibration session info."""
    
    
    def __init__(self, line):
        """Initializes a new instance of CalibSession."""
        
        self.time = datetime.strptime(line.replace(LS_CALIB_BEGINS, ""), "%Y-%m-%d %H:%M:%S")
        self.points = []
    
    
    def __str__(self):
        """Returns string representation."""
        
        return f"Calibration - {self.time}"
    
    
    def add_point(self, point):
        """Adds new point into session."""
        
        self.points.append(point)


class CalibPoint(object):
    """Holds calibration point info."""
    
    
    def __init__(self, line):
        """Initializes a new instance of CalibPoint."""
        
        values = line.split(",")
        
        self.direction = values[0]
        self.step = int(values[1])
        self.dx = float(values[2])
        self.dy = float(values[3])
        self.x = float(values[4])
        self.y = float(values[5])
        self.distance = float(values[6])
