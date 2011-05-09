#!/usr/bin/python
#
# Very simple app-indicator, shows gtk-bookmarsk (aka places)
# Author: Alex Simenduev <shamil.si@gmail.com>
#

import os
import gtk
import signal
import subprocess
import appindicator

APP_NAME = 'indicator-places'
APP_VERSION = '0.2'

class application:
    def __init__(self):
        self.ind = appindicator.Indicator ("Places", "user-home", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status (appindicator.STATUS_ACTIVE)        

        self.update_menu()

    def update_menu(self, widget = None, data = None):
        try:
            bookmarks_path = os.path.join(os.path.expanduser('~'), '.gtk-bookmarks')
            bookmarks = open(bookmarks_path).readlines()
        except IOError:
            bookmarks = []        

        # Create menu
        menu = gtk.Menu()
        self.ind.set_menu(menu)

        # Home folder menu item
        item = gtk.MenuItem("Home folder")
        item.connect("activate", self.on_bookmark_click, '~')
        item.show()
        menu.append(item)

        # Show separator
        item = gtk.SeparatorMenuItem()
        item.show()
        menu.append(item)

        # Populate bookmarks menu items
        for bm in bookmarks:
            path, label = bm.strip().partition(' ')[::2]

            if not label:
                label = os.path.basename(os.path.normpath(path))

            item = gtk.MenuItem(label)
            item.connect("activate", self.on_bookmark_click, path) # run open_place function on item activate
            item.show() # show the item

            # Append the item to menu
            menu.append(item)

        # Show separator
        item = gtk.SeparatorMenuItem()
        item.show()
        menu.append(item)

        # Refresh menu item
        item = gtk.MenuItem('Refresh')
        item.connect("activate", self.update_menu)
        item.show()
        menu.append(item)

        # Show separator
        item = gtk.SeparatorMenuItem()
        item.show()
        menu.append(item)

        # About menu item
        item = gtk.MenuItem('About')
        item.connect("activate", self.on_about_click)
        item.show()
        menu.append(item)

        # Quit menu item
        item = gtk.MenuItem("Quit")
        item.connect("activate", gtk.main_quit)
        item.show()
        menu.append(item)

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
        about.set_authors(["Alex Simenduev <shamil.si@gmail.com>"])
        about.set_website("http://github.com/shamil/indicator-places")
        about.set_logo_icon_name('user-home')
        about.run()
        about.hide()

if __name__ == "__main__":
    # Catch CTRL-C
    signal.signal(signal.SIGINT, lambda signal, frame: gtk.main_quit())

    # Run the app
    application()
    gtk.main()
