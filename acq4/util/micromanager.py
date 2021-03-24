# -*- coding: utf-8 -*-
from __future__ import print_function
import os, sys
from acq4.util.Mutex import Mutex
import atexit
from pathlib import Path

from acq4 import CONFIGPATH
from pyqtgraph import configfile
# singleton MMCorePy instance
_mmc = None

# default location to search for micromanager
DEFAULT_MM_PATH = 'C:\\Program Files\\Micro-Manager-2.00gamma1'
default_config = "D:\\survey_software\\acq4\\config\\Survey03_no_fluidics.cfg"


class MMCWrapper:
    """Wraps MMCorePy to raise more helpfule exceptions
    """

    def __init__(self, mmc):
        self.__mmc = mmc
        self.__wrapper_cache = {}

    def __getattr__(self, name):
        attr = getattr(self.__mmc, name)
        if not callable(attr):
            return attr

        if name in self.__wrapper_cache:
            return self.__wrapper_cache[name]

        def fn(*args, **kwds):
            try:
                return attr(*args, **kwds)
            except RuntimeError as exc:
                raise RuntimeError(exc.args[0].getFullMsg() + " (calling mmc.%s)" % name)

        fn.__name__ = name + "_wrapped"
        self.__wrapper_cache[name] = fn
        return fn

def getMMConfig():
    """
        get the micromanager path and desired micromanager config file from acq4 config 
    """    
    cfPath = Path(CONFIGPATH[0]).joinpath( 'default.cfg')
    print(cfPath)
    if cfPath.exists():
        cfg = configfile.readConfigFile(str(cfPath))
        print(cfg)
        micromanager_dict = {'config_file' : 'config/'+cfg['micromanager_configfile'],
                            'micromanager_dir' : cfg['micromanager_directory']}
        return micromanager_dict
    print("Could not find config file in: %s" % CONFIGPATH)


#  slightly painful parsing of the config file here because
# the manager may not exist yet?
try:
    micromanager_settings = getMMConfig()
    path = (micromanager_settings['micromanager_dir'])
except:
    print("failed to get micromanager settings")
    path = DEFAULT_MM_PATH
    micromanager_settings = {"config_file":None}

default_config = micromanager_settings["config_file"]


def getMMCorePy(path=None, config = default_config):
    """Return a singleton MMCorePy instance that is shared by all devices for accessing micromanager.
    """
    global _mmc
    if _mmc is None:
        if path is None:
            path = DEFAULT_MM_PATH

        if not Path(path).exists():
            
            raise Exception("micromanager not found at "+DEFAULT_MM_PATH)
        print("attempting to import pymmcore")
        try:
            import pymmcore

            _mmc = MMCWrapper(pymmcore.CMMCore())

            _mmc.setDeviceAdapterSearchPaths([path])
            print("imported pymmcore")
        except ImportError:

            try:
                import MMCorePy
            except ImportError:
                if sys.platform != "win32":
                    raise
                # MM does not install itself to standard path. User should take care of this,
                # but we can make a guess..
                sys.path.append(path)
                os.environ["PATH"] = os.environ["PATH"] + ";" + path
                try:
                    import MMCorePy
                finally:
                    sys.path.pop()

            _mmc = MMCorePy.CMMCore()
        # load the system configuration...
        if config is not None:      
            print("loading config at "+config)
            now = os.getcwd()
            os.chdir(path)  
            _mmc.loadSystemConfiguration(now+os.sep+config)
            os.chdir(now)
    return _mmc

def unloadMMCore():
    print("attempting to unload Micro Manager Devices ... ")

    if "_mmc" in globals().keys():
        print("Unloading All Micro Manager Devices")
        mmc = getMMCorePy()
        return mmc.unloadAllDevices()
    else:
        print("Nothing left to unload")
        return None
        
atexit.register(unloadMMCore)