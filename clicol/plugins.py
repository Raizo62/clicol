from __future__ import print_function
from __future__ import unicode_literals

import sys
from pkg_resources import iter_entry_points
PY3 = sys.version_info.major == 3


class Plugins:
    #  Registered plugins
    registered = list()
    #  To process plugins
    active = list()
    debug = False
    keybinds = dict()
    tests = list()

    def __init__(self, debug=False, setup=(None, None)):
        self.debug = debug
        (pluginsetups, colormap) = setup
        for entrypoint in iter_entry_points('clicol.plugins'):
            plugin = entrypoint.load()
            #  Plugins have to have a section in plugins.cfg
            if pluginsetups.has_section(entrypoint.name.lower()):
                pluginsetup = dict(pluginsetups.items(entrypoint.name.lower()))
                if 'active' in pluginsetup.keys():
                    if not pluginsetup['active'] in ['1', 'True', 'true', 'yes', 'Yes', 'On', 'on']:
                        continue
                #  Register plugins
                self.register(plugin((pluginsetup, colormap)))
        return


    'Run active plugins'
    def preprocess(self, input, effects = []):
        for plugin in self.active:
            try:
                input = plugin.plugin_preprocess(input, effects)
            except AttributeError:
                pass
        return input

    'Run active plugins'
    def postprocess(self, input, effects = []):
        for plugin in self.active:
            try:
                input = plugin.plugin_postprocess(input, effects)
            except AttributeError:
                pass
        return input

    def register(self, plugin):
        try:
            self.registered.append(plugin)
            if self.debug: print("Plugin %s registered" % plugin)
            if plugin.loadonstart:
                self.active.append(plugin)
                try:
                    for key in plugin.keybinds:
                        self.keybinds[key] = plugin
                    self.tests.append(plugin.plugin_test)
                except AttributeError:
                    pass
        except:
            pass

    def tests(self):
        input = ""
        for plugin in self.active:
            try:
                input += ": ".join(plugin.plugin_test())
                input += "\r\n" * 2
            except AttributeError:
                pass
        return inputtext.encode('utf-8').decode('unicode_escape') if PY3 else inputtext
