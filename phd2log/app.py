#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import os.path
import pero
import perrot

from .constants import *
from .parser import parse_log
from .calculations import calc_guiding_rms
from .guiding import GuideSession
from .import plotting
from .import style


class PHD2Viewer(object):
    """Creates PHD2 viewer app."""
    
    
    def __init__(self):
        """Initializes new instance of PHD2Viewer."""
        
        self._path = None
        self._sessions = []
        self._session = None
        
        self._settings = {
            "autoscale": True,
            "show_ra": True,
            "show_dec": True,
            "show_corr": True,
            "show_mimo": True,
            "show_thr": True}
        
        self._prev_butt = None
        self._next_butt = None
        self._info_butt = None
        self._refresh_butt = None
        
        self._info_text = None
        self._session_text = None
        
        self._rms_text = None
        self._events_plot = None
        self._star_mass_plot = None
        self._star_snr_plot = None
        self._radec_plot = None
        self._drift_plot = None
        
        self._syncer = None
        self._layout = None
        
        # make UI
        self._init_buttons()
        self._init_infos()
        self._init_plots()
        self._init_syncer()
        self._init_layout()
        self._bind_events()
    
    
    def show(self, width=1180, height=750):
        """Shows viewer."""
        
        # make title
        title = style.APP_NAME
        if self._path:
            filename = os.path.basename(self._path)
            title += f" - {filename}"
        
        # show app
        self._layout.show(title, width=width, height=height)
    
    
    def open(self, path):
        """Opens given log file."""
        
        # show loading signs
        self._update_session_info("Opening log file...")
        self._update_rms_info("")
        self._repaint()
        
        # check path
        if not os.path.exists(path):
            self._update_session_info("Drop a PHD2 log file onto the app window")
            self._show_info(text=f"File does not exist!\n{path}")
            return
        
        # set path
        self._path = path
        
        # set title
        filename = os.path.basename(path)
        self._layout.set_title(f"{style.APP_NAME} - {filename}")
        
        # parse log
        self._sessions = []
        sessions = parse_log(self._path)
        for session in sessions:
            if isinstance(session, GuideSession):
                self._sessions.append(session)
        
        # open first session
        session = self._sessions[0] if self._sessions else None
        self._set_session(session)
    
    
    def _on_drop_files(self, evt):
        """Defines drop files event handling."""
        
        self.open(evt.paths[-1])
    
    
    def _on_key_down(self, evt):
        """Defines key down event handling."""
        
        # show help
        if evt.char == "h":
            self._show_info_help()
        
        # show session settings
        elif evt.char == "i":
            self._show_info_settings()
        
        # show sessions
        elif evt.char == "s":
            self._show_info_sessions_list()
        
        # set session
        elif evt.char in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
            self._set_next_session(int(evt.char))
        
        # set next session
        elif evt.char == "n":
            self._set_next_session()
        
        # set previous session
        elif evt.char == "p":
            self._set_next_session(reverse=True)
        
        # toggle y-axis autoscale
        elif evt.char == "a":
            self._settings["autoscale"] = not self._settings["autoscale"]
            self._radec_plot.graphics.y_axis.autoscale = self._settings["autoscale"]
            self._drift_plot.graphics.y_axis.autoscale = self._settings["autoscale"]
        
        # toggle RA visibility
        elif evt.char == "r":
            self._settings["show_ra"] = not self._settings["show_ra"]
            self._update_ra_visibility(True, True)
        
        # toggle DEC visibility
        elif evt.char == "d":
            self._settings["show_dec"] = not self._settings["show_dec"]
            self._update_dec_visibility(True, True)
        
        # toggle corrections visibility
        elif evt.char == "c":
            self._settings["show_corr"] = not self._settings["show_corr"]
            self._update_corr_visibility(True, True)
        
        # toggle mimo visibility
        elif evt.char in ("m", "l"):
            self._settings["show_mimo"] = not self._settings["show_mimo"]
            self._update_mimo_visibility(True, True)
        
        # toggle threshold visibility
        elif evt.char == "t":
            self._settings["show_thr"] = not self._settings["show_thr"]
            self._update_thr_visibility(True, True)
        
        # recalculate RMS
        elif evt.char == "e":
            self._update_rms_info()
        
        # unhandled key
        else:
            return
        
        # cancel event propagation
        evt.cancel()
    
    
    def _on_navigation_butt(self, evt, reverse=False):
        """Defines navigation button event handling."""
        
        self._set_next_session(reverse=reverse)
    
    
    def _on_info_butt(self, evt):
        """Defines info button event handling."""
        
        self._show_info_settings()
    
    
    def _on_refresh_butt(self, evt):
        """Defines refresh button event handling."""
        
        self._update_rms_info()
    
    
    def _on_help_butt(self, evt):
        """Defines help button event handling."""
        
        self._show_info_help()
    
    
    def _on_session_text_mouse_up(self, evt):
        """Defines mouse up event handling."""
        
        self._show_info_sessions_list()
    
    
    def _on_rms_text_mouse_up(self, evt):
        """Defines mouse up event handling."""
        
        self._update_rms_info()
    
    
    def _repaint(self):
        """Forces immediate repaint."""
        
        self._layout.should_repaint()
    
    
    def _set_session(self, session):
        """Sets session data to all elements."""
        
        # show loading signs
        self._update_session_info("Loading session...")
        self._update_rms_info("")
        self._repaint()
        
        # set session
        self._session = session
        
        # set data to plots
        self._update_plots_data()
        
        # zoom to full range
        self._radec_plot.zoom()
        self._syncer.force(self._radec_plot)
        
        # set data to infos
        self._update_session_info()
        self._update_rms_info()
    
    
    def _set_next_session(self, pos=None, reverse=False):
        """Sets next guiding session."""
        
        # check sessions
        if not self._sessions:
            return
        
        # set selected
        if pos is not None:
            if pos <= len(self._sessions):
                self._set_session(self._sessions[pos-1])
            return
        
        # get sessions
        sessions = self._sessions[:] + self._sessions[:]
        
        # reverse order
        if reverse:
            sessions.reverse()
        
        # set new
        if self._session is None:
            self._set_session(sessions[0])
            return
        
        # set next
        it = iter(sessions)
        for session in it:
            if session is self._session:
                self._set_session(next(it))
                return
    
    
    def _init_buttons(self):
        """Initializes buttons elements."""
        
        # init previous session button
        graphics = plotting.make_guide_button(
            tag = "butt_prev",
            icon = plotting.ICON_LEFT,
            x = style.PLOT_FRAME_X1,
            radius = (6, 0, 0, 6))
        self._prev_butt = pero.Control(graphics=graphics)
        
        # init next session button
        graphics = plotting.make_guide_button(
            tag = "butt_next",
            icon = plotting.ICON_RIGHT,
            radius = 0)
        self._next_butt = pero.Control(graphics=graphics)
        
        # init session info button
        graphics = plotting.make_guide_button(
            tag = "butt_info",
            icon = plotting.ICON_INFO,
            radius = (0, 6, 6, 0))
        self._info_butt = pero.Control(graphics=graphics)
        
        # init rms refresh button
        graphics = plotting.make_guide_button(
            tag = "butt_refresh",
            icon = plotting.ICON_REFRESH,
            radius = (0, 6, 6, 0))
        self._refresh_butt = pero.Control(graphics=graphics)
        
        # init help button
        graphics = plotting.make_guide_button(
            tag = "butt_help",
            icon = plotting.ICON_HELP,
            x = style.PLOT_SPACING,
            radius = 6)
        self._help_butt = pero.Control(graphics=graphics)
    
    
    def _init_infos(self):
        """Initializes all info elements."""
        
        # make session info
        graphics = plotting.make_guide_session_text(graphics_text="Drop a PHD2 log file onto the app window")
        self._session_text = pero.Control(graphics=graphics)
        
        # make RMS info
        graphics = plotting.make_guide_rms_text()
        self._rms_text = pero.Control(graphics=graphics)
        
        # init system info
        self._info_text = pero.Textbox(
            anchor = pero.C,
            font_size = 14,
            text_color = style.SYSINFO_TEXT,
            text_spacing = .4,
            fill_color = style.SYSINFO_BGR,
            line_color = style.SYSINFO_LINE,
            radius = 10,
            padding = (10, 15))
    
    
    def _init_plots(self):
        """Initializes all plots elements."""
        
        # make events plot
        graphics = plotting.make_guide_events_plot()
        self._events_plot = perrot.PlotControl(graphics=graphics)
        plotting.finalize_plot_control_style(self._events_plot)
        
        # make star mass plot
        graphics = plotting.make_guide_star_mass_plot()
        self._star_mass_plot = perrot.PlotControl(graphics=graphics)
        plotting.finalize_plot_control_style(self._star_mass_plot)
        
        # make star SNR plot
        graphics = plotting.make_guide_star_snr_plot()
        self._star_snr_plot = perrot.PlotControl(graphics=graphics)
        plotting.finalize_plot_control_style(self._star_snr_plot)
        
        # make RA/DEC plot
        graphics = plotting.make_guide_radec_plot(UNITS_ARCSEC)
        self._radec_plot = perrot.PlotControl(graphics=graphics)
        plotting.finalize_plot_control_style(self._radec_plot)
        
        # make drift plot
        graphics = plotting.make_guide_drift_plot(UNITS_ARCSEC)
        self._drift_plot = perrot.PlotControl(graphics=graphics)
        plotting.finalize_plot_control_style(self._drift_plot)
    
    
    def _init_syncer(self):
        """Synchronize x-axes of all plots."""
        
        self._syncer = perrot.Syncer()
        
        self._syncer.sync_x(self._events_plot, self._star_mass_plot)
        self._syncer.sync_x(self._events_plot, self._star_snr_plot)
        self._syncer.sync_x(self._events_plot, self._radec_plot)
        self._syncer.sync_x(self._events_plot, self._drift_plot)
        
        self._syncer.sync_x(self._star_mass_plot, self._events_plot)
        self._syncer.sync_x(self._star_mass_plot, self._star_snr_plot)
        self._syncer.sync_x(self._star_mass_plot, self._radec_plot)
        self._syncer.sync_x(self._star_mass_plot, self._drift_plot)
        
        self._syncer.sync_x(self._star_snr_plot, self._events_plot)
        self._syncer.sync_x(self._star_snr_plot, self._star_mass_plot)
        self._syncer.sync_x(self._star_snr_plot, self._radec_plot)
        self._syncer.sync_x(self._star_snr_plot, self._drift_plot)
        
        self._syncer.sync_x(self._drift_plot, self._events_plot)
        self._syncer.sync_x(self._drift_plot, self._star_mass_plot)
        self._syncer.sync_x(self._drift_plot, self._star_snr_plot)
        self._syncer.sync_x(self._drift_plot, self._radec_plot)
        
        self._syncer.sync_x(self._radec_plot, self._events_plot)
        self._syncer.sync_x(self._radec_plot, self._star_mass_plot)
        self._syncer.sync_x(self._radec_plot, self._star_snr_plot)
        self._syncer.sync_x(self._radec_plot, self._drift_plot)
    
    
    def _init_layout(self):
        """Initializes main layout."""
        
        # init _layout
        self._layout = pero.Sizer()
        self._layout.graphics.padding = (20, 20, 20, 0)
        self._layout.graphics.fill_color = style.MAIN_BGR
        
        # add cols and rows
        self._layout.add_col(width=style.BUTTON_WIDTH+style.PLOT_FRAME_X1, relative=False)
        self._layout.add_col(width=style.BUTTON_WIDTH, relative=False)
        self._layout.add_col()
        self._layout.add_col(width=style.BUTTON_WIDTH, relative=False)
        self._layout.add_col()
        self._layout.add_col(width=style.BUTTON_WIDTH, relative=False)
        self._layout.add_col(width=style.BUTTON_WIDTH+style.PLOT_SPACING, relative=False)
        
        self._layout.add_row(height=style.TEXT_HEIGHT, relative=False)
        self._layout.add_row(height=style.PLOT_HEIGHT_EVENTS, relative=False)
        self._layout.add_row(height=style.PLOT_HEIGHT_STAR_MASS, relative=False)
        self._layout.add_row(height=style.PLOT_HEIGHT_STAR_SNR, relative=False)
        self._layout.add_row(0.6)
        self._layout.add_row(0.4)
        
        # add elements
        self._layout.add(self._prev_butt, 0, 0)
        self._layout.add(self._next_butt, 0, 1)
        self._layout.add(self._session_text, 0, 2)
        self._layout.add(self._info_butt, 0, 3)
        
        self._layout.add(self._rms_text, 0, 4)
        self._layout.add(self._refresh_butt, 0, 5)
        
        self._layout.add(self._help_butt, 0, 6)
        
        self._layout.add(self._events_plot, 1, 0, col_span=7)
        self._layout.add(self._star_mass_plot, 2, 0, col_span=7)
        self._layout.add(self._star_snr_plot, 3, 0, col_span=7)
        self._layout.add(self._radec_plot, 4, 0, col_span=7)
        self._layout.add(self._drift_plot, 5, 0, col_span=7)
    
    
    def _bind_events(self):
        """Binds interaction events."""
        
        # bind file drops to main layout
        self._layout.bind(pero.EVT_DROP_FILES, self._on_drop_files)
        
        # bind all key events to main layout
        self._layout.bind(pero.EVT_KEY_DOWN, self._on_key_down)
        
        # bind mouse click event to buttons
        self._prev_butt.bind(pero.EVT_LEFT_UP, self._on_navigation_butt, reverse=True)
        self._next_butt.bind(pero.EVT_LEFT_UP, self._on_navigation_butt)
        self._info_butt.bind(pero.EVT_LEFT_UP, self._on_info_butt)
        self._refresh_butt.bind(pero.EVT_LEFT_UP, self._on_refresh_butt)
        self._help_butt.bind(pero.EVT_LEFT_UP, self._on_help_butt)
        
        # bind mouse click event to infos
        self._session_text.bind(pero.EVT_LEFT_UP, self._on_session_text_mouse_up)
    
    
    def _show_info(self, canvas=None, text="", **kwargs):
        """Shows system overlay info."""
        
        # draw to overlay
        if canvas is None:
            self._layout.draw_overlay(self._show_info, text=text, **kwargs)
            self._layout.should_repaint()
            return
        
        # recalc coords back to whole view
        x = 0.5 * canvas.width - canvas.viewport.x
        y = 0.5 * canvas.height - canvas.viewport.y
        
        # draw to canvas
        self._info_text.draw(canvas,
            text = text,
            x = x,
            y = y,
            **kwargs)
    
    
    def _show_info_settings(self):
        """Shows session settings."""
        
        if self._session is not None:
            self._show_info(text=self._session.settings.strip())
    
    
    def _show_info_help(self):
        """Shows app help."""
        
        text = ""
        text += "H - shows this help\n"
        text += "I - shows session info\n"
        text += "S - shows list of sessions\n"
        text += "N - loads next session\n"
        text += "P - loads previous session\n"
        text += "R - toggles RA data visibility\n"
        text += "D - toggles DEC data visibility\n"
        text += "C - toggles corrections visibility\n"
        text += "M - toggles minimum move visibility\n"
        text += "A - toggles autoscale on RA/DEC and drift plots\n"
        text += "E - evaluates RMS for visible range\n"
        text += "1 to 9 - jumps to specific session"
        
        self._show_info(text=text)
    
    
    def _show_info_sessions_list(self):
        """Shows sessions list."""
        
        labels = []
        for i, session in enumerate(self._sessions):
            info = plotting.format_guide_session_info(session)
            labels.append(f"{i+1}:  {info}")
        
        self._show_info(text="\n".join(labels))
    
    
    def _update_session_info(self, text=None):
        """Updates current session info text."""
        
        # set given text
        if text is not None:
            self._session_text.graphics.graphics.text = text
            self._session_text.refresh()
            return
        
        # init label
        idx = self._sessions.index(self._session)
        label = f"{idx + 1}/{len(self._sessions)}  -  "
        
        # add session
        label += plotting.format_guide_session_info(self._session)
        
        # set label
        self._update_session_info(label)
    
    
    def _update_rms_info(self, text=None):
        """Updates current session RMS text."""
        
        # set given text
        if text is not None:
            self._rms_text.graphics.graphics.text = text
            self._rms_text.refresh()
            return
        
        # check session
        if self._session is None:
            self._update_rms_info("")
            return
        
        # get current x-range
        x_range = self._radec_plot.graphics.x_axis.scale.in_range
        
        # get current data
        points = []
        for point in self._session.points:
            if x_range[0] <= point.stamp <= x_range[1] and not point.rejected:
                points.append(point)
        
        # check points
        if len(points) < 2:
            self._update_rms_info("Not enough valid entries")
            return
        
        # calc rms
        rms_ra_px, rms_dec_px, rms_tot_px = calc_guiding_rms(points)
        rms_ra_arcsec = rms_ra_px * self._session.pixel_scale
        rms_dec_arcsec = rms_dec_px * self._session.pixel_scale
        rms_tot_arcsec = rms_tot_px * self._session.pixel_scale
        
        # create label
        label = ""
        label += f"RMS: {rms_tot_arcsec:.2f}\" / {rms_tot_px:.2f} px  -  "
        label += f"RA: {rms_ra_arcsec:.2f}\" / {rms_ra_px:.2f} px  -  "
        label += f"DEC: {rms_dec_arcsec:.2f}\" / {rms_dec_px:.2f} px"
        
        # set label
        self._update_rms_info(label)
    
    
    def _update_plots_data(self):
        """Updates all plots with current session."""
        
        # set data to plots
        plotting.add_guide_event_data(self._events_plot.graphics, self._session)
        self._events_plot.refresh()
        
        plotting.add_guide_star_mass_data(self._star_mass_plot.graphics, self._session)
        self._star_mass_plot.refresh()
        
        plotting.add_guide_star_snr_data(self._star_snr_plot.graphics, self._session)
        self._star_snr_plot.refresh()
        
        plotting.add_guide_radec_data(self._radec_plot.graphics, self._session, UNITS_ARCSEC)
        self._update_ra_visibility(False, False)
        self._update_dec_visibility(False, False)
        self._update_corr_visibility(False, False)
        self._update_mimo_visibility(False, False)
        self._update_thr_visibility(False, False)
        self._radec_plot.refresh()
        
        plotting.add_guide_drift_data(self._drift_plot.graphics, self._session, UNITS_ARCSEC)
        self._update_ra_visibility(False, False)
        self._update_dec_visibility(False, False)
        self._drift_plot.refresh()
    
    
    def _update_ra_visibility(self, toggle, refresh):
        """Updates visibility of RA data."""
        
        # set data to update
        tags = (
            ("series_ra", "show_ra"),
            ("series_drift_ra", "show_ra"),
            ("series_corr_ra", "show_ra", "show_corr"),
            ("annot_mimo_x_hi", "show_ra", "show_mimo"),
            ("annot_mimo_x_lo", "show_ra", "show_mimo"))
        
        # set plots to update
        plots = (self._radec_plot, self._drift_plot)
        
        # update plots
        self._update_visibility(tags, plots, toggle, refresh)
    
    
    def _update_dec_visibility(self, toggle, refresh):
        """Updates visibility of DEC data."""
        
        # set data to update
        tags = (
            ("series_dec", "show_dec"),
            ("series_drift_dec", "show_dec"),
            ("series_corr_dec", "show_dec", "show_corr"),
            ("annot_mimo_y_hi", "show_dec", "show_mimo"),
            ("annot_mimo_y_lo", "show_dec", "show_mimo"))
        
        # set plots to update
        plots = (self._radec_plot, self._drift_plot)
        
        # update plots
        self._update_visibility(tags, plots, toggle, refresh)
    
    
    def _update_corr_visibility(self, toggle, refresh):
        """Updates visibility of correction data."""
        
        # set data to update
        tags = (
            ("series_corr_ra", "show_ra", "show_corr"),
            ("series_corr_dec", "show_dec", "show_corr"))
        
        # set plots to update
        plots = (self._radec_plot,)
        
        # update plots
        self._update_visibility(tags, plots, toggle, refresh)
    
    
    def _update_mimo_visibility(self, toggle, refresh):
        """Updates visibility of minimum move data."""
        
        # set data to update
        tags = (
            ("annot_mimo_x_hi", "show_ra", "show_mimo"),
            ("annot_mimo_x_lo", "show_ra", "show_mimo"),
            ("annot_mimo_y_hi", "show_dec", "show_mimo"),
            ("annot_mimo_y_lo", "show_dec", "show_mimo"))
        
        # set plots to update
        plots = (self._radec_plot,)
        
        # update plots
        self._update_visibility(tags, plots, toggle, refresh)
    
    
    def _update_thr_visibility(self, toggle, refresh):
        """Updates visibility of minimum move data."""
        
        # set data to update
        tags = (
            ("annot_thr_hi", "show_thr"),
            ("annot_thr_lo", "show_thr"))
        
        # set plots to update
        plots = (self._radec_plot,)
        
        # update plots
        self._update_visibility(tags, plots, toggle, refresh)
    
    
    def _update_visibility(self, tags, plots, toggle, refresh):
        """Toggles visibility of objects."""
        
        # update plots
        for plot in plots:
            
            # update objects
            for obj_tag, *requirements in tags:
                
                # get object
                obj = plot.graphics.get_obj(obj_tag, silent=True)
                if obj is None:
                    continue
                
                # toggle visibility
                visible = not obj.visible if toggle else obj.visible
                
                # check requirements
                if requirements:
                    settings = self._settings
                    visible = visible and all(settings[r] for r in requirements)
                
                # set visibility
                obj.visible = visible
            
            # refresh plot
            if refresh:
                plot.refresh()
