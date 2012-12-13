import time
import traceback
import sys, os

if __name__ == "__main__":
    #import os.path as osp
    d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path = [os.path.join(d,'lib','util')] + sys.path + [d]

from PyQt4 import QtGui, QtCore
import LogWidgetTemplate
from pyqtgraph import FeedbackButton
import configfile
from DataManager import DirHandle
from HelpfulException import HelpfulException
from Mutex import Mutex
import numpy as np
from pyqtgraph import FileDialog
from debug import printExc
import weakref
import re

#from lib.Manager import getManager

#WIN = None

Stylesheet = """
    body {color: #000; font-size: 11pt; font-family: sans;}
    .entry {}
    .error .message {color: #900}
    .warning .message {color: #740}
    .user .message {color: #009}
    .status .message {color: #090}
    .logExtra {margin-left: 40px;}
    .traceback {color: #555; font-size: 10pt; height: 0px;}
    .timestamp {color: #000;}
"""

pageTemplate = """
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <style type="text/css">
%s    </style>
    
    <script type="text/javascript">
        function showDiv(id) {
            div = document.getElementById(id);
            div.style.visibility = "visible";
            div.style.height = "auto";
        }
    </script>
</head>
<body>
</body>
</html>
""" % Stylesheet



class LogButton(FeedbackButton):

    def __init__(self, *args):
        FeedbackButton.__init__(self, *args)

        global WIN
        self.clicked.connect(WIN.show)
        WIN.buttons.append(weakref.ref(self))
    
    #def close(self):
        #global WIN
        #WIN.buttons.remove(self)

class LogWindow(QtGui.QMainWindow):
    

    """LogWindow contains a LogWidget inside a window. LogWindow is responsible for collecting messages generated by the program/user, formatting them into a nested dictionary,
    and saving them in a log.txt file. The LogWidget takes care of displaying messages.
    
    Messages can be logged by calling logMsg or logExc functions from lib.Manager. These functions call the LogWindow.logMsg and LogWindow.logExc functions, but other classes 
    should not call the LogWindow functions directly.
    
    """
    sigLogMessage = QtCore.Signal(object)
    
    def __init__(self, manager):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("Log")
        path = os.path.dirname(__file__)
        self.setWindowIcon(QtGui.QIcon(os.path.join(path, 'logIcon.png')))
        self.wid = LogWidget(self, manager)
        self.wid.ui.input = QtGui.QLineEdit()
        self.wid.ui.gridLayout.addWidget(self.wid.ui.input, 2, 0, 1, 3)
        self.wid.ui.dirLabel.setText("Current Storage Directory: None")
        self.setCentralWidget(self.wid)
        self.resize(1000, 500)
        self.manager = manager
        #global WIN
        global WIN
        WIN = self
        self.msgCount = 0
        self.logCount=0
        self.logFile = None
        configfile.writeConfigFile('', self.fileName())  ## start a new temp log file, destroying anything left over from the last session.
        self.buttons = [] ## weak references to all Log Buttons get added to this list, so it's easy to make them all do things, like flash red.
        self.lock = Mutex()
        self.errorDialog = ErrorDialog()
        
        self.wid.ui.input.returnPressed.connect(self.textEntered)
        self.sigLogMessage.connect(self.queuedLogMsg, QtCore.Qt.QueuedConnection)
        
        #self.sigDisplayEntry.connect(self.displayEntry)

    def queuedLogMsg(self, args):  ## called indirectly when logMsg is called from a non-gui thread
        self.logMsg(*args[0], **args[1])
        
    def logMsg(self, msg, importance=5, msgType='status', **kwargs):
        """msg: the text of the log message
           msgTypes: user, status, error, warning (status is default)
           importance: 0-9 (0 is low importance, 9 is high, 5 is default)
           other keywords:
              exception: a tuple (type, exception, traceback) as returned by sys.exc_info()
              docs: a list of strings where documentation related to the message can be found
              reasons: a list of reasons (as strings) for the message
              traceback: a list of formatted callstack/trackback objects (formatting a traceback/callstack returns a list of strings), usually looks like [['line 1', 'line 2', 'line3'], ['line1', 'line2']]
           Feel free to add your own keyword arguments. These will be saved in the log.txt file, but will not affect the content or way that messages are displayed.
        """

        ## for thread-safetyness:
        isGuiThread = QtCore.QThread.currentThread() == QtCore.QCoreApplication.instance().thread()
        if not isGuiThread:
            self.sigLogMessage.emit(((msg, importance, msgType), kwargs))
            return
        
        try:
            currentDir = self.manager.getCurrentDir()
        except:
            currentDir = None
        if isinstance(currentDir, DirHandle):
            kwargs['currentDir'] = currentDir.name()
        else:
            kwargs['currentDir'] = None
        
        now = str(time.strftime('%Y.%m.%d %H:%M:%S'))
        name = 'LogEntry_' + str(self.msgCount)
        self.msgCount += 1
        entry = {
            #'docs': None,
            #'reasons': None,
            'message': msg,
            'timestamp': now,
            'importance': importance,
            'msgType': msgType,
            #'exception': exception,
            'id': self.msgCount,
        }
        for k in kwargs:
            entry[k] = kwargs[k]
            
        self.processEntry(entry)
        
        ## Allow exception to override values in the entry
        if entry.get('exception', None) is not None and 'msgType' in entry['exception']:
            entry['msgType'] = entry['exception']['msgType']
        
        self.saveEntry({name:entry})
        self.wid.addEntry(entry) ## takes care of displaying the entry if it passes the current filters on the logWidget
        #self.wid.displayEntry(entry)
        
        if entry['msgType'] == 'error':
            if self.errorDialog.show(entry) is False:
                self.flashButtons()
        
    def logExc(self, *args, **kwargs):
        """Calls logMsg, but adds in the current exception and callstack. Must be called within an except block, and should only be called if the exception is not re-raised. Unhandled exceptions, or exceptions that reach the top of the callstack are automatically logged, so logging an exception that will be re-raised can cause the exception to be logged twice. Takes the same arguments as logMsg."""
        kwargs['exception'] = sys.exc_info()
        kwargs['traceback'] = traceback.format_stack()[:-2] + ["------- exception caught ---------->\n"]
        self.logMsg(*args, **kwargs)
        
    def processEntry(self, entry):
        ## pre-processing common to saveEntry and displayEntry

        ## convert exc_info to serializable dictionary
        if entry.get('exception', None) is not None:
            exc_info = entry.pop('exception')
            entry['exception'] = self.exceptionToDict(*exc_info, topTraceback=entry.get('traceback', []))
        else:
            entry['exception'] = None

        
    def textEntered(self):
        msg = unicode(self.wid.ui.input.text())
        if msg == '!!':
            self.makeError1()
        elif msg == '##':
            self.makeErrorLogExc()
        try:
            currentDir = self.manager.getCurrentDir()
        except:
            currentDir = None
        self.logMsg(msg, importance=8, msgType='user', currentDir=currentDir)
        self.wid.ui.input.clear()

    
    def exceptionToDict(self, exType, exc, tb, topTraceback):
        #lines = (traceback.format_stack()[:-skip] 
            #+ ["  ---- exception caught ---->\n"] 
            #+ traceback.format_tb(sys.exc_info()[2])
            #+ traceback.format_exception_only(*sys.exc_info()[:2]))
        #print topTraceback
        excDict = {}
        excDict['message'] = traceback.format_exception(exType, exc, tb)[-1][:-1] 
        excDict['traceback'] = topTraceback + traceback.format_exception(exType, exc, tb)[:-1]
        if hasattr(exc, 'docs'):
            if len(exc.docs) > 0:
                excDict['docs'] = exc.docs
        if hasattr(exc, 'reasons'):
            if len(exc.reasons) > 0:
                excDict['reasons'] = exc.reasons
        if hasattr(exc, 'kwargs'):
            for k in exc.kwargs:
                excDict[k] = exc.kwargs[k]
        if hasattr(exc, 'oldExc'):
            excDict['oldExc'] = self.exceptionToDict(*exc.oldExc, topTraceback=[])
        return excDict
    
    def flashButtons(self):
        for b in self.buttons:
            if b() is not None:
                b().failure(tip='An error occurred. Please see the log.', limitedTime = False)
    
    def resetButtons(self):
        for b in self.buttons:
            if b() is not None:
                b().reset()
            #try:
                #b.reset()
            #except RuntimeError:
                #self.buttons.remove(b)
                #print "Removed a logButton from logWindow's list. button:", b
    
    
    def makeError1(self):
        try:
            self.makeError2()
            #print x
        except:
            t, exc, tb = sys.exc_info()
            #logExc(message="This button doesn't work", reasons='reason a, reason b', docs='documentation')
            #if isinstance(exc, HelpfulException):
                #exc.prependErr("Button doesn't work", (t,exc,tb), reasons = ["It's supposed to raise an error for testing purposes", "You're doing it wrong."])
                #raise
            #else:
            raise HelpfulException(message='This button does not work.', exc=(t, exc, tb), reasons=["It's supposed to raise an error for testing purposes", "You're doing it wrong."])
    
    def makeErrorLogExc(self):
        try:
            print y
        except:
            self.logExc('This is the message sent to logExc', msgType='error')
    
    def makeError2(self):
        try:
            print y
        except:
            t, exc, tb = sys.exc_info()
            raise HelpfulException(message='msg from makeError', exc=(t, exc, tb), reasons=["reason one", "reason 2"], docs=['what, you expect documentation?'])
    
    def show(self):
        QtGui.QMainWindow.show(self)
        self.activateWindow()
        self.raise_()
        self.resetButtons()
    
    def fileName(self):
        ## return the log file currently used
        if self.logFile is None:
            return "tempLog.txt"
        else:
            return self.logFile.name()
        
    def setLogDir(self, dh):
        if self.fileName() == dh.name():
            return
        
        oldfName = self.fileName()
        if self.logFile is not None:
            self.logMsg('Moving log storage to %s.' % (self.logFile.name(relativeTo=self.manager.baseDir))) ## make this note before we change the log file, so when a log ends, you know where it went after.
        
        self.logMsg('Moving log storage to %s.' % (dh.name(relativeTo=self.manager.baseDir))) ## make this note before we change the log file, so when a log ends, you know where it went after.
        
        if oldfName == 'tempLog.txt':
            with self.lock:
                temp = configfile.readConfigFile(oldfName)
        else:
            temp = {}
                
        if dh.exists('log.txt'):
            self.logFile = dh['log.txt']
            with self.lock:
                self.msgCount = len(configfile.readConfigFile(self.logFile.name()))
            newTemp = {}
            for v in temp.values():
                self.msgCount += 1
                newTemp['LogEntry_'+str(self.msgCount)] = v
            self.saveEntry(newTemp)
        else:
            self.logFile = dh.createFile('log.txt')
            self.saveEntry(temp)
        
        self.logMsg('Moved log storage from %s to %s.' % (oldfName, self.fileName()))
        self.wid.ui.dirLabel.setText("Current Storage Directory: " + self.fileName())
        self.manager.sigLogDirChanged.emit(dh)
    
    def getLogDir(self):
        if self.logFile is None:
            return None
        else:
            return self.logFile.parent()
    
    def saveEntry(self, entry):  
        with self.lock:
            configfile.appendConfigFile(entry, self.fileName())
    
    def disablePopups(self, disable):
        self.errorDialog.disable(disable)


class LogWidget(QtGui.QWidget):
    
    sigDisplayEntry = QtCore.Signal(object) ## for thread-safetyness
    sigAddEntry = QtCore.Signal(object) ## for thread-safetyness
    
    def __init__(self, parent, manager):
        QtGui.QWidget.__init__(self, parent)
        self.ui = LogWidgetTemplate.Ui_Form()
        self.manager = manager
        self.ui.setupUi(self)
        #self.ui.input.hide()
        self.ui.filterTree.topLevelItem(1).setExpanded(True)
        
        self.entries = [] ## stores all log entries in memory
        self.cache = {} ## for storing html strings of entries that have already been processed
        self.displayedEntries = []
        #self.currentEntries = None ## recordArray that stores currently displayed entries -- so that if filters get more restrictive we can just refilter this list instead of filtering everything
        self.typeFilters = []
        self.importanceFilter = 0
        self.dirFilter = False
        self.entryArrayBuffer = np.zeros(1000, dtype=[ ### a record array for quick filtering of entries
            ('index', 'int32'),
            ('importance', 'int32'),
            ('msgType', '|S10'),
            ('directory', '|S100'),
            ('entryId', 'int32')
        ])
        self.entryArray = self.entryArrayBuffer[:0]
        
        self.filtersChanged()
        
        self.sigDisplayEntry.connect(self.displayEntry, QtCore.Qt.QueuedConnection)
        self.sigAddEntry.connect(self.addEntry, QtCore.Qt.QueuedConnection)
        self.ui.exportHtmlBtn.clicked.connect(self.exportHtml)
        self.ui.filterTree.itemChanged.connect(self.setCheckStates)
        self.ui.importanceSlider.valueChanged.connect(self.filtersChanged)
        #self.ui.logView.linkClicked.connect(self.linkClicked)
        self.ui.output.anchorClicked.connect(self.linkClicked)
        
        #page = self.ui.logView.page()
        #page.setLinkDelegationPolicy(page.DelegateAllLinks)
        
    def loadFile(self, f):
        """Load the file, f. f must be able to be read by configfile.py"""
        log = configfile.readConfigFile(f)
        self.entries = []
        self.entryArrayBuffer = np.zeros(len(log),dtype=[
            ('index', 'int32'),
            ('importance', 'int32'),
            ('msgType', '|S10'),
            ('directory', '|S100'),
            ('entryId', 'int32')
        ])
        self.entryArray = self.entryArrayBuffer[:]
                                   
        i = 0
        for k,v in log.iteritems():
            v['id'] = k[9:]  ## record unique ID to facilitate HTML generation (javascript needs this ID)
            self.entries.append(v)
            self.entryArray[i] = np.array([(i, v.get('importance', 5), v.get('msgType', 'status'), v.get('currentDir', ''), v.get('entryId', v['id']))], dtype=[('index', 'int32'), ('importance', 'int32'), ('msgType', '|S10'), ('directory', '|S100'), ('entryId', 'int32')])
            i += 1
            
        self.filterEntries() ## puts all entries through current filters and displays the ones that pass
        
    def addEntry(self, entry):
        ## All incoming messages begin here

        ## for thread-safetyness:
        isGuiThread = QtCore.QThread.currentThread() == QtCore.QCoreApplication.instance().thread()
        if not isGuiThread:
            self.sigAddEntry.emit(entry)
            return
        
        self.entries.append(entry)
        i = len(self.entryArray)
        
        entryDir = entry.get('currentDir', None)
        if entryDir is None:
            entryDir = ''
            
        arr = np.array([(i, entry['importance'], entry['msgType'], entryDir, entry['id'])], dtype = [('index', 'int32'), ('importance', 'int32'), ('msgType', '|S10'), ('directory', '|S100'), ('entryId', 'int32')])
        
        ## make more room if needed
        if len(self.entryArrayBuffer) == len(self.entryArray):
            newArray = np.empty(len(self.entryArrayBuffer)+1000, self.entryArrayBuffer.dtype)
            newArray[:len(self.entryArray)] = self.entryArray
            self.entryArrayBuffer = newArray
        self.entryArray = self.entryArrayBuffer[:len(self.entryArray)+1]
        #self.entryArray[i] = [(i, entry['importance'], entry['msgType'], entry['currentDir'])]
        self.entryArray[i] = arr
        self.checkDisplay(entry) ## displays the entry if it passes the current filters
        #np.append(self.entryArray, np.array(i, [[i, entry['importance'], entry['msgType'], entry['currentDir']]]), dtype = [('index', int), ('importance', int), ('msgType', str), ('directory', str)])




    def setCheckStates(self, item, column):
        if item == self.ui.filterTree.topLevelItem(1):
            if item.checkState(0):
                for i in range(item.childCount()):
                    item.child(i).setCheckState(0, QtCore.Qt.Checked)
        elif item.parent() == self.ui.filterTree.topLevelItem(1):
            if not item.checkState(0):
                self.ui.filterTree.topLevelItem(1).setCheckState(0, QtCore.Qt.Unchecked)
        self.filtersChanged()
        
    def filtersChanged(self):
        ### Update self.typeFilters, self.importanceFilter, and self.dirFilter to reflect changes.
        tree = self.ui.filterTree
        
        self.typeFilters = []
        for i in range(tree.topLevelItem(1).childCount()):
            child = tree.topLevelItem(1).child(i)
            if tree.topLevelItem(1).checkState(0) or child.checkState(0):
                text = child.text(0)
                self.typeFilters.append(unicode(text))
            
        self.importanceFilter = self.ui.importanceSlider.value()
    
        self.updateDirFilter()
            #self.dirFilter = self.manager.getDirOfSelectedFile().name()
        #else:
            #self.dirFilter = False
            
        self.filterEntries()
        
    def updateDirFilter(self, dh=None):
        if self.ui.filterTree.topLevelItem(0).checkState(0):
            if dh==None:
                self.dirFilter = self.manager.getDirOfSelectedFile().name()
            else:
                self.dirFilter = dh.name()
        else:
            self.dirFilter = False
        
    
        
    def filterEntries(self):
        """Runs each entry in self.entries through the filters and displays if it makes it through."""
        ### make self.entries a record array, then filtering will be much faster (to OR true/false arrays, + them)
        typeMask = self.entryArray['msgType'] == ''
        for t in self.typeFilters:
            typeMask += self.entryArray['msgType'] == t
        mask = (self.entryArray['importance'] > self.importanceFilter) * typeMask
        if self.dirFilter != False:
            d = np.ascontiguousarray(self.entryArray['directory'])
            j = len(self.dirFilter)
            i = len(d)
            d = d.view(np.byte).reshape(i, 100)[:, :j]
            d = d.reshape(i*j).view('|S%d' % j)
            mask *= (d == self.dirFilter)
            
            
        self.ui.output.clear()
        global Stylesheet
        self.ui.output.document().setDefaultStyleSheet(Stylesheet)
        #global pageTemplate
        #self.ui.logView.setHtml(pageTemplate)
        indices = list(self.entryArray[mask]['index'])
        inds = indices
        
        #if self.dirFilter != False:
            #j = len(self.dirFilter)
            #for i, n in inds:
                #if not self.entries[n]['currentDir'][:j] == self.dirFilter:
                    #indices.pop(i)
                    
        self.displayEntry([self.entries[i] for i in indices])
                          
    def checkDisplay(self, entry):
        ### checks whether entry passes the current filters and displays it if it does.
        if entry['msgType'] not in self.typeFilters:
            return
        elif entry['importance'] < self.importanceFilter:
            return
        elif self.dirFilter is not False:
            if entry['currentDir'][:len(self.dirFilter)] != self.dirFilter:
                return
        else:
            self.displayEntry([entry])
    
        
    def displayEntry(self, entries):
        ## entries should be a list of log entries
        
        ## for thread-safetyness:
        isGuiThread = QtCore.QThread.currentThread() == QtCore.QCoreApplication.instance().thread()
        if not isGuiThread:
            self.sigDisplayEntry.emit(entries)
            return
        
        for entry in entries:
            if not self.cache.has_key(id(entry)):
                self.cache[id(entry)] = self.generateEntryHtml(entry)
                
                ## determine message color:
                #if entry['msgType'] == 'status':
                    #color = 'green'
                #elif entry['msgType'] == 'user':
                    #color = 'blue'
                #elif entry['msgType'] == 'error':
                    #color = 'red'
                #elif entry['msgType'] == 'warning':
                    #color = '#DD4400' ## orange
                #else:
                    #color = 'black'
                    
                #if entry.has_key('exception') or entry.has_key('docs') or entry.has_key('reasons'):
                    ##self.displayComplexMessage(entry, color)
                    #self.displayComplexMessage(entry)
                #else: 
                    #self.displayText(entry['message'], entry, color, timeStamp=entry['timestamp'])
                    
            #for x in self.cache[id(entry)]:
                #self.ui.output.appendHtml(x)
                
            html = self.cache[id(entry)]
            #frame = self.ui.logView.page().currentFrame()
            #isMax = frame.scrollBarValue(QtCore.Qt.Vertical) == frame.scrollBarMaximum(QtCore.Qt.Vertical)
            sb = self.ui.output.verticalScrollBar()
            isMax = sb.value() == sb.maximum()
            
            #frame.findFirstElement('body').appendInside(html)
            self.ui.output.append(html)
            self.displayedEntries.append(entry)
            
            if isMax:
                QtGui.QApplication.processEvents()  ## can't scroll to end until the web frame has processed the html change
                self.ui.output.scrollToAnchor(str(entry['id']))
                #frame.setScrollBarValue(QtCore.Qt.Vertical, frame.scrollBarMaximum(QtCore.Qt.Vertical))
            #self.ui.logView.update()
                
    def generateEntryHtml(self, entry):
        msg = self.cleanText(entry['message'])
        
        reasons = ""
        docs = ""
        exc = ""
        if entry.has_key('reasons'):
            reasons = self.formatReasonStrForHTML(entry['reasons'])
        if entry.has_key('docs'):
            docs = self.formatDocsStrForHTML(entry['docs'])
        if entry.get('exception', None) is not None:
            exc = self.formatExceptionForHTML(entry, entryId=entry['id'])
            
        extra = reasons + docs + exc
        if extra != "":
            #extra = "<div class='logExtra'>" + extra + "</div>"
            extra = "<table class='logExtra'><tr><td>" + extra + "</td></tr></table>"
        
        #return """
        #<div class='entry'>
            #<div class='%s'>
                #<span class='timestamp'>%s</span>
                #<span class='message'>%s</span>
                #%s
            #</div>
        #</div>
        #""" % (entry['msgType'], entry['timestamp'], msg, extra)
        return """
        <a name="%s"/><table class='entry'><tr><td>
            <table class='%s'><tr><td>
                <span class='timestamp'>%s</span>
                <span class='message'>%s</span>
                %s
            </td></tr></table>
        </td></tr></table>
        """ % (str(entry['id']), entry['msgType'], entry['timestamp'], msg, extra)
        
        
        #if entry.has_key('exception') or entry.has_key('docs') or entry.has_key('reasons'):
            ##self.displayComplexMessage(entry, color)
            #return self.generateComplex(entry)
        #else: 
            #return self.generateSimple(entry['message'], entry, color, timeStamp=entry['timestamp'])
            ##self.displayText(entry['message'], entry, color, timeStamp=entry['timestamp'])
    
    @staticmethod
    def cleanText(text):
        text = re.sub(r'&', '&amp;', text)
        text = re.sub(r'>','&gt;', text)
        text = re.sub(r'<', '&lt;', text)
        text = re.sub(r'\n', '<br/>\n', text)
        return text




    #def displayText(self, msg, entry, colorStr='black', timeStamp=None, clean=True):
        #if clean:
            #msg = self.cleanText(msg)
        
        #if msg[-1:] == '\n':
            #msg = msg[:-1]     
        #msg = '<br />'.join(msg.split('\n'))
        #if timeStamp is not None:
            #strn = '<b style="color:black"> %s </b> <span style="color:%s"> %s </span>' % (timeStamp, colorStr, msg) 
        #else:
            #strn = '<span style="color:%s"> %s </span>' % (colorStr, msg)
        ##self.ui.output.appendHtml(strn)
        #self.cache[id(entry)].append(strn)
            


    #def displayComplexMessage(self, entry, color='black'):
        #self.displayText(entry['message'], entry, color, timeStamp = entry['timestamp'], clean=True)
        #if entry.has_key('reasons'):
            #reasons = self.formatReasonStrForHTML(entry['reasons'])
            #self.displayText(reasons, entry, 'black', clean=False)
        #if entry.has_key('docs'):
            #docs = self.formatDocsStrForHTML(entry['docs'])
            #self.displayText(docs, entry, 'black', clean=False)
        #if entry.get('exception', None) is not None:
            #self.displayException(entry['exception'], entry, 'black', tracebacks=entry.get('traceback', None))
            

    
    def formatExceptionForHTML(self, entry, exception=None, count=1, entryId=None):
        ### Here, exception is a dict that holds the message, reasons, docs, traceback and oldExceptions (which are also dicts, with the same entries)
        ## the count and tracebacks keywords are for calling recursively
        if exception is None:
            exception = entry['exception']
        #if tracebacks is None:
            #tracebacks = []
            
        indent = 10
        
        text = self.cleanText(exception['message'])
        text = re.sub(r'^HelpfulException: ', '', text)
        #if exception.has_key('oldExc'):  
            #self.displayText("&nbsp;"*indent + str(count)+'. ' + text, entry, color, clean=False)
        #else:
            #self.displayText("&nbsp;"*indent + str(count)+'. Original error: ' + text, entry, color, clean=False)
        messages = [text]
        #print "\n", messages, "\n"
        
        if exception.has_key('reasons'):
            reasons = self.formatReasonsStrForHTML(exception['reasons'])
            text += reasons
            #self.displayText(reasons, entry, color, clean=False)
        if exception.has_key('docs'):
            docs = self.formatDocsStrForHTML(exception['docs'])
            #self.displayText(docs, entry, color, clean=False)
            text += docs
        
        traceback = [self.formatTracebackForHTML(exception['traceback'], count)]
        text = [text]
        
        if exception.has_key('oldExc'):
            exc, tb, msgs = self.formatExceptionForHTML(entry, exception['oldExc'], count=count+1)
            text.extend(exc)
            messages.extend(msgs)
            traceback.extend(tb)
            
        #else:
            #if len(tracebacks)==count+1:
                #n=0
            #else: 
                #n=1
            #for i, tb in enumerate(tracebacks):
                #self.displayTraceback(tb, entry, number=i+n)
        if count == 1:
            exc = "<div class=\"exception\"><ol>" + "\n".join(["<li>%s</li>" % ex for ex in text]) + "</ol></div>"
            tbStr = "\n".join(["<li><b>%s</b><br/><span class='traceback'>%s</span></li>" % (messages[i], tb) for i,tb in enumerate(traceback)])
            #traceback = "<div class=\"traceback\" id=\"%s\"><ol>"%str(entryId) + tbStr + "</ol></div>"
            entry['tracebackHtml'] = tbStr

            #return exc + '<a href="#" onclick="showDiv(\'%s\')">Show traceback</a>'%str(entryId) + traceback
            return exc + '<a href="exc:%s">Show traceback %s</a>'%(str(entryId), str(entryId))
        else:
            return text, traceback, messages
        
        
    def formatTracebackForHTML(self, tb, number):
        try:
            tb = [line for line in tb if not line.startswith("Traceback (most recent call last)")]
        except:
            print "\n"+str(tb)+"\n"
            raise
        return re.sub(" ", "&nbsp;", ("").join(map(self.cleanText, tb)))[:-1]
        #tb = [self.cleanText(strip(x)) for x in tb]
        #lines = []
        #prefix = ''
        #for l in ''.join(tb).split('\n'):
            #if l == '':
                #continue
            #if l[:9] == "Traceback":
                #prefix = ' ' + str(number) + '. '
                #continue
            #spaceCount = 0
            #while l[spaceCount] == ' ':
                #spaceCount += 1
            #if prefix is not '':
                #spaceCount -= 1
            #lines.append("&nbsp;"*(spaceCount*4) + prefix + l)
            #prefix = ''
        #return '<div class="traceback">' + '<br />'.join(lines) + '</div>'
        #self.displayText('<br />'.join(lines), entry, color, clean=False)
        
    def formatReasonsStrForHTML(self, reasons):
        #indent = 6
        reasonStr = "<table class='reasons'><tr><td>Possible reasons include:\n<ul>\n"
        for r in reasons:
            r = self.cleanText(r)
            reasonStr += "<li>" + r + "</li>\n"
            #reasonStr += "&nbsp;"*22 + chr(97+i) + ". " + r + "<br>"
        reasonStr += "</ul></td></tr></table>\n"
        return reasonStr
    
    def formatDocsStrForHTML(self, docs):
        #indent = 6
        docStr = "<div class='docRefs'>Relevant documentation:\n<ul>\n"
        for d in docs:
            d = self.cleanText(d)
            docStr += "<li><a href=\"doc:%s\">%s</a></li>\n" % (d, d)
        docStr += "</ul></div>\n"
        return docStr
    
    def exportHtml(self, fileName=False):
        #self.makeError1()
        if fileName is False:
            self.fileDialog = FileDialog(self, "Save HTML as...", self.manager.getCurrentDir().name())
            #self.fileDialog.setFileMode(QtGui.QFileDialog.AnyFile)
            self.fileDialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
            self.fileDialog.show()
            self.fileDialog.fileSelected.connect(self.exportHtml)
            return
        if fileName[-5:] != '.html':
            fileName += '.html'
            
        #doc = self.ui.output.document().toHtml('utf-8')
        #for e in self.displayedEntries:
            #if e.has_key('tracebackHtml'):
                #doc = re.sub(r'<a href="exc:%s">(<[^>]+>)*Show traceback %s(<[^>]+>)*</a>'%(str(e['id']), str(e['id'])), e['tracebackHtml'], doc)
                
        global pageTemplate
        doc = pageTemplate
        for e in self.displayedEntries:
            doc += self.cache[id(e)]
        for e in self.displayedEntries:
            if e.has_key('tracebackHtml'):
                doc = re.sub(r'<a href="exc:%s">(<[^>]+>)*Show traceback %s(<[^>]+>)*</a>'%(str(e['id']), str(e['id'])), e['tracebackHtml'], doc)
            
            
        
        #doc = self.ui.logView.page().currentFrame().toHtml()
        f = open(fileName, 'w')
        f.write(doc.encode('utf-8'))
        f.close()
        
        
    
    def makeError1(self):
        ### just for testing error logging
        try:
            self.makeError2()
            #print x
        except:
            t, exc, tb = sys.exc_info()
            #logExc(message="This button doesn't work", reasons='reason a, reason b', docs='documentation')
            #if isinstance(exc, HelpfulException):
                #exc.prependErr("Button doesn't work", (t,exc,tb), reasons = ["It's supposed to raise an error for testing purposes", "You're doing it wrong."])
                #raise
            #else:
            printExc("This is the message sent to printExc.")
            #raise HelpfulException(message='This button does not work.', exc=(t, exc, tb), reasons=["It's supposed to raise an error for testing purposes", "You're doing it wrong."])
    
    def makeError2(self):
        ### just for testing error logging
        try:
            print y
        except:
            t, exc, tb = sys.exc_info()
            raise HelpfulException(message='msg from makeError', exc=(t, exc, tb), reasons=["reason one", "reason 2"], docs=['what, you expect documentation?'])

    def linkClicked(self, url):
        url = url.toString()
        if url[:4] == 'doc:':
            self.manager.showDocumentation(url[4:].lower())
        elif url[:4] == 'exc:':
            cursor = self.ui.output.document().find('Show traceback %s' % url[4:])
            try:
                tb = self.entries[int(url[4:])-1]['tracebackHtml']
            except IndexError:
                try:
                    tb = self.entries[self.entryArray[self.entryArray['entryId']==(int(url[4:]))]['index']]['tracebackHtml']
                except:
                    print "requested index %d, but only %d entries exist." % (int(url[4:])-1, len(self.entries))
                    raise
            cursor.insertHtml(tb)

    def clear(self):
        #self.ui.logView.setHtml("")
        self.ui.output.clear()
        self.displayedEntryies = []

        
        
class ErrorDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        #self.setModal(False)
        self.setWindowFlags(QtCore.Qt.Window)
        #self.setWindowModality(QtCore.Qt.NonModal)
        self.setWindowTitle('ACQ4 Error')
        self.layout = QtGui.QVBoxLayout()
        self.layout.setContentsMargins(3,3,3,3)
        self.setLayout(self.layout)
        self.messages = []
        
        self.msgLabel = QtGui.QLabel()
        #self.msgLabel.setWordWrap(False)
        #self.msgLabel.setMaximumWidth(800)
        self.msgLabel.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #self.msgLabel.setFrameStyle(QtGui.QFrame.Box)
        #self.msgLabel.setStyleSheet('QLabel { font-weight: bold }')
        self.layout.addWidget(self.msgLabel)
        self.msgLabel.setMaximumWidth(800)
        self.msgLabel.setMinimumWidth(500)
        self.msgLabel.setWordWrap(True)
        self.layout.addStretch()
        self.disableCheck = QtGui.QCheckBox('Disable error message popups')
        self.layout.addWidget(self.disableCheck)
        
        self.btnLayout = QtGui.QHBoxLayout()
        self.btnLayout.addStretch()
        self.okBtn = QtGui.QPushButton('OK')
        self.btnLayout.addWidget(self.okBtn)
        self.nextBtn = QtGui.QPushButton('Show next error')
        self.btnLayout.addWidget(self.nextBtn)
        self.nextBtn.hide()
        self.logBtn = QtGui.QPushButton('Show Log...')
        self.btnLayout.addWidget(self.logBtn)
        self.btnLayoutWidget = QtGui.QWidget()
        self.layout.addWidget(self.btnLayoutWidget)
        self.btnLayoutWidget.setLayout(self.btnLayout)
        self.btnLayout.addStretch()
        
        self.okBtn.clicked.connect(self.okClicked)
        self.nextBtn.clicked.connect(self.nextMessage)
        self.logBtn.clicked.connect(self.logClicked)
        
        
    def show(self, entry):
        ## rules are:
        ##   - Try to show friendly error messages
        ##   - If there are any helpfulExceptions, ONLY show those
        ##     otherwise, show everything
        self.lastEntry = entry
        
        ## extract list of exceptions
        exceptions = []
        #helpful = []
        key = 'exception'
        exc = entry
        while key in exc:
            exc = exc[key]
            
            ## ignore this error if it was generated on the command line.
            if 'File "<stdin>"' in exc.get('traceback', ['',''])[1]:
                return False
            
            if exc is None:
                break
            key = 'oldExc'
            if exc['message'].startswith('HelpfulException'):
                exceptions.append('<b>' + self.cleanText(re.sub(r'^HelpfulException: ', '', exc['message'])) + '</b>')
            elif exc['message'] == 'None':
                continue
            else:
                exceptions.append(self.cleanText(exc['message']))
                
        msg = "<br>".join(exceptions)
        #if len(helpful) > 0:
            #msg = '<b>' + '<br>'.join(helpful) + '</b>'
        #else:
            #msg = '<b>' + entry['message'] + '</b><br>' + '<br>'.join(exceptions)
        
        
        if self.disableCheck.isChecked():
            return False
        if self.isVisible():
            self.messages.append(msg)
            self.nextBtn.show()
            self.nextBtn.setEnabled(True)
            self.nextBtn.setText('Show next error (%d more)' % len(self.messages))
        else:
            w = QtGui.QApplication.activeWindow()
            self.nextBtn.hide()
            self.msgLabel.setText(msg)
            self.open()
            if w is not None:
                cp = w.geometry().center()
                self.setGeometry(cp.x() - self.width()/2., cp.y() - self.height()/2., self.width(), self.height())
        #self.activateWindow()
        self.raise_()
            
    @staticmethod
    def cleanText(text):
        text = re.sub(r'&', '&amp;', text)
        text = re.sub(r'>','&gt;', text)
        text = re.sub(r'<', '&lt;', text)
        text = re.sub(r'\n', '<br/>\n', text)
        return text
        
    def closeEvent(self, ev):
        QtGui.QDialog.closeEvent(self, ev)
        self.messages = []
        
    def okClicked(self):
        self.accept()
        self.messages = []
        
    def logClicked(self):
        global WIN
        self.accept()
        WIN.show()
        self.messages = []
        
    def nextMessage(self):
        self.msgLabel.setText(self.messages.pop(0))
        self.nextBtn.setText('Show next error (%d more)' % len(self.messages))
        if len(self.messages) == 0:
            self.nextBtn.setEnabled(False)
        
    def disable(self, disable):
        self.disableCheck.setChecked(disable)
    
    
if __name__ == "__main__":
    #import sys
    #import os.path as osp
    #d = osp.dirname(osp.dirname(osp.abspath(__file__)))
    #sys.path = [osp.join(d, 'util')] + sys.path + [d]
    #from lib.util import pyqtgraph
    app = QtGui.QApplication([])
    log = LogWindow(None)
    log.show()
    original_excepthook = sys.excepthook
    
    def excepthook(*args):
        global original_excepthook
        log.displayException(*args)
        ret = original_excepthook(*args)
        sys.last_traceback = None           ## the important bit
        
    
    sys.excepthook = excepthook

    app.exec_()