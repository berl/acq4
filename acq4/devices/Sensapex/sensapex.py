# -*- coding: utf-8 -*-
import time
import numpy as np
from PyQt4 import QtGui, QtCore
from ..Stage import Stage, MoveFuture, StageInterface
from acq4.drivers.sensapex import SensapexDevice
from acq4.util.Mutex import Mutex
from acq4.util.Thread import Thread
from acq4.pyqtgraph import debug, ptime, SpinBox


class Sensapex(Stage):
    """
    A Sensapex manipulator.
    """
    def __init__(self, man, config, name):
        self.devid = config.get('deviceId')
        self.scale = config.pop('scale', (1e-9, 1e-9, 1e-9))
        self.dev = SensapexDevice(self.devid)
        self._lastMove = None
        man.sigAbortAll.connect(self.stop)

        Stage.__init__(self, man, config, name)

        # clear cached position for this device and re-read to generate an initial position update
        self._lastPos = None
        self.getPosition(refresh=True)

        # TODO: set any extra parameters specified in the config
        
        
        # thread for polling position changes
        self.monitor = MonitorThread(self)
        self.monitor.start()

    def capabilities(self):
        """Return a structure describing the capabilities of this device"""
        if 'capabilities' in self.config:
            return self.config['capabilities']
        else:
            return {
                'getPos': (True, True, True),
                'setPos': (True, True, True),
                'limits': (False, False, False),
            }

    def stop(self):
        """Stop the manipulator immediately.
        """
        with self.lock:
            self.dev.stop()
            if self._lastMove is not None:
                self._lastMove._stopped()
            self._lastMove = None

    def _getPosition(self):
        # Called by superclass when user requests position refresh
        with self.lock:
            pos = self.dev.get_pos()
            pos = [pos[i] * self.scale[i] for i in (0, 1, 2)]
            if pos != self._lastPos:
                self._lastPos = pos
                emit = True
            else:
                emit = False

        if emit:
            # don't emit signal while locked
            self.posChanged(pos)

        return pos

    def targetPosition(self):
        with self.lock:
            if self._lastMove is None or self._lastMove.isDone():
                return self.getPosition()
            else:
                return self._lastMove.targetPos

    def quit(self):
        self.monitor.stop()
        Stage.quit(self)

    def _move(self, abs, rel, speed, linear):
        with self.lock:
            if self._lastMove is not None and not self._lastMove.isDone():
                self.stop()
            pos = self._toAbsolutePosition(abs, rel)
            speed = self._interpretSpeed(speed)

            self._lastMove = SensapexMoveFuture(self, pos, speed)
            return self._lastMove

    #def deviceInterface(self, win):
        #return SensapexGUI(self, win)


class MonitorThread(Thread):
    """Thread to poll for manipulator position changes.
    """
    def __init__(self, dev):
        self.dev = dev
        self.lock = Mutex(recursive=True)
        self.stopped = False
        self.interval = 0.3
        
        Thread.__init__(self)

    def start(self):
        self.stopped = False
        Thread.start(self)

    def stop(self):
        with self.lock:
            self.stopped = True

    def setInterval(self, i):
        with self.lock:
            self.interval = i
    
    def run(self):
        minInterval = 100e-3
        interval = minInterval
        lastPos = None
        while True:
            try:
                with self.lock:
                    if self.stopped:
                        break
                    maxInterval = self.interval

                pos = self.dev._getPosition()  # this causes sigPositionChanged to be emitted
                if pos != lastPos:
                    # if there was a change, then loop more rapidly for a short time.
                    interval = minInterval
                    lastPos = pos
                else:
                    interval = min(maxInterval, interval*2)

                time.sleep(interval)
            except:
                debug.printExc('Error in Scientifica monitor thread:')
                time.sleep(maxInterval)
                

class SensapexMoveFuture(MoveFuture):
    """Provides access to a move-in-progress on a Sensapex manipulator.
    """
    def __init__(self, dev, pos, speed):
        MoveFuture.__init__(self, dev, pos, speed)
        self._interrupted = False
        self._errorMSg = None
        self._finished = False
        pos = np.array(pos) / np.array(self.dev.scale)
        self.dev.dev.goto_pos(pos, speed * 1e6)
        
    def wasInterrupted(self):
        """Return True if the move was interrupted before completing.
        """
        return self._interrupted

    def isDone(self):
        """Return True if the move is complete.
        """
        return self._getStatus() != 0

    def _getStatus(self):
        # check status of move unless we already know it is complete.
        # 0: still moving; 1: finished successfully; -1: finished unsuccessfully
        if self._finished:
            if self._interrupted:
                return -1
            else:
                return 1
        if self.dev.dev.is_busy():
            # Still moving
            return 0
        # did we reach target?
        pos = self.dev._getPosition()
        dif = ((np.array(pos) - np.array(self.targetPos))**2).sum()**0.5
        if dif < 2.5e-6:
            # reached target
            self._finished = True
            return 1
        else:
            # missed
            self._finished = True
            self._interrupted = True
            self._errorMsg = "Move did not complete (target=%s, position=%s, dif=%s)." % (self.targetPos, pos, dif)
            return -1

    def _stopped(self):
        # Called when the manipulator is stopped, possibly interrupting this move.
        status = self._getStatus()
        if status == 1:
            # finished; ignore stop
            return
        elif status == -1:
            self._errorMsg = "Move was interrupted before completion."
        elif status == 0:
            # not actually stopped! This should not happen.
            raise RuntimeError("Interrupted move but manipulator is still running!")
        else:
            raise Exception("Unknown status: %s" % status)

    def errorMessage(self):
        return self._errorMsg



#class ScientificaGUI(StageInterface):
    #def __init__(self, dev, win):
        #StageInterface.__init__(self, dev, win)

        ## Insert Scientifica-specific controls into GUI
        #self.zeroBtn = QtGui.QPushButton('Zero position')
        #self.layout.addWidget(self.zeroBtn, self.nextRow, 0, 1, 2)
        #self.nextRow += 1

        #self.psGroup = QtGui.QGroupBox('Rotary Controller')
        #self.layout.addWidget(self.psGroup, self.nextRow, 0, 1, 2)
        #self.nextRow += 1

        #self.psLayout = QtGui.QGridLayout()
        #self.psGroup.setLayout(self.psLayout)
        #self.speedLabel = QtGui.QLabel('Speed')
        #self.speedSpin = SpinBox(value=self.dev.userSpeed, suffix='m/turn', siPrefix=True, dec=True, limits=[1e-6, 10e-3])
        #self.psLayout.addWidget(self.speedLabel, 0, 0)
        #self.psLayout.addWidget(self.speedSpin, 0, 1)

        #self.zeroBtn.clicked.connect(self.dev.dev.zeroPosition)
        #self.speedSpin.valueChanged.connect(lambda v: self.dev.setDefaultSpeed(v))

