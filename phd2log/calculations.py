#  Created byMartin.cz
# This code was inspired by original work of Andy Galasso.
# https://github.com/agalasso/phdlogview

import numpy
from .stats import Stats


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
    
    # init stats
    ra_stats = Stats()
    dec_stats = Stats()
    
    # init buffs
    ra_drift = 0
    last_ra_raw = 0
    last_ra_guide = 0
    
    # process points
    for point in points:
        
        # calc RA drift
        if point.ra_raw_distance is not None and point.ra_guide_distance is not None:
            drift = point.ra_raw_distance - last_ra_raw - last_ra_guide
            ra_drift += drift
            last_ra_raw = point.ra_raw_distance
            last_ra_guide = point.ra_guide_distance
            ra_stats.add(point.seconds, ra_drift)
            point.ra_drift = ra_drift
        
        # calc DEC drift
        if point.dec_raw_distance is not None:
            dec_stats.add(point.seconds, point.dec_raw_distance)
            point.dec_drift = point.dec_raw_distance
    
    # apply offset
    ra_a = ra_stats.a()
    ra_b = ra_stats.b()
    dec_a = dec_stats.a()
    dec_b = dec_stats.b()
    
    for point in points:
        if point.ra_drift is not None:
            point.ra_drift -= ra_a * point.seconds + ra_b
        if point.dec_drift is not None:
            point.dec_drift -= dec_a * point.seconds + dec_b


def calc_guiding_rms(points):
    """Calculates total RMS from given guiding points."""
    
    # get valid points
    points = [p for p in points if not p.rejected]
    if not points:
        return 0, 0, 0
        
    # add points to stats
    stats = Stats()
    for point in points:
        if point.ra_raw_distance is not None and point.dec_raw_distance is not None:
            stats.add(point.ra_raw_distance, point.dec_raw_distance)
    
    # get RMS
    rms_ra = numpy.sqrt(stats.var_x)
    rms_dec = numpy.sqrt(stats.var_y)
    rms_tot = numpy.sqrt(rms_ra*rms_ra + rms_dec*rms_dec)
    
    return float(rms_ra), float(rms_dec), float(rms_tot)
