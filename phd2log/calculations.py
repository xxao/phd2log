#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy


def calc_guiding_drifts(points):
    """Calculates and assigns drifts to given guiding points."""
    
    # reset points
    for point in points:
        point.ra_drift = None
        point.dec_drift = None
    
    # init buffs
    degree = 2
    ra_points = []
    dec_points = []
    last_ra_drift = 0
    last_ra_raw = 0
    last_ra_guide = 0
    
    # process points
    for point in points:
        
        # skip rejected
        if point.rejected:
            continue
        
        # calc RA drift
        if point.ra_raw_distance is not None and point.ra_guide_distance is not None:
            point.ra_drift = point.ra_raw_distance + (last_ra_drift - last_ra_raw - last_ra_guide)
            last_ra_drift = point.ra_drift
            last_ra_raw = point.ra_raw_distance
            last_ra_guide = point.ra_guide_distance
            ra_points.append(point)
        
        # calc DEC drift
        if point.dec_raw_distance is not None:
            point.dec_drift = point.dec_raw_distance
            dec_points.append(point)
    
    # fit RA data to polynomial for better view
    if ra_points:
        x = numpy.array([p.seconds for p in ra_points])
        y = numpy.array([p.ra_drift for p in ra_points])
        fit = numpy.polynomial.polynomial.Polynomial.fit(x, y, degree)
        for point in ra_points:
            point.ra_drift -= fit(point.seconds)
    
    # fit DEC to polynomial for better view
    if dec_points:
        x = numpy.array([p.seconds for p in dec_points])
        y = numpy.array([p.dec_drift for p in dec_points])
        fit = numpy.polynomial.polynomial.Polynomial.fit(x, y, degree)
        for point in dec_points:
            point.dec_drift -= fit(point.seconds)


def calc_guiding_rms(points):
    """Calculates RMS from given guiding points."""
    
    # init buffs
    rms_ra = 0
    rms_dec = 0
    ra_points = []
    dec_points = []
    
    # get points
    for point in points:
        if point.rejected:
            continue
        if point.ra_raw_distance is not None:
            ra_points.append(point)
        if point.dec_raw_distance is not None:
            dec_points.append(point)
    
    # calc RA rms
    if ra_points:
        y = numpy.array([p.ra_raw_distance for p in ra_points])
        var_y = numpy.var(y, ddof=0)
        rms_ra = numpy.sqrt(var_y)
    
    # calc DEC rms
    if dec_points:
        y = numpy.array([p.dec_raw_distance for p in dec_points])
        var_y = numpy.var(y, ddof=0)
        rms_dec = numpy.sqrt(var_y)
    
    # calc total rms
    rms_tot = numpy.sqrt(rms_ra*rms_ra + rms_dec*rms_dec)
    
    return float(rms_ra), float(rms_dec), float(rms_tot)
