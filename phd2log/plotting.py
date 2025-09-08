#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import datetime
import pero
import perrot
import numpy

from .constants import *
from .icons import *
from .import style


def make_guide_button(icon, **overrides):
    """Makes session button."""
    
    # init path
    path = pero.Path.from_svg(icon)
    
    # init symbol
    symbol = pero.Symbol(
        path = path,
        size = 12,
        fill_color = style.BUTTON_TEXT,
        line_color = None)
    
    # init box
    box = pero.Box(
        graphics = symbol,
        v_align = pero.CENTER,
        h_align = pero.CENTER,
        fill_color = style.BUTTON_BGR,
        line_color = style.AXES_LINE,
        padding = 0,
        **overrides)
    
    return box


def make_guide_session_text(**overrides):
    """Makes text block for guide session info."""
    
    # init text
    text = pero.Text(
        font_size = 14,
        text_color = style.AXES_TEXT,
        text_align = pero.LEFT,
        text_base = pero.MIDDLE)
    
    # init box
    box = pero.Box(
        tag = "guide_session",
        graphics = text,
        radius = 0,
        v_align = pero.CENTER,
        fill_color = style.TEXT_BGR,
        line_color = style.AXES_LINE,
        padding = (0, 10),
        **overrides)
    
    return box


def make_guide_rms_text(**overrides):
    """Makes text block for guide RMS info."""
    
    # init text
    text = pero.Text(
        font_size = 14,
        text_color = style.AXES_TEXT,
        text_align = pero.LEFT,
        text_base = pero.MIDDLE)
    
    # init box
    box = pero.Box(
        tag = "guide_rms",
        graphics = text,
        x = style.PLOT_SPACING,
        radius = (6, 0, 0, 6),
        v_align = pero.CENTER,
        fill_color = style.TEXT_BGR,
        line_color = style.AXES_LINE,
        padding = (0, 10),
        **overrides)
    
    return box


def make_guide_events_plot(**overrides):
    """Makes guide events plot."""
    
    # init plot
    plot = perrot.Plot(
        tag = "guide_events",
        frame_x1 = style.PLOT_FRAME_X1,
        x_axis_visible = False,
        x_axis_ticker = pero.TimeTicker(),
        y_axis_visible = False,
        y_axis_title = "",
        y_axis_autoscale = True,
        y_major_grid_visible = False,
        y_minor_grid_visible = False,
        padding = (style.PLOT_SPACING, 0, 0.5*style.PLOT_SPACING, 0),
        **overrides)
    
    # finalize style
    finalize_plot_style(plot)
    
    return plot


def make_guide_star_mass_plot(**overrides):
    """Makes guide star mass plot."""
    
    # init plot
    plot = perrot.Plot(
        tag = "guide_star_mass",
        frame_x1 = style.PLOT_FRAME_X1,
        x_axis_visible = False,
        x_axis_ticker = pero.TimeTicker(),
        x_axis_scale_in_range = (0, 60),
        y_axis_title = "mass",
        y_axis_ticker_major_count = 3,
        y_axis_ticker_formatter = pero.EngFormatter(),
        y_axis_autoscale = True,
        y_axis_scale_in_range = (0, 1),
        padding = (0.5*style.PLOT_SPACING, 0),
        **overrides)
    
    # finalize style
    finalize_plot_style(plot)
    
    return plot


def make_guide_star_snr_plot(**overrides):
    """Makes guide star SNR plot."""
    
    # init plot
    plot = perrot.Plot(
        tag = "guide_star_snr",
        frame_x1 = style.PLOT_FRAME_X1,
        x_axis_visible = False,
        x_axis_ticker = pero.TimeTicker(),
        x_axis_scale_in_range = (0, 60),
        y_axis_title = "snr",
        y_axis_ticker_major_count = 3,
        y_axis_autoscale = True,
        y_axis_scale_in_range = (0, 1),
        padding = (0.5*style.PLOT_SPACING, 0),
        **overrides)
    
    # finalize style
    finalize_plot_style(plot)
    
    return plot


def make_guide_radec_plot(units=UNITS_ARCSEC, **overrides):
    """Makes guide RA/DEC plot in pixels."""
    
    # init plot
    plot = perrot.Plot(
        tag = "guide_radec",
        frame_x1 = style.PLOT_FRAME_X1,
        x_axis_visible = False,
        x_axis_ticker = pero.TimeTicker(),
        x_axis_scale_in_range = (0, 60),
        y_axis_title = f"[{units}]",
        y_axis_autoscale = True,
        y_axis_symmetric = True,
        y_axis_scale_in_range = (-1, 1),
        padding = (0.5*style.PLOT_SPACING, 0),
        **overrides)
    
    # add zero
    plot.hline(0, line_color=style.AXES_ZERO, z_index=perrot.SERIES_Z-1)
    
    # finalize style
    finalize_plot_style(plot)
    
    return plot


def make_guide_drift_plot(units=UNITS_ARCSEC, **overrides):
    """Makes guide cumulative drift plot in pixels."""
    
    # init plot
    plot = perrot.Plot(
        tag = "guide_drift",
        frame_x1 = style.PLOT_FRAME_X1,
        x_axis_ticker = pero.TimeTicker(),
        x_axis_scale_in_range = (0, 60),
        y_axis_title = f"drift-corr [{units}]",
        y_axis_autoscale = True,
        y_axis_symmetric = True,
        y_axis_scale_in_range = (-1, 1),
        padding = (0.5*style.PLOT_SPACING, 0),
        **overrides)
    
    # add zero
    plot.hline(0, line_color=style.AXES_ZERO, z_index=perrot.SERIES_Z-1)
    
    # finalize style
    finalize_plot_style(plot)
    
    return plot


def add_guide_event_data(plot, session, **overrides):
    """Adds events data to plot."""
    
    # remove old data
    for series in plot.series:
        plot.remove(series)
    
    # check session
    if session is None:
        return
    
    # add info
    evt_info = plot.scatter(
        tag = "series_evt_info",
        data = session.info,
        x = lambda d: d.stamp,
        y = 1,
        marker = "d",
        marker_size = 10,
        marker_line_color = lambda d: style.SERIES_EVT_COLOR.get(d.category, "a"),
        marker_fill_color = lambda d: style.SERIES_EVT_COLOR.get(d.category, "a"),
        marker_fill_alpha = 180,
        tooltip_text = format_guide_info_tooltip,
        tooltip_v_clip = False,
        margin = (0.5, 0.05),
        **overrides)
    
    # get error points
    errors = [p for p in session.points if p.error_code]
    
    # add errors
    error_info = plot.scatter(
        tag = "series_evt_error",
        data = errors,
        x = lambda d: d.stamp,
        y = 1,
        marker = "d",
        marker_size = 10,
        marker_line_color = style.SERIES_EVT_COLOR[INFO_CAT_ERROR],
        marker_fill_color = style.SERIES_EVT_COLOR[INFO_CAT_ERROR],
        marker_fill_alpha = 180,
        tooltip_text = format_guide_point_tooltip,
        tooltip_v_clip = False,
        margin = (0.5, 0.05),
        **overrides)
    
    # finalize style
    finalize_series_style(evt_info)
    finalize_series_style(error_info)


def add_guide_star_mass_data(plot, session, **overrides):
    """Adds star mass data to plot."""
    
    # remove old data
    for series in plot.series:
        plot.remove(series)
    
    for annot in plot.annotations:
        if annot.tag.startswith("annot_star_mass_"):
            plot.remove(annot)
    
    # check session
    if session is None:
        return
    
    # filter points
    points = [p for p in session.points if p.star_mass is not None]
    
    # add star mass
    star_mass = plot.profile(
        tag = "series_star_mass",
        data = points,
        x = lambda d: d.stamp,
        y = lambda d: d.star_mass,
        color = style.SERIES_STAR_MASS,
        show_points = False,
        tooltip_text = format_guide_point_tooltip,
        tooltip_v_clip = False,
        **overrides)
    
    # add median
    if points:
        median = numpy.median([p.star_mass for p in points])
        plot.hline(
            y = median,
            tag = "annot_star_mass_med",
            line_color = style.SERIES_STAR_MASS_MED,
            line_alpha = 170,
            line_style = pero.DASHED)
    
    # finalize style
    finalize_series_style(star_mass)


def add_guide_star_snr_data(plot, session, **overrides):
    """Adds star SNR data to plot."""
    
    # remove old data
    for series in plot.series:
        plot.remove(series)
    
    for annot in plot.annotations:
        if annot.tag.startswith("annot_star_snr_"):
            plot.remove(annot)
    
    # check session
    if session is None:
        return
    
    # filter points
    points = [p for p in session.points if p.star_snr is not None]
    
    # add star mass
    star_snr = plot.profile(
        tag = "series_star_snr",
        data = points,
        x = lambda d: d.stamp,
        y = lambda d: d.star_snr,
        color = style.SERIES_STAR_SNR,
        show_points = False,
        tooltip_text = format_guide_point_tooltip,
        tooltip_v_clip = False,
        **overrides)
    
    # add median
    if points:
        median = numpy.median([p.star_snr for p in points])
        plot.hline(
            y = median,
            tag = "annot_star_snr_med",
            line_color = style.SERIES_STAR_SNR_MED,
            line_alpha = 170,
            line_style = pero.DASHED)
    
    # finalize style
    finalize_series_style(star_snr)


def add_guide_radec_data(plot, session, units=UNITS_ARCSEC, **overrides):
    """Adds RA/DEC data to plot."""
    
    # remove old data
    for series in plot.series:
        plot.remove(series)
        
    for annot in plot.annotations:
        if annot.tag.startswith("annot_"):
            plot.remove(annot)
    
    # check session
    if session is None:
        return
    
    # init scale factor
    f = 1 if units == UNITS_PX else session.pixel_scale
    
    # filter RA points
    points = [p for p in session.points if p.ra_raw_distance is not None]
    
    # add RA line
    ra_line = plot.profile(
        tag = "series_ra",
        title = "RA",
        data = points,
        x = lambda d: d.stamp,
        y = lambda d: -d.ra_raw_distance * f,
        color = style.SERIES_RA,
        show_points = False,
        legend_text_color = style.LEGEND_TEXT,
        tooltip_text = format_guide_point_tooltip,
        tooltip_v_clip = False,
        z_index = style.SERIES_Z_RA,
        **overrides)
    
    # filter DEC points
    points = [p for p in session.points if p.dec_raw_distance is not None]
    
    # add DEC line
    dec_line = plot.profile(
        tag = "series_dec",
        title = "DEC",
        data = points,
        x = lambda d: d.stamp,
        y = lambda d: d.dec_raw_distance * f,
        color = style.SERIES_DEC,
        show_points = False,
        legend_text_color = style.LEGEND_TEXT,
        tooltip_text = format_guide_point_tooltip,
        tooltip_v_clip = False,
        z_index = style.SERIES_Z_DEC,
        **overrides)
    
    # finalize style
    finalize_series_style(ra_line)
    finalize_series_style(dec_line)
    
    # add guide pulses
    add_guide_correction_data(plot, session, units)
    
    # add minimum move
    add_guide_mimo_data(plot, session, units)
    
    # mark rejected regions
    add_guide_rejection_data(plot, session)


def add_guide_correction_data(plot, session, units=UNITS_ARCSEC):
    """Adds guide pulses to plot."""
    
    # check session
    if session is None:
        return
    
    # init width
    pw = 0.4 * (session.exposure or 1)
    
    # init scale factor
    f = 1 if units == UNITS_PX else session.pixel_scale
    
    # filter RA points
    points = [p for p in session.points if p.ra_guide_distance]
    
    # add RA corrections
    ra_corr = plot.bars(
        tag = "series_corr_ra",
        data = points,
        left = lambda d: d.stamp-pw,
        right = lambda d: d.stamp+pw,
        top = lambda d: d.ra_guide_distance * f,
        bottom = 0,
        anchor = pero.TOP,
        color = style.SERIES_CORR_RA,
        line_alpha = 120,
        fill_alpha = 30,
        z_index = style.SERIES_Z_CORR_DA,
        tooltip_text = format_guide_point_tooltip,
        tooltip_v_clip = False)
    
    # filter DEC points
    points = [p for p in session.points if p.dec_guide_distance]
    
    # add DEC corrections
    dec_corr = plot.bars(
        tag = "series_corr_dec",
        data = points,
        left = lambda d: d.stamp-pw,
        right = lambda d: d.stamp+pw,
        top = lambda d: -d.dec_guide_distance * f,
        bottom = 0,
        anchor = pero.TOP,
        color = style.SERIES_CORR_DEC,
        line_alpha = 120,
        fill_alpha = 30,
        z_index = style.SERIES_Z_CORR_DEC,
        tooltip_text = format_guide_point_tooltip,
        tooltip_v_clip = False)
    
    # finalize style
    finalize_series_style(ra_corr)
    finalize_series_style(dec_corr)


def add_guide_mimo_data(plot, session, units=UNITS_ARCSEC):
    """Adds minimum moves to plot."""
    
    # remove old data
    for annot in plot.annotations:
        if annot.tag.startswith("annot_mimo_"):
            plot.remove(annot)
    
    # check session
    if session is None:
        return
    
    # init scale factor
    f = 1 if units == UNITS_PX else session.pixel_scale
    
    # add x lines
    if session.x_min_move:
        
        plot.hline(
            tag = "annot_mimo_x_hi",
            y = session.x_min_move * f,
            line_color = style.SERIES_MIMO_X,
            line_alpha = 170,
            line_style = pero.DOTTED)
        
        plot.hline(
            tag = "annot_mimo_x_lo",
            y = -session.x_min_move * f,
            line_color = style.SERIES_MIMO_X,
            line_alpha = 170,
            line_style = pero.DOTTED)
    
    # add y lines
    if session.y_min_move:
        
        plot.hline(
            tag = "annot_mimo_y_hi",
            y = session.y_min_move * f,
            line_color = style.SERIES_MIMO_Y,
            line_alpha = 170,
            line_style = pero.DOTTED)
        
        plot.hline(
            tag = "annot_mimo_y_lo",
            y = -session.y_min_move * f,
            line_color = style.SERIES_MIMO_Y,
            line_alpha = 170,
            line_style = pero.DOTTED)


def add_guide_thr_data(plot, session, pixel_size, focal_length, units=UNITS_ARCSEC):
    """Adds main scope thresholds to plot."""
    
    # remove old data
    for annot in plot.annotations:
        if annot.tag.startswith("annot_thr_"):
            plot.remove(annot)
    
    # init scale factor
    f = 1 if units == UNITS_PX else session.pixel_scale
    
    # apply main scope ratio
    pixel_scale = 206.265 * pixel_size / focal_length
    f *= pixel_scale / session.pixel_scale
    
    # add x lines
    if session.x_min_move:
        
        plot.hline(
            tag = "annot_thr_hi",
            y = 1 * f,
            line_color = style.SERIES_THR,
            line_alpha = 170,
            line_style = pero.DASHED)
        
        plot.hline(
            tag = "annot_thr_lo",
            y = -1 * f,
            line_color = style.SERIES_THR,
            line_alpha = 170,
            line_style = pero.DASHED)


def add_guide_rejection_data(plot, session):
    """Adds rejected regions to plot."""
    
    # remove old data
    for annot in plot.annotations:
        if annot.tag.startswith("annot_reject_"):
            plot.remove(annot)
    
    # check session
    if session is None:
        return
    
    # init buff
    count = 0
    running = False
    last = session.points[0]
    start = last.stamp
    
    # mark rejected regions
    for point in session.points:
        
        # set running
        if point.rejected:
            if not running:
                start = 0.5 * (point.stamp + last.stamp)
                running = True
        
        # mark region
        elif running:
            tag = f"annot_reject_{count}"
            end = 0.5 * (point.stamp + last.stamp)
            plot.vband(start, end, tag=tag, fill_color=style.SERIES_REJECTED, fill_alpha=60)
            running = False
            count += 1
        
        # remember last
        last = point


def add_guide_drift_data(plot, session, units=UNITS_ARCSEC, **overrides):
    """Makes cumulative drift data to plot."""
    
    # remove old data
    for series in plot.series:
        plot.remove(series)
    
    # check session
    if session is None:
        return
    
    # init scale factor
    f = 1 if units == UNITS_PX else session.pixel_scale
    
    # filter ra points
    points = [p for p in session.points if p.ra_drift is not None]
    
    # add RA line
    ra_drift = plot.profile(
        tag = "series_drift_ra",
        data = points,
        x = lambda d: d.stamp,
        y = lambda d: -d.ra_drift * f,
        color = style.SERIES_DRIFT_RA,
        show_points = False,
        tooltip_text = format_guide_point_tooltip,
        tooltip_v_clip = False,
        tooltip_anchor = pero.SW,
        tooltip_y_offset = -10,
        **overrides)
    
    # filter dec points
    points = [p for p in session.points if p.dec_drift is not None]
    
    # add DEC line
    dec_drift = plot.profile(
        tag = "series_drift_dec",
        data = points,
        x = lambda d: d.stamp,
        y = lambda d: -d.dec_drift * f,
        color = style.SERIES_DRIFT_DEC,
        show_points = False,
        tooltip_text = format_guide_point_tooltip,
        tooltip_v_clip = False,
        tooltip_anchor = pero.SW,
        tooltip_y_offset = -10,
        **overrides)
    
    # finalize style
    finalize_series_style(ra_drift)
    finalize_series_style(dec_drift)


def finalize_plot_style(plot):
    """Finalizes plot style."""
    
    # x-tooltip formatter
    def x_tooltip(seconds):
        return f"{seconds:.3f} s"
    
    # prepare properties
    props = {
        "bgr_fill_color": style.MAIN_BGR,
        
        "frame_line_color": style.AXES_LINE,
        "frame_fill_color": style.PLOT_BGR,
        
        "legend_line_color": style.LEGEND_LINE,
        "legend_fill_color": style.LEGEND_BGR,
        
        "x_axis_title_font_weight": pero.NORMAL,
        "x_axis_title_text_color": style.AXES_TEXT,
        "x_axis_ticker_formatter": XFormatter(),
        "x_axis_tooltip": pero.FuncFormatter(func=x_tooltip),
        "x_axis_label_text_color": style.AXES_TEXT,
        "x_axis_line_color": style.AXES_LINE,
        "x_axis_major_tick_line_color": style.AXES_LINE,
        "x_axis_minor_tick_line_color": style.AXES_LINE,
        "x_major_grid_line_color": style.GRID_MAJOR,
        "x_minor_grid_line_color": style.GRID_MINOR,
        "x_axis_tooltip_resaware": False,
        
        "y_axis_title_font_weight": pero.NORMAL,
        "y_axis_title_text_color": style.AXES_TEXT,
        "y_axis_label_text_color": style.AXES_TEXT,
        "y_axis_line_color": style.AXES_LINE,
        "y_axis_minor_tick_size": 0,
        "y_axis_major_tick_line_color": style.AXES_LINE,
        "y_axis_minor_tick_line_color": style.AXES_LINE,
        "y_major_grid_line_color": style.GRID_MAJOR,
        "y_minor_grid_line_color": style.GRID_MINOR,
        "y_minor_grid_visible": False,
    }
    
    # apply to plot
    plot.set_properties(props)


def finalize_series_style(series):
    """Finalizes series style."""
    
    # prepare properties
    props = {
        "tooltip_line_color": style.TOOLTIP_LINE,
        "tooltip_fill_color": style.TOOLTIP_BGR,
        "tooltip_text_color": style.TOOLTIP_TEXT,
        "tooltip_font_size": style.TOOLTIP_SIZE,
        "tooltip_text_spacing": style.TOOLTIP_SPACING,
        "tooltip_padding": 7,
    }
    
    # apply to series
    series.set_properties(props)


def finalize_plot_control_style(control):
    """Finalizes plot control style."""
    
    # prepare properties
    props = {
        "left_tool_line_color": style.AXES_LINE,
        "left_tool_fill_color": style.TOOLTIP_BGR,
        "left_tool_fill_alpha": 150,
        "right_tool_relative": False,
        "right_tool_line_color": style.AXES_LINE,
        "tooltip_line_color": style.TOOLTIP_LINE,
        "tooltip_fill_color": style.TOOLTIP_BGR,
        "tooltip_text_color": style.TOOLTIP_TEXT,
        "tooltip_font_size": style.TOOLTIP_SIZE,
        "tooltip_text_spacing": style.TOOLTIP_SPACING,
        "tooltip_padding": 7,
    }
    
    # apply to plot control
    control.set_properties(props)


def format_guide_point_tooltip(point):
    """Formats guide point for tooltip."""
    
    tooltip = []
    
    tooltip.append(f"time: {point.time.strftime('%H:%M:%S')}")
    tooltip.append(f"frame: {point.frame}")
    tooltip.append(f"seconds: {point.seconds:.2f}")
    
    if point.dx is not None and point.dy is not None:
        tooltip.append(f"dx, dy: {point.dx:.2f} px, {point.dy:.2f} px")
    
    if point.ra_raw_distance is not None and point.dec_raw_distance is not None:
        px = f"{point.ra_raw_distance:.2f} px, {point.dec_raw_distance:.2f} px"
        arcsec = f"{point.ra_raw_distance * point.scale:.2f}\", {point.dec_raw_distance * point.scale:.2f}\""
        tooltip.append(f"raw dist.: {arcsec} ({px})")
    
    if point.ra_guide_distance is not None and point.dec_guide_distance is not None:
        px = f"{point.ra_guide_distance:.2f} px, {point.dec_guide_distance:.2f} px"
        arcsec = f"{point.ra_guide_distance * point.scale:.2f}\", {point.dec_guide_distance * point.scale:.2f}\""
        tooltip.append(f"guide dist.: {arcsec} ({px})")
    
    if point.ra_duration is not None and point.dec_duration is not None:
        tooltip.append(f"guide dur.: {point.ra_duration:.2f} ms, {point.dec_duration:.2f} ms")
    
    if point.ra_direction is not None and point.dec_direction is not None:
        tooltip.append(f"guide dir.: {point.ra_direction}, {point.dec_direction}")
    
    if point.star_mass is not None:
        tooltip.append(f"star mass: {point.star_mass:.0f}")
    
    if point.star_snr is not None:
        tooltip.append(f"star snr: {point.star_snr:.0f}")
    
    if point.error_code:
        tooltip.append(f"error: ({point.error_code}) {point.error_info}")
    
    if point.rejected:
        tooltip.append("rejected")
    
    return "\n".join(tooltip)


def format_guide_info_tooltip(point):
    """Formats info point for tooltip."""
    
    tooltip = []
    
    tooltip.append(f"time: {point.time.strftime('%H:%M:%S')}")
    tooltip.append(f"frame: {point.frame}")
    tooltip.append(f"seconds: {point.seconds:.2f}")
    tooltip.append(f"category: {point.category.lower()}")
    tooltip.append(f"value: {point.value.lower()}")
    
    return "\n".join(tooltip)


def format_guide_session_info(session):
    """Formats session info."""
    
    # init label
    label = ""
    
    # format length
    seconds = session.length
    hours = seconds // 3600
    seconds = seconds % 3600
    minutes = seconds // 60
    seconds = seconds % 60
    
    # add session time
    label += f"{str(session.time)}  - "
    if hours:
        label += f" {hours:.0f}h"
    if minutes or hours and seconds:
        label += f" {minutes:.0f}m"
    if seconds:
        label += f" {seconds:.0f}s"
    
    # add points count
    label += f"  -  {len(session.points):,d} entries"
    
    return label


class XFormatter(pero.Formatter):
    """Defines custom x-axis formatter."""
    
    
    def format(self, value, *args, **kwargs):
        """Formats given value."""
        
        dt = datetime.datetime.fromtimestamp(value)
        if self.precision > 1:
            return dt.strftime('%H:%M:%S')
        
        digits = min(6, abs(int(numpy.floor(numpy.log10(abs(self.precision))))))
        label = dt.strftime('%H:%M:%S.%f')
        return label[:9+digits]
