import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Grl', '0.3')
from gi.repository import Gtk, Gdk, Grl, GObject, GLib
from gi.repository import Gio


class YouTube(GObject.GObject):

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

        self.caps = None
        self.options = None
        self.source = None
        self.query = None
        self.search_list = []

    def query_triggered(self, query):
        self.query = query
        self.registry.connect('source-added', self.on_source_added)
        self.registry.load_all_plugins(True)
        return self.return_title_list()

    def return_title_list(self):
        return self.search_list

    # def resolve_cb(self, source, operation_id, media, user_data, error):
    #     if (error):
    #         print("ERROR WHILE RESOLVING")
        
    #     url = media.get_url()
    #     print(url)
    #     exit()

    # def search_cb(self, source, browse_id, media, remaining, user_data, error):

    #     if (error):
    #         print("ERROR WHILE SEARCHING")

    #     if (not media):
    #         print("No media items found matching the text")
    #         return

    #     if (media):
    #         title = media.get_title()
    #         url = media.get_url()
    #         if (title):
    #             print("TITLE IS " + str(title))
            
    #         if (url):
    #             print("URL IS " + str(url))

    #         else:
    #             print("TRYING WITH SLOW KEYS")
    #             KEYS = [Grl.METADATA_KEY_URL, Grl.METADATA_KEY_INVALID]
    #             caps = self.source.get_caps(Grl.SupportedOps.RESOLVE)
    #             options = Grl.OperationOptions.new(caps)
    #             options.set_resolution_flags(Grl.ResolutionFlags.IDLE_RELAY)
    #             source.resolve(media, KEYS, options, self.resolve_cb, None)
    #             pass
    #     if (remaining == 0):
    #         print("SEARCH FINISHED")
    #         self.return_title_list()
    #     else:
    #         print ("RESULTS REMAINING! " + str(remaining))


    def on_source_added(self, registry, source):
        self.source = source
        id = self.source.get_id()
        if (id == "grl-youtube"):
            self.caps = self.source.get_caps(Grl.SupportedOps.SEARCH)
            self.options = Grl.OperationOptions.new(self.caps)
            self.options.set_count(10)
            self.options.set_resolution_flags(Grl.ResolutionFlags.IDLE_RELAY | Grl.ResolutionFlags.FAST_ONLY)
            media_list = self.source.search_sync(self.query, self.METADATA_KEYS, self.options)
            for m in media_list:
                self.search_list.append(m.get_title())
        return
