#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Very simple app-indicator, shows gtk-bookmarsk (aka places)
# Author: Alex Simenduev <shamil.si@gmail.com>
#

import os
import gtk
import gio
import signal
import subprocess
import appindicator

APP_NAME = 'indicator-places'
APP_VERSION = '0.3'

class IndicatorPlaces:
    BOOKMARKS_PATH = os.getenv('HOME') + '/.gtk-bookmarks'

    def __init__(self):
        self.ind = appindicator.Indicator("Places", "nautilus", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_label("Places")
        self.ind.set_status(appindicator.STATUS_ACTIVE)        

        self.update_menu()

    # This methind creates a menu
    def update_menu(self, widget = None, data = None):
        try:
            bookmarks = open(self.BOOKMARKS_PATH).readlines()
        except IOError:
            bookmarks = []        

        # Create menu
        menu = gtk.Menu()
        self.ind.set_menu(menu)

        # Home folder menu item
        item = gtk.MenuItem("Home folder")
        item.connect("activate", self.on_bookmark_click, os.getenv('HOME'))
        menu.append(item)

        # Computer menu item
        item = gtk.MenuItem("Computer")
        item.connect("activate", self.on_bookmark_click, 'computer:')
        menu.append(item)

        # Computer menu item
        item = gtk.MenuItem("Network")
        item.connect("activate", self.on_bookmark_click, 'computer:')
        menu.append(item)

        # Show separator
        item = gtk.SeparatorMenuItem()
        menu.append(item)

        # Populate bookmarks menu items
        for bm in bookmarks:
            path, label = bm.strip().partition(' ')[::2]

            if not label:
                label = os.path.basename(os.path.normpath(path))

            item = gtk.MenuItem(label)
            item.connect("activate", self.on_bookmark_click, path)

            # Append the item to menu
            menu.append(item)

        # Show separator
        item = gtk.SeparatorMenuItem()
        menu.append(item)
        
        # About menu item
        item = gtk.MenuItem('About')
        item.connect("activate", self.on_about_click)
        menu.append(item)

        # Quit menu item
        item = gtk.MenuItem("Quit")
        item.connect("activate", gtk.main_quit)
        menu.append(item)

        # Show the menu
        menu.show_all()

    # Open clicked bookmark
    def on_bookmark_click(self, widget, path):
#       subprocess.Popen('/usr/bin/xdg-open %s' % path, shell = True)
        subprocess.Popen('/usr/bin/nautilus %s' % path, shell = True)
        
    # Show about dialog
    def on_about_click(self, widget, data = None):
        about = gtk.AboutDialog()
        about.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        about.set_program_name(APP_NAME)
        about.set_version(APP_VERSION)
        about.set_comments("A very simple indicator which shows GTK Bookmarks")
        about.set_copyright("Copyright 2011 © Alex Simenduev <shamil.si@gmail.com>")        
        about.set_website("github.com/shamil/indicator-places")
        about.set_logo_icon_name('nautilus')
        about.run()
        about.hide()
        
    def on_bookmarks_changed(self, filemonitor, file, other_file, event_type):
        if event_type == gio.FILE_MONITOR_EVENT_CHANGES_DONE_HINT:
            print 'Bookmarks changed, updating menu...'
            self.update_menu()

if __name__ == "__main__":
    # Catch CTRL-C
    signal.signal(signal.SIGINT, lambda signal, frame: gtk.main_quit())

    # Run the indicator
    i = IndicatorPlaces()
    
    # Monitor bookmarks changes 
    file = gio.File(i.BOOKMARKS_PATH)
    monitor = file.monitor_file()
    monitor.connect("changed", i.on_bookmarks_changed)            
    
    # Main gtk loop
    gtk.main()
