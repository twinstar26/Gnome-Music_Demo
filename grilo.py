import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Grl', '0.3')
from gi.repository import Gtk, Gdk, Grl, GObject
from gi.repository import Gio

import sys
import traceback

class YouTube():

    METADATA_KEYS = \
    [
        Grl.METADATA_KEY_TITLE,
        Grl.METADATA_KEY_URL,
        Grl.METADATA_KEY_INVALID
    ]

    def __init__(self):

        Grl.init(None)

        self.registry = Grl.Registry.get_default()

        # THIS API KEY IS NOT MINE AND SOLELY BELONGS TO GNOME-DEVELOPERS
        # I AM USING IT SOLELY FOR PURPOSE OF CREATING A DEMO APP
        # FOR GSOC WITH GNOME 2020
        # THIS KEY WILL NOT BE USED FOR ANY OTHER PURPOSES
        self.config = Grl.Config.new("grl-youtube")
        self.config.set_api_key("AIzaSyDLRGH1fK0-hIlkuVOgi96FLeskI_BDj2k")

        self.registry.add_config(self.config)

        self.registry.connect('source-added', self.on_source_added)
        self.registry.load_all_plugins(True)
        self.caps = None
        self.options = None
        # self.source = None
        

    def resolve_cb(self, source, operation_id, media, user_data, error):
        if (error):
            print("ERROR WHILE RESOLVING")
        url = Grl.Media.get_url(media)
        print(url)

    def search_cb(self, source, browse_id, media, remaining, error):

        if (error):
            print("ERROR WHILE SEARCHING")

        if (not media):
            print("No media items found matching the text")
            return

        if (media):
            title = Grl.Media.get_title(media)
            url = Grl.Media.get_url(media)
            if (url):
                print("TITLE IS " + str(title))
                print("URL IS " + str(url))
            else:
                print("TRYING WITH SLOW KEYS")
                KEYS = [Grl.METADATA_KEY_INVALID, Grl.METADATA_KEY_URL]
                caps = Grl.Source.get_caps(source, Grl.SupportedOps.RESOLVE)
                options = Grl.OperationOptions.new(caps)
                Grl.OperationOptions.set_resolution_flags(options, Grl.ResolutionFlags.IDLE_RELAY)
                Grl.Source.resolve(source, media, KEYS, options, self.resolve_cb, None)
    
        if (remaining == 0):
            print ("SEARCH FINISHED")
        else:
            print ("RESULTS REMAINING! " + str(remaining))


    def on_source_added(self, registry, source):
        id = source.get_id()
        print("SOURCE IS " + str(id))
        if (id == "grl-youtube"):
            print("ABOVE SOURCE IS ACCEPTED!!")
            self.caps = Grl.Source.get_caps(source, Grl.SupportedOps.SEARCH)
            self.options = Grl.OperationOptions.new(self.caps)
            self.options.set_count(5)
            self.options.set_resolution_flags(Grl.ResolutionFlags.IDLE_RELAY | Grl.ResolutionFlags.FAST_ONLY)
            source.search("cars", self.METADATA_KEYS, self.options, self.search_cb, None)

j = YouTube()


    # text (str) – the text to search
    # keys ([int]) – the GLib.List of #GrlKeyID s to request
    # options (Grl.OperationOptions) – options wanted for that operation
    # callback (Grl.SourceResultCb) – the user defined callback
    # user_data (object or None) – the user data to pass in the callback
