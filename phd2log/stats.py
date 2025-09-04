#  Created byMartin.cz
# This code was inspired by original work of Andy Galasso.
# https://github.com/agalasso/phdlogview

import numpy


class Stats(object):
    """Calculates basic data statistics."""
    
    
    def __init__(self):
        """Initializes a new instance of Stats."""
        
        self.avg_x = 0.0
        self.avg_y = 0.0
        self.var_x = 0.0
        self.var_y = 0.0
        self.cov_xy = 0.0
        self.n = 0
    
    
    def add(self, x, y):
        """Adds session point."""
        
        k = self.n
        self.n += 1
        k /= self.n
        
        dx = x - self.avg_x
        dy = y - self.avg_y
        
        self.var_x += (k * dx * dx - self.var_x) / self.n
        self.var_y += (k * dy * dy - self.var_y) / self.n
        self.cov_xy += (k * dx * dy - self.cov_xy) / self.n
        self.avg_x += dx / self.n
        self.avg_y += dy / self.n
    
    
    def a(self):
        """Calculates line a factor of y = ax + b."""
        
        if self.n < 2:
            return 0
        
        return self.cov_xy / self.var_x
    
    
    def b(self):
        """Calculates line b factor of y = ax + b."""
        
        return self.avg_y - self.a() * self.avg_x
    
    
    def theta(self):
        """Calculates line theta."""
        
        if self.n < 2:
            return 0
        
        return numpy.atan2(self.cov_xy, self.var_x)
