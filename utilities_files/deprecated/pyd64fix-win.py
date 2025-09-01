#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    PyD64Fix (c) 2015  Žarko Živanov

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

VERSION="1.0"

import sys
import os
import argparse

PETASCII = (" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",
            " "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",
            " ","!",'"',"#","$","%","&","'","(",")","*","+",",","-",".","/",
            "0","1","2","3","4","5","6","7","8","9",":",";","<","=",">","?",
            "@","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O",
            "P","Q","R","S","T","U","V","W","X","Y","Z","[","£","]","↑","←",
            "━","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O",
            "P","Q","R","S","T","U","V","W","X","Y","Z","┼"," ","│"," "," ",
            " "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",
            " "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",
            " "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",
            " "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",
            " "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",
            " "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",
            " "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",
            " "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ")

# converts PETASCII to ASCII
def toascii(s):
    return "".join(PETASCII[c] for c in s)

# converts bytes/string to hex numbers
def hexdata(s):
    return " ".join("{:02x}".format(c) for c in s)

# contains data for one 256-byte block
class D64Block(object):
    def __init__(self):
        self.data = None

    def __setattr__(self, name, value):
        # override assignment to make a copy
        if (name == "data") and (value != None):
            self.__dict__[name] = bytearray(value)
        else:
            super(D64Block, self).__setattr__(name, value)

    def __eq__(self, other):
        return self.data == other.data

    def __ne__(self, other):
        return self.data != other.data

    def load(self, descriptor):
        self.data = bytearray(descriptor.read(256))

    def zeroes():
        self.data = bytearray(256)

    def __getitem__(self, items):
        return self.data[items]

    def __str__(self):
        return hexdata(self.data)

# contains the data for one d64 image
class D64Data(object):
    # number of sectors in each track (1-42)
    sectors = (21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,
               19,19,19,19,19,19,19,
               18,18,18,18,18,18,
               17,17,17,17,17,17,17,17,17,17,17,17)

    # starting block for tracks
    sectorsn= (0,21, 42, 63, 84, 105, 126, 147, 168, 189, 210, 231,
               252, 273, 294, 315, 336, 357, 376, 395, 414, 433, 452,
               471, 490, 508, 526, 544, 562, 580, 598, 615, 632, 649,
               666, 683, 700, 717, 734, 751, 768, 785)

    # valid sizes of d64 images
    d64sizes = {174848:(35, 683, False, "35 tracks, no errors"),
                175531:(35, 683, True, "35 track, 683 error bytes"),
                196608:(40, 768, False, "40 track, no errors"),
                197376:(40, 768, True, "40 track, 768 error bytes"),
                205312:(42, 802, False, "42 track, no errors"),
                206114:(42, 802, True, "42 track, 802 error bytes")}

    def __init__(self, filepath = ""):
        self.data = []              # d64 bytes
        self.tracks = 0             # 35, 40 or 42
        self.blocks = 0             # 683, 768 or 802
        self.errors = False         # does the image contains errormap
        self.errorcount = 0         # number of errors
        self.errormap = bytearray(0)# errormap
        self.description = ""       # image description
        self.name = ""              # name extracted from image
        self.normname = ""          # normalised name
        self.filename = ""          # name of the d64 file
        self.use = True             # if the image can be used in combining
        self.used = False           # if the image is used in combining
        if filepath != "": self.load(filepath)

    # load d64 file specified by filepath (.d64 may be omitted)
    def load(self, filepath):
        if not os.path.exists(filepath):
            if filepath[-4:0] in [".d64",".D64"]:
                return False
            else:
                filepath += ".d64"
                if not os.path.exists(filepath):
                    return False
        # check file size
        d64fstat = os.stat(filepath)
        if not d64fstat.st_size in self.d64sizes:
            return False
        # setup basic d64 informations
        self.tracks = self.d64sizes[d64fstat.st_size][0]
        self.blocks = self.d64sizes[d64fstat.st_size][1]
        self.errors = self.d64sizes[d64fstat.st_size][2]
        self.description = self.d64sizes[d64fstat.st_size][3]
        try:
            d64file = open(filepath, mode="rb")
            # load d64 blocks
            for b in range(self.blocks):
                block = D64Block()
                block.load(d64file)
                self.data.append(block)
            # load error information, if exists
            if self.errors:
                self.errormap = bytearray(1)
                self.errormap.extend( bytearray(d64file.read(self.blocks)) )
                self.errorcount = self.blocks - list(self.errormap).count(1)
            else:
                self.errorcount = 0
            # filename
            self.filenamed64 = os.path.basename(filepath)
            # filename without extension
            self.filename = os.path.splitext(self.filenamed64)[0]
            # extract disk name and ID from d64
            self.name = toascii(self[18,0][144:164])
            # normalized disk name
            self.normname = self.name
            self.normname.strip()
            self.normname = self.normname.replace(" ","_")
            while self.normname.find("__") != -1: self.normname = self.normname.replace("__","_")
        except:
            self.data = []
            return False
        finally:
            d64file.close()

        return True

    # allow indexing/slicing of blocks
    def __getitem__(self, items):
        if isinstance(items, tuple):
            # track 1-42, sector 0-20
            assert (len(items) == 2) and (1 <= items[0] <= self.tracks) and (0 <= items[1] < self.sectors[items[0]]), "track/sector out of range (%d, %d)" % (items[0],items[1])
            return self.data[ self.sectorsn[items[0]-1]+items[1] ]
        elif isinstance(items, slice):
            # block 1-682/768
            return self.data[slice(items.start-1, items.stop-1,items.step)]
        else:
            # block 1-682/768
            assert 1 <= items <= self.blocks, "block out of range (%d)" % items
            return self.data[items-1]

# collection of d64 images from same physical floppy
class D64Collection(object):
    def __init__(self):
        self.clear()
        
    def clear(self):
        self.data = []
        self.different = [] # indexes of correct blocks that are different
        self.combname = ""
        self.combined = None

    # add a d64 image, check if correct blocks are the same
    def add(self, d64):
        if isinstance(d64, basestring):
            d64 = D64Data(d64)
            if len(d64.data) == 0: return None
        if len(self.data) > 0:
            if d64.tracks != self.data[0].tracks: return None
        self.data.append(d64)
        if self.combname == "": self.combname = d64.filename
        else:
            i = 0
            while (len(self.combname) > i) and (len(d64.filename) > i) and (self.combname[i] == d64.filename[i]): i += 1
            self.combname = self.combname[:i]
        if self.combname != "":
            while self.combname[-1] in "- , . :".split(): self.combname = self.combname[:-1]
        # check if correct blocks are the same
        different = []
        for d in self.data[:-1]:    # iterate through d64 images
            for i,b in enumerate(d[1:d.blocks+1]):  # iterate through blocks
                check = True
                if d.errors and d.errormap[i+1] != 1: check = False
                if d64.errors and d64.errormap[i+1] != 1: check = False
                if check and (b != d64[i+1]):
                    different.append(i)
                    d64.errormap[i+1] = 16
        self.different.append(different)
        self.combine()
        return different

    # try to combine loaded images into one correct image
    def combine(self, filepath = "", auto=True):
        if self.data == []: return False
        self.combined = D64Data()
        emptylist = not auto
        for d in self.data:
            d.used = False
            if auto: d.use = True
            elif d.use: emptylist = False
        if emptylist:
            self.combined.errormap = bytearray(1+self.data[0].blocks)
            return False
        self.combined.blocks = self.data[0].blocks
        self.combined.tracks = self.data[0].tracks
        #TODO for name/normname find first d64 with correct 18.0 block, not first from the list
        self.combined.name = self.data[0].name
        self.combined.normname = self.data[0].normname
        self.combined.errormap = bytearray(1)
        self.combined.errorcount = 0
        for i in range(1,self.data[0].blocks+1):
            # check if there is different correct blocks for index
            difcheck = True
            added = False
            for j,d in enumerate(self.data):
                if i in self.different[j] and d.use:
                    difcheck = False
                    break
            # copy one correct block, if exists
            for d in self.data:
                if ((not d.errors) or (d.errormap[i] == 1)) and d.use:
                    self.combined.data.append(d[i])
                    d.used = True
                    added = True
                    break
            # if everything is OK
            if difcheck and added:
                self.combined.errormap.append(1)
            else:
                # there are still errors...
                self.combined.errors = True
                self.combined.errorcount += 1
                #TODO choose least bad error, not first from the list
                for d in self.data:
                    if d.use: break
                # 16 indicates different correct blocks
                if not difcheck: self.combined.errormap.append(16)
                else: self.combined.errormap.append(d.errormap[i])
                # if there aren't correct blocks for index, copy first incorrect block
                if not added: self.combined.data.append(d[i])
        # save combined d64 image
        if filepath != "": self.save(filepath)
        return not self.combined.errors

    def save(self, filepath):
        if self.combined:
            ok = True
            try:
                d64file = open(filepath, mode="wb")
                for b in self.combined.data:
                    d64file.write(b.data)
                if self.combined.errors:
                    d64file.write(self.combined.errormap[1:])
            except:
                ok = False
            finally:
                d64file.close()
        return ok

about = u"""PyD64Fix %s (c) 2015  Zarko Zivanov

Program that tries to combine several d64 images
of the same physical floppy, into one image with
less or without errors.
Error detection is based on errormap part of d64.""" % (VERSION)

epilog="""You may use wildcards for d64 filename(s).
Default output filename will have "pyd64fix" suffix.
If there are still errors in d64 file, their number
will also be in the filename.

Program will check for different correct blocks in
the images. If they are detected, it is advisable to
omit those images from combining, or to do combining
manually."""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=about, formatter_class=argparse.RawDescriptionHelpFormatter,epilog=epilog)
    parser.add_argument('d64', metavar='d64', nargs='*', default="", help='(path to) d64 image (with or without d64 extension)')
    parser.add_argument('-g','--gui', action='store_true', help='invoke GUI (you need PyQt for this)')
    parser.add_argument('-a','--autoname', action='store_true', help='auto-generate disk name from its header')
    parser.add_argument('-o','--output', metavar="OUT", help='filename for output (.d64 may be omitted)')
    parser.add_argument('-u','--usage', action='store_true', help='Show examples of use')
    args = parser.parse_args()

    prgcall = "pyd64fix.py" if sys.platform[:3] == "win" else "./pyd64fix.py"
    if args.usage:
        print """Usage examples:

%(p)s disk001-*.d64
    load all d64 files whose name starts with disk001-
    and combine them into disk001-pyd64fix.d64. If, for
    example, the resulting image still has 3 errors,
    output name would be disk001-pyd64fix(3E).d64
%(p)s -o newimage a b c
    load a.d64, b.d64 and c.d64 and combine them into
    newimage.d64

%(p)s -g a b.d64 c
    load a.d64, b.d64 and c.d64 and start in GUI mode
    """ % {'p' : prgcall}
        exit(0)

    d64col = D64Collection()
    for d in args.d64:
        print "Loading %s ..." % d,
        sys.stdout.flush()
        dif = d64col.add(d)
        if dif != None: print "\rLoaded %s" % d64col.data[-1].filenamed64,
        if dif == None: print ", Not found or wrong size"
        elif dif != []: print ", Different blocks detected",
        else: print ", OK",
        if dif != None:
            if d64col.data[-1].errors: print ", %d errors" % d64col.data[-1].errorcount
            else: print ", no errors"
    #TODO za autoname treba naci prvi d64 kome je 18.0 blok ispravan, a ne prvi u listi
    if args.output != None:
        output = args.output
    elif args.autoname: output = d64col.data[0].normname
    elif d64col.combname != "": output = d64col.combname+"-pyd64fix"
    else: output = "pyd64fix"
    if not args.gui:
        if d64col.data != []:
            if d64col.combined.errors: output += "(%dE)" % d64col.combined.errorcount
            if not output[-4:0] in [".d64",".D64"]: output += ".d64"
            d64col.save(output)
            print "Saved as", output, ", with %d error(s)" % d64col.combined.errorcount if d64col.combined.errors else ", no errors"
            exit(1 if d64col.combined.errors else 0)
        else:
            parser.parse_args(["-h"])
            exit(0)

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class d64DataWidget(QWidget):
    def __init__(self):
        super(d64DataWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(100, 100)
        self.tracks = 42
        self.errormap = [0]*803 #802 + 1, indexing starts from 1
        self.errorcol = (Qt.NoBrush, Qt.green, Qt.red, Qt.red, Qt.red, Qt.red, Qt.red, Qt.red, Qt.red, Qt.red, Qt.red, Qt.red, Qt.red, Qt.red, Qt.red, Qt.red, Qt.blue)

    def setD64(self, d64):
        self.errormap = [0]*803
        if d64.errors:
            for i,e in enumerate(d64.errormap): self.errormap[i] = d64.errormap[i]
        else:
            for i in range(1,d64.blocks+1): self.errormap[i] = 1
        self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        font = QFont('Serif', 7, QFont.Light)
        qp.setFont(font)

        size = self.size()
        w = size.width()
        h = size.height()

        stepx = w / self.tracks
        stepy = h / 21

        qp.setPen(QColor(0, 0, 0))

        xx = 0
        erridx = 1
        for x in range(self.tracks):
            yy = 0
            for y in range(D64Data.sectors[x]):
                qp.setBrush(self.errorcol[self.errormap[erridx]])
                qp.drawRect(xx, yy, stepx-2, stepy-2)
                yy = yy + stepy
                erridx += 1
            xx = xx + stepx

class D64List(QGridLayout):
    def __init__(self, parent=None):
        super(D64List, self).__init__(parent)
        self.parent1 = parent
        label = QLabel("Sh")
        label.setToolTip("Show image")
        self.addWidget(label, 0, 0, alignment=Qt.AlignCenter)
        label = QLabel("Cm")
        label.setToolTip("Use image for combining")
        self.addWidget(label, 0, 1, alignment=Qt.AlignCenter)
        label = QLabel("d64 image")
        label.setToolTip("Image's filename")
        self.addWidget(label, 0, 2)
        self.rlist = []
        self.clist = []
        self.llist = []
        self.row = 1
        self.sgroup = QButtonGroup()
        self.sgroup.setExclusive(True)
        self.cgroup = QButtonGroup()
        self.cgroup.setExclusive(False)
        self.setContentsMargins(0,0,0,0)

    def clear(self):
        for d in self.rlist:
            self.sgroup.removeButton(d)
            d.close()
        for d in self.clist:
            self.cgroup.removeButton(d)
            d.close()
        for d in self.llist:
            self.removeWidget(d)
            d.close()
        self.rlist = []
        self.clist = []
        self.llist = []
        self.row = 1
        self.update()

    def add(self, name, combineit=True):
        radio = QRadioButton()
        self.sgroup.addButton(radio, self.row-1)
        self.addWidget(radio, self.row, 0, alignment=Qt.AlignCenter)
        radio.setToolTip("Show this image")
        self.rlist.append(radio)
        check = QCheckBox()
        if not combineit: check.setEnabled(False)
        self.cgroup.addButton(check, self.row-1)
        self.addWidget(check, self.row, 1, alignment=Qt.AlignCenter)
        check.setToolTip("Use this image for combining")
        self.clist.append(check)
        if name[-4:] in [".d64",".D64"]: name = name[:-4]
        if len(name) > 16: name = name[0:16]
        label = QLabel(name)
        self.addWidget(label, self.row, 2)
        self.llist.append(label)
        #if self.sgroup.checkedId() == -1: radio.setChecked(True)
        radio.setChecked(True)
        if combineit: check.setChecked(True)
        self.row += 1

class MainWindow(QMainWindow):
    """main application window"""
    def __init__(self, parent=None): 
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("PyD64Fix")

        self.centralWidget = QWidget()
        self.centralWidgetLayout = QHBoxLayout()
        self.centralWidget.setLayout(self.centralWidgetLayout)
        self.setCentralWidget(self.centralWidget)

        self.statusBar = QStatusBar(self)
        self.statusBar.setObjectName("setStatusbar")
        self.setStatusBar(self.statusBar)

        #widget for controls
        self.controls = QVBoxLayout()
        self.controls.setAlignment(Qt.AlignTop)
        self.controls.setContentsMargins(0,0,0,0)
        self.centralWidgetLayout.addLayout(self.controls)

        button = QPushButton("Select d64")
        self.controls.addWidget(button)
        button.setToolTip("Select (multiple) d64 files of the same physical floppy")
        self.connect(button, SIGNAL("clicked()"), self.selectD64)

        button = QPushButton("Save d64")
        self.controls.addWidget(button)
        button.setToolTip("Save combined d64 image")
        self.connect(button, SIGNAL("clicked()"), self.saveD64)

        button = QPushButton("About")
        self.controls.addWidget(button)
        self.connect(button, SIGNAL("clicked()"), self.about)

        # d64 list
        self.d64list = D64List()
        self.controls.addLayout(self.d64list)
        for d64 in d64col.data:
            self.d64list.add(d64.filename)
        self.d64list.add("combined.d64", False)
        self.connect(self.d64list.sgroup, SIGNAL("buttonClicked(int)"), self, SLOT("radioClickedSlot(int)"))
        self.connect(self.d64list.cgroup, SIGNAL("buttonClicked(int)"), self, SLOT("checkClickedSlot(int)"))

        #widget for d64 representation
        self.d64Layout = QVBoxLayout()
        self.d64Layout.setContentsMargins(0,0,0,0)
        self.centralWidgetLayout.addLayout(self.d64Layout)
        self.d64widget = d64DataWidget()
        self.d64Layout.addWidget(self.d64widget)
        self.d64widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.d64label = QLabel(u"<b><font color='green'>■<font color='white'> - OK"
                               u", <font color='red'>■<font color='white'> - Error"
                               u", <font color='blue'>■<font color='white'> - Different data"
                               u", <font color='black'>□<font color='white'> - Unused")
        self.d64label.setStyleSheet("background-color: darkgray")
        self.d64Layout.addWidget(self.d64label)
        self.resize(QSize(500,200))

        self.d64list.rlist[-1].click()
        self.selectPath = os.getcwd()
        self.savePath = self.selectPath

    def selectD64(self):
        dialog = QFileDialog(None,"Select d64 file(s) for combining",self.selectPath,"d64 images (*.d64 *.D64)")
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        if dialog.exec_() == QDialog.Accepted:
            #if user selected something
            d64col.clear()
            for d in dialog.selectedFiles():
                d64col.add(unicode(d))
            self.selectPath = dialog.directory().path()
            self.d64list.clear()
            for d64 in d64col.data:
                self.d64list.add(d64.filename)
            self.d64list.add("combined.d64", False)
            self.d64list.rlist[-1].click()

    def saveD64(self):
        dialog = QFileDialog(None,"Save combined d64 file",self.savePath,"d64 images (*.d64 *.D64)")
        dialog.setFileMode(QFileDialog.AnyFile)
        errors = "(%dE)" % d64col.combined.errorcount if d64col.combined.errors else ""
        if d64col.combname == "": dialog.selectFile("pyd64fix%s.d64" % errors)
        else: dialog.selectFile(d64col.combname + "-pyd64fix%s.d64" % errors)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        if dialog.exec_() == QDialog.Accepted:
            #if user selected something
            d64col.save(dialog.selectedFiles()[0])
            self.savePath = dialog.directory().path()

    @pyqtSlot(int)
    def radioClickedSlot(self,index):
        if index < len(d64col.data):
            self.d64widget.setD64(d64col.data[index])
            self.showD64Status(d64col.data[index])
        elif d64col.combined:
            self.d64widget.setD64(d64col.combined)
            self.showD64Status(d64col.combined)

    @pyqtSlot(int)
    def checkClickedSlot(self,index):
        d64col.data[index].use = self.d64list.cgroup.button(index).isChecked()
        d64col.combine(auto=False)
        self.radioClickedSlot(self.d64list.sgroup.checkedButton())

    def showD64Status(self, d64):
        self.statusBar.showMessage("Name+ID: '%s', Blocks: %d, Errors: %d" % (d64.name, d64.blocks, d64.errorcount) )

    def about(self):
        """displays about dialog"""
        text = about.replace("\n","<br>")
        text += "<br><br>E-Mail: zzarko@gmail.com"
        text += "<br><br>University of Novi Sad, Faculty Of Technical Sciences"
        text += "<br>Chair for Applied Computer Science"
        text += ', <a href="http://www.acs.uns.ac.rs/">http://www.acs.uns.ac.rs</a>'
        text += "<br><br>Linux User Group of Novi Sad"
        text += ', <a href="http://www.lugons.org/">http://www.lugons.org/</a>'

        gpl = "<br><br>This program is free software: you can redistribute it and/or modify "
        gpl += "it under the terms of the GNU General Public License as published by "
        gpl += "the Free Software Foundation, either version 3 of the License, or "
        gpl += "(at your option) any later version."
        gpl += "<br><br>This program is distributed in the hope that it will be useful, "
        gpl += "but WITHOUT ANY WARRANTY; without even the implied warranty of "
        gpl += "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the "
        gpl += "GNU General Public License for more details. "
        gpl += "<br><br>You should have received a copy of the GNU General Public License "
        gpl += "along with this program. If not, see "
        gpl += "<a href=http://www.gnu.org/licenses>http://www.gnu.org/licenses</a>."

        dialog = QMessageBox(QMessageBox.Information,"About",text+gpl)
        dialog.setTextFormat(Qt.RichText)
        dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    app.exec_()

"""
History of changes

1.0 - Initial version
"""

