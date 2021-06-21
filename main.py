#!/usr/bin/env python
import handler
import viewport
import globals

globals.drawing_area.connect('draw', viewport.draw_cb)
globals.drawing_area.connect('configure-event', viewport.configure_event_cb)

globals.gtkBuilder.connect_signals(handler.Handler())

globals.window.show_all()
viewport.desenhar_borda()
globals.Gtk.main()
