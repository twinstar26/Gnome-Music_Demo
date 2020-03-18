import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import Gio
from gi.repository import Pango

import sys


class Gmenu(Gio.MenuModel):
    def __init__(self, app):
        self.menu = Gio.Menu()
        self.menu.append("Quit", "app.quit")

        self.quit_action = Gio.SimpleAction.new("quit", None)
        self.quit_action.connect("activate", self.quit_cb)
        app.add_action(self.quit_action)

    def quit_cb(self, action, parameter):
        print("You have quit.")
        app.quit()


class MyWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.Window.__init__(self, title="GNOME-Music Demo", application=app)
        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.searchbar = Gtk.SearchBar()
        self.grid.attach(self.searchbar, 0, 0, 1, 1)
        if not self.searchbar.get_search_mode():
            self.searchbar.set_search_mode(True)
        self.searchentry = Gtk.SearchEntry()
        self.searchbar.connect_entry(self.searchentry)
        self.searchbar.add(self.searchentry)
        self.searchbar.set_show_close_button(False)
        self.connect("key-release-event", self._on_key_release)
        self.query = str()

        self.columns = ["SONGS FOUND"]
        # this will come from grilo backend
        self.phonebook = [["song1"], ["song2"], ["song3"], ["song4"]]

        self.listmodel = Gtk.ListStore(str)
        for i in range(len(self.phonebook)):
            self.listmodel.append(self.phonebook[i])

        self.view = Gtk.TreeView(model=self.listmodel)
        for i, column in enumerate(self.columns):
            cell = Gtk.CellRendererText()
            if i == 0:
                cell.props.weight_set = True
                cell.props.weight = Pango.Weight.BOLD
            col = Gtk.TreeViewColumn(column, cell, text=i)
            self.view.append_column(col)

        self.view.get_selection().connect("changed", self.on_changed)

        self.label = Gtk.Label()
        self.label.set_text("")

        self.grid.attach(self.view, 0, 1, 1, 1)
        self.grid.attach(self.label, 0, 2, 1, 1)

        self.add(self.grid)


    def on_changed(self, selection):
        (model, iter) = selection.get_selected()
        self.label.set_text("\n %s" % (model[iter][0]))
        return True


    def _on_key_release(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        if keyname == 'Return':
            print("Query entered is >> " + str(self.query))
            self.searchbar.set_visible(True)
            # grilo code goes over here

        elif keyname == "space":
            self.query += " "
        elif keyname == "BackSpace":
            self.query[:-1]
        elif keyname == "Left" or keyname == "Right" or keyname == "Up" or keyname == "Down":
            pass
        else:
            if str(keyname).isalpha():
                self.query += str(keyname)
                # print(self.query)
                
class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)
        self.menu = Gmenu(self)

    def do_activate(self):
        win = MyWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)
        self.set_app_menu(self.menu.menu)

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)