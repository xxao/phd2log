#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy


def calc_guiding_drifts(points):
    """Calculates and assigns drifts to given guiding points."""
    
    # reset points
    for point in points:
        point.ra_drift = None
        point.dec_drift = None
    
    # get valid points
    points = [p for p in points if not p.rejected]
    if not points:
        return
    
    # init buffs
    degree = 2
    last_ra_drift = 0
    last_ra_raw = 0
    last_ra_guide = 0
    
    # process points
    for point in points:
        
        # calc RA drift
        point.ra_drift = point.ra_raw_distance + (last_ra_drift - last_ra_raw - last_ra_guide)
        last_ra_drift = point.ra_drift
        last_ra_raw = point.ra_raw_distance
        last_ra_guide = point.ra_guide_distance
        
        # calc DEC drift
        point.dec_drift = point.dec_raw_distance
    
    # fit data to polynomial for better view
    x = numpy.array([p.seconds for p in points])
    ra = numpy.array([p.ra_drift for p in points])
    dec = numpy.array([p.dec_drift for p in points])
    ra_fit = numpy.polynomial.polynomial.Polynomial.fit(x, ra, degree)
    dec_fit = numpy.polynomial.polynomial.Polynomial.fit(x, dec, degree)
    
    # apply shift
    for point in points:
        point.ra_drift -= ra_fit(point.seconds)
        point.dec_drift -= dec_fit(point.seconds)


def calc_guiding_rms(points):
    """Calculates RMS from given guiding points."""
    
    # get valid points
    points = [p for p in points if not p.rejected]
    if not points:
        return 0, 0, 0
    
    # calc RA rms
    ra = numpy.array([p.ra_raw_distance for p in points])
    var_ra = numpy.var(ra, ddof=0)
    rms_ra = numpy.sqrt(var_ra)
    
    # calc DEC rms
    dec = numpy.array([p.dec_raw_distance for p in points])
    var_dec = numpy.var(dec, ddof=0)
    rms_dec = numpy.sqrt(var_dec)
    
    # calc total rms
    rms_tot = numpy.sqrt(rms_ra*rms_ra + rms_dec*rms_dec)
    
    return float(rms_ra), float(rms_dec), float(rms_tot)
