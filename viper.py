#!/usr/bin/env python3
"""
Viper IDE - Assembly & C64 Code Editor
Eski CrossViper'dan türetilmiş, 6502 Assembly ve C64 odaklı IDE

Bu IDE şunları destekler:
- 6502 Assembly syntax highlighting
- C64 BASIC syntax highlighting 
- Multiple format disassembly
- Opcodes ve instruction tanıma
- C64 memory map entegrasyonu
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import font
import threading
import platform
import os
import sys
import time
import re
import shutil
import subprocess
import configparser
import zipfile

# Viper modülleri
try:
    from viper_codeeditor import TextLineNumbers, TextPad
    from viper_configuration import Configuration
    from viper_dialog import (SettingsDialog, ViewDialog, 
                        InfoDialog, NewDirectoryDialog, HelpDialog,
                        GotoDialog, MessageYesNoDialog, MessageDialog,
                        MessageSudoYesNoDialog, ChangeDirectoryDialog,
                        OpenFileDialog, SaveFileDialog, RenameDialog,
                        ZipFolderDialog)
    VIPER_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Viper modülleri bulunamadı: {e}")
    VIPER_MODULES_AVAILABLE = False

# 6502 Assembly Syntax Highlighting
try:
    from pygments import lex, highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import get_formatter_by_name
    from pygments.token import Token
    import pygments.lexers
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False

# D64 system entegrasyonu
try:
    from improved_disassembler import ImprovedDisassembler
    from assembly_formatters import AssemblyFormatters
    from bridge_systems import DisassemblyFormatBridge
    D64_SYSTEM_AVAILABLE = True
except ImportError:
    D64_SYSTEM_AVAILABLE = False

# Syntax highlighter entegrasyonu
try:
    from syntax_highlighter import Assembly6502Highlighter, C64BasicHighlighter, HybridHighlighter
    SYNTAX_HIGHLIGHTER_AVAILABLE = True
except ImportError:
    SYNTAX_HIGHLIGHTER_AVAILABLE = False

###################################################################
class RunThread(threading.Thread):
    def __init__(self, command):
        super().__init__()
        self.command = command
    
    def run(self):
        try:
            os.system(self.command)
        except Exception as e:
            print(str(e))

###################################################################
class ToolTip():
    def __init__(self, widget):
        self.widget = widget
        self.tipWindow = None
        self.id = None
        self.x = self.y = 0
    
    def showtip(self, text):
        self.text = text
        if self.tipWindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox('insert')
        x = x + self.widget.winfo_rootx() + 0
        y = y + cy + self.widget.winfo_rooty() + 40
        self.tipWindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry('+%d+%d' % (x, y))
        
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background='#000000', foreground='yellow', relief=tk.SOLID, borderwidth=1)
        label.pack(ipadx=1)
     
    def hidetip(self):
        tw = self.tipWindow
        self.tipWindow = None
        if tw:
            tw.destroy()
    
        
###################################################################


class LeftPanel(ttk.Frame):
    '''
        LeftPanel ... containing treeView, leftButtonFrame, Buttons 
    '''
    def __init__(self, master=None, rightPanel=None):
        super().__init__(master)
        self.master = master
        self.rightPanel = rightPanel
        self.pack()
        
        
        self.initUI()
        
        self.clipboard = ''
    
    def initUI(self):
        path = os.path.abspath(__file__)
        pathList = path.replace('\\', '/')
        pathList = path.split('/')[:-1]
        print(pathList)
        self.dir = ''
        for item in pathList:
       	    self.dir += item + '/'
        
        print('directory: ' + self.dir)
        leftButtonFrame = ttk.Frame(self, height=25)
        leftButtonFrame.pack(side=tk.TOP, fill=tk.X)

        # TreeView
        from os.path import expanduser
        path = expanduser("~")
        os.chdir(path)
        #path = '.'

        self.tree = ttk.Treeview(self)

        self.tree.tag_configure('pythonFile', background='black', foreground='green')
        self.tree.tag_configure('row', background='black', foreground='white')
        self.tree.tag_configure('folder', background='black', foreground='yellow')
        self.tree.tag_configure('subfolder', background='black', foreground='#448dc4')
        self.tree.tag_configure('hidden', background='black', foreground='gray')
        
        
        #self.tree.heading('#0', text='<-', anchor='w')
        #self.tree.heading('#0', text='Name')
        self.tree['show'] = 'tree'
        self.tree.bind("<Double-1>", self.OnDoubleClickTreeview)
        self.tree.bind("<Button-1>", self.OnClickTreeview)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.tree.bind("<ButtonRelease-3>", self.treePopUp)
        self.tree.bind('<Alt-Right>', self.changeToTextPad)
        
        
        abspath = os.path.abspath(path)
        root_node = self.tree.insert('', 'end', text=abspath, open=True, tags='folder')
        self.process_directory(root_node, abspath)

        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Buttons
        infoIcon = tk.PhotoImage(file=self.dir + 'images/info-file.png')
        infoButton = ttk.Button(leftButtonFrame, image=infoIcon, command=self.infoFile)
        infoButton.image = infoIcon
        infoButton.pack(side=tk.LEFT)
        self.createToolTip(infoButton, 'Show Information')

        newFolderIcon = tk.PhotoImage(file=self.dir + 'images/new-folder.png')
        newFolderButton = ttk.Button(leftButtonFrame, image=newFolderIcon, command=self.newFolder)
        newFolderButton.image = newFolderIcon
        newFolderButton.pack(side=tk.LEFT)
        self.createToolTip(newFolderButton, 'Create New Folder')

        copyFileIcon = tk.PhotoImage(file=self.dir + 'images/copy-file.png')
        copyFileButton = ttk.Button(leftButtonFrame, image=copyFileIcon, command=self.copyFile)
        copyFileButton.image = copyFileIcon
        copyFileButton.pack(side=tk.LEFT)
        self.createToolTip(copyFileButton, 'Copy Item')

        pasteFileIcon = tk.PhotoImage(file=self.dir + 'images/paste-file.png')
        pasteFileButton = ttk.Button(leftButtonFrame, image=pasteFileIcon, command=self.pasteFile)
        pasteFileButton.image = pasteFileIcon
        pasteFileButton.pack(side=tk.LEFT)
        self.createToolTip(pasteFileButton, 'Paste Item')

        deleteFileIcon = tk.PhotoImage(file=self.dir + 'images/delete-file.png')
        deleteFileButton = ttk.Button(leftButtonFrame, image=deleteFileIcon, command=self.deleteFile)
        deleteFileButton.image = deleteFileIcon
        deleteFileButton.pack(side=tk.LEFT)
        self.createToolTip(deleteFileButton, 'Delete Item')

        self.selected = []
        self.sourceItem = None
        self.destinationItem = None
        
    def changeToTextPad(self, event=None):
        if self.rightPanel.textPad:
            self.rightPanel.textPad.focus_set()

    def createToolTip(self, widget, text):
        toolTip = ToolTip(widget)
        def enter(event):
            toolTip.showtip(text)
        def leave(event):
            toolTip.hidetip()
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)
        
    
    def process_directory(self, parent, path):
        try:
            l = []
            for p in os.listdir(path):
                abspath = os.path.join(path, p)
                isdir = os.path.isdir(abspath)

                if isdir:
                    item = '> /' + str(p)
                    l.append(item)
                    continue
                    
                else:
                    item = str(p)
                    l.append(item)
                
                # list sort ...
            l.sort()
            #l.reverse()
            
            for items in l:
                if items.startswith('>'):
                    self.tree.insert(parent, 'end', text=str(items), open=False, tags='subfolder')
                elif items.startswith('.'):
                    self.tree.insert(parent, 'end', text=str(items), open=False, tags='hidden')                    
                elif items.endswith('.py') or items.endswith('.pyw'):
                    self.tree.insert(parent, 'end', text=str(items), open=False, tags='pythonFile')
                else:
                    self.tree.insert(parent, 'end', text=str(items), open=False, tags='row')
       
        except Exception as e:
            MessageDialog(self, 'Error', '\n' + str(e) + '\n')
            return
        
    def OnClickTreeview(self, event):
        item = self.tree.identify('item',event.x,event.y)
        if '/' in self.tree.item(item,"text") or '\\' in self.tree.item(item, "text"):
            self.master.master.master.title(self.checkPath(self.tree.item(item, 'text')))
                
        else:
            dir = self.checkPath(os.getcwd())
            self.master.master.master.title(dir + '/' + self.checkPath(self.tree.item(item, 'text')))
        #print(item)
    
    def ignore(self, event):
        # workaround for dismiss OnDoubleClickTreeview to open file twice 
        # step 1
        return 'break'

    def OnDoubleClickTreeview(self, event):
        item = self.tree.identify('item',event.x,event.y)
        #print("you clicked on", self.tree.item(item,"text"))
        if self.tree.item(item, "text") == '': 

            d = os.getcwd()
            d = self.checkPath(d)
            directory = filedialog.askdirectory(initialdir=d)
            if not directory:
                return
            try:
                os.chdir(directory)
                for i in self.tree.get_children():
                    self.tree.delete(i)
                path = '.'
                abspath = os.path.abspath(path)
                root_node = self.tree.insert('', 'end', text=abspath, open=True, tags='folder')
                self.process_directory(root_node, abspath)
                
            except Exception as e:
                MessageDialog(self, 'Error', '\n' + str(e) + '\n')

                return
        
        elif self.tree.item(item, "text").startswith('>'):
            root = os.getcwd()
            sub = self.tree.item(item, "text").split()[1]
            dir = root + sub
            dir = self.checkPath(dir)
            try:
                os.chdir(dir)
            except Exception as e:
                MessageDialog(self, 'Error', '\n' + str(e) + '\n')

            self.selected = None
            self.refreshTree()
            self.master.master.master.title(dir)
    
        elif '/' in self.tree.item(item, "text") or '\\' in self.tree.item(item, "text"):
            os.chdir('..')
            dir = self.checkPath(os.getcwd())
            self.master.master.master.title(dir)
            self.refreshTree()
            return 'break'

        else:
            file = self.tree.item(item,"text")
            dir = os.getcwd()
            dir = self.checkPath(dir)
            filename = dir + '/' + file
            self.tree.config(cursor="X_cursor")
            self.tree.bind('<Double-1>', self.ignore)
            
            try:
                self.master.master.rightPanel.open(file=filename)
            except Exception as e:
                MessageDialog(self, 'Error', '\n' + str(e) + '\n')

            self.tree.config(cursor='')
            self.tree.update()
            self.rightPanel.textPad.mark_set("insert", "1.0")
            self.master.master.master.title(filename)
            self.rightPanel.textPad.focus_set()
            
            # workaround 
            # step 2
            self.refreshTree()
            self.tree.update()
            self.tree.after(500, self.bindit)
        
        self.refreshTree()
    
    def bindit(self):
        # workaround 
        # step 3
        self.tree.bind('<Double-1>', self.OnDoubleClickTreeview)

    def checkPath(self, path):
        if '\\' in path:
            path = path.replace('\\', '/')
        return path

    def on_select(self, event):
        self.selected = event.widget.selection()
    
    def infoFile(self):
        rootDir = self.checkPath(os.getcwd())
        #print(rootDir)
        directory = None
        file = None
        size = None
        if self.selected:
            for idx in self.selected:
                try:
                    text = self.tree.item(idx)['text']
                except:
                    self.selected = []
                    return
            if '/' in text or '\\' in text:
                directory = True
            else:
                file = True
            if file == True:
                filename = rootDir + '/' + text
                size = os.path.getsize(filename)
                size = format(size, ',d')
            else:
                filename = text
            text = self.checkPath(text)
            InfoDialog(self, title='Info', text=text, directory=directory, file=file, size=size)
        
        else:
            return
        

    def refreshTree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        path = '.'
        abspath = os.path.abspath(path)
        root_node = self.tree.insert('', 'end', text=abspath, open=True, tags='folder')
        self.process_directory(root_node, abspath)

    def newFolder(self):
        NewDirectoryDialog(self, title='Create directory')
        self.refreshTree()
        
    def copyFile(self):
        if not self.selected:
            self.clipboard = ''
            return
        else:
            for idx in self.selected:
                text = self.tree.item(idx)['text']
        
        self.clipboard = text
        self.homedir = self.checkPath(os.getcwd())
        
        if self.clipboard.startswith('>'):
            dir = self.clipboard.split()[1]
            self.sourceItem = self.homedir + dir
        elif '/' in self.clipboard or '\\' in self.clipboard:
            self.sourceItem = self.homedir
        else:
            self.sourceItem = self.homedir + '/' + self.clipboard
            self.sourceItem = self.checkPath(self.sourceItem)
        
        self.selected = None
        self.rightPanel.setMessage('<' + self.clipboard + '>' + ' marked', 800) 

    def pasteFile(self):
        if not self.sourceItem:
            return
        
        if not self.selected:
            #self.destinationItem = self.checkPath(os.getcwd())
            self.rightPanel.setMessage('<No target selected>', 800)
            return
        
        if self.selected:
            try:
                for idx in self.selected:
                    text = self.tree.item(idx)['text']
        
            except Exception as e:
                #print('this')
                MessageDialog(self, 'Error', '\n' + str(e) + '\n')
                return
        
            currentDirectory = self.checkPath(os.getcwd())
        
            if text.startswith('>'):
                dir = text.split()[1]
                self.destinationItem = currentDirectory + dir
        
            elif '/' in text or '\\' in text:
                self.destinationItem = currentDirectory

            else:
                self.destinationItem = currentDirectory + '/' + text
        
        #print('self.sourceItem:', self.sourceItem)
        #print('self.destinationItem:', self.destinationItem)
        
        if os.path.isfile(self.sourceItem):             # Source == file
            if os.path.isdir(self.destinationItem):     # Destination == directory
                destination = self.destinationItem      

                try:
                    shutil.copy2(self.sourceItem, destination)
                    self.refreshTree()

                except Exception as e:
                    MessageDialog(self, 'Error', '\n' + str(e) + '\n')
                    return
            
            elif os.path.isfile(self.destinationItem):  # Destination == file
                destination = os.path.dirname(self.destinationItem)

                try:
                    shutil.copy2(self.sourceItem, destination)
                    self.refreshTree()

                except Exception as e:
                    MessageDialog(self, 'Error', '\n' + str(e) + '\n')
                    return

        elif os.path.isdir(self.sourceItem):            # Source == directory
            if os.path.isdir(self.destinationItem):     # Destination == directory
                destination = self.destinationItem + '/'
                basename = self.sourceItem.split('/')[-1]
                destination = destination + basename
                destination = self.checkPath(destination)
                #print('destination:', destination)

                try:
                    shutil.copytree(self.sourceItem, destination)
                    self.refreshTree()
                
                except Exception as e:
                    MessageDialog(self, 'Error', '\n' + str(e) + '\n')
                    return
            
            elif os.path.isfile(self.destinationItem):   # Destination == file
                destination = os.path.dirname(self.destinationItem) + '/'
                destination = self.checkPath(destination)
                basename = self.sourceItem.split('/')[-1]
                destination = destination + basename
                #print('destination:', destination)
                
                try:
                    shutil.copytree(self.sourceItem, destination)
                    self.refreshTree()
                    
                except Exception as e:
                    MessageDialog(self, 'Error', '\n' + str(e) + '\n')
                    return
        
        self.selected = None
        self.sourceItem = None
            
        
    def deleteFile(self):
        rootDir = self.checkPath(os.getcwd())
        directory = None
        file = None
        size = None
        
        if self.selected:
            for idx in self.selected:
                try:
                    text = self.tree.item(idx)['text']
                except:
                    self.selected = []
                    return
            
            if '/' in text or '\\' in text:
                directory = True
            else:
                file = True
            
            if file == True:
                filename = rootDir + '/' + text
            else: # directory
                if text.startswith('>'):
                    dir = text.split()[-1]
                    filename = rootDir + dir
                elif '/' in text or '\\' in text:
                    filename = text
                
        else:
            return
        
        filename = self.checkPath(filename)
        
        dialog = MessageYesNoDialog(self, 'Delete', '\n\tDelete\n\n' + filename + '  ?\n\n')
        result = dialog.result
        
        if result == 1:
            if directory:
                try:
                    shutil.rmtree(filename)
                    self.refreshTree()
                    
                except Exception as e:
                    MessageDialog(self, 'Error', '\n' + str(e) + '\n')

                    
            elif file:
                try:
                    os.remove(filename)
                    self.refreshTree()
                
                except Exception as e:
                    MessageDialog(self, 'Error', '\n' + str(e) + '\n')

        
    
    def treePopUp(self, event):
        item = self.tree.identify('item',event.x,event.y)
        self.tree.selection_set(item)
            
        menu = tk.Menu(self, tearoff=False, background='#000000',foreground='white',
                activebackground='green', activeforeground='white')
        menu.add_command(label='Info', compound=tk.LEFT, command=self.treeGenerateInfo)
        menu.add_separator()
        menu.add_command(label="Create New Folder", compound=tk.LEFT, command=self.treeGenerateFolder)
        menu.add_command(label="Change Folder", compound=tk.LEFT, command=self.treeGenerateChangeDir)
        menu.add_separator()
        menu.add_command(label="Copy Item", compound=tk.LEFT, command=self.treeGenerateCopy)
        menu.add_command(label="Paste Item", compound=tk.LEFT, command=self.treeGeneratePaste)
        menu.add_command(label="Rename Item", compound=tk.LEFT, command=self.treeGenerateRename)

        menu.add_separator()
        menu.add_command(label="Delete Item", compound=tk.LEFT, command=self.treeGenerateDelete)
        menu.add_separator()
        menu.add_command(label="Zip Folder", compound=tk.LEFT, command=self.treeZipFolder)
        menu.add_separator()
        menu.add_command(label="Open Terminal", compound=tk.LEFT, command = self.treeGenerateTerminal)
        menu.add_separator()
        menu.add_command(label="Refresh Tree", compound=tk.LEFT, command = self.treeGenerateRefresh)
        menu.tk_popup(event.x_root, event.y_root, 0)

    def treeGenerateInfo(self):
        if not self.selected:
            self.rightPanel.setMessage('<No Selection>', 800)
            return
        
        self.infoFile()
    
    def treeGenerateFolder(self):
        self.newFolder()
    
    def treeGenerateCopy(self):
        if not self.selected:
            self.rightPanel.setMessage('<No Selection>', 800)

        self.copyFile()

    def treeGeneratePaste(self):
        if not self.selected:
            self.rightPanel.setMessage('<No Selection>', 800)

        self.pasteFile()
    
    def treeGenerateDelete(self):
        if not self.selected:
            self.rightPanel.setMessage('<No Selection>', 800)

        self.deleteFile()
    
    def treeGenerateRename(self):
        if not self.selected:
            self.rightPanel.setMessage('<No Selection>', 800)
        
        obj = self.tree.selection()
        item = self.tree.item(obj)['text']
        
        RenameDialog(self, title='Rename Item', item=item)
        self.refreshTree()
        
    def treeGenerateChangeDir(self):
        d = os.getcwd()
        d = self.checkPath(d)
        
        dialog = ChangeDirectoryDialog(self, 'Change Folder', 'Select Folder')
        result = dialog.result
        selected = dialog.selected
        
        if result == 0:
            os.chdir(d)
            self.refreshTree()
        else:

            if selected is not None:
                if d == selected:
                    self.refreshTree()
                    return
                dir = os.getcwd() + selected
                try:
                    os.chdir(dir)
                except Exception as e:
                    self.refreshTree()
  
            else:
                os.chdir(d)
                self.refreshTree()

        
        self.master.master.master.title(os.getcwd())
        self.refreshTree()
    
    def treeGenerateRefresh(self):
        self.refreshTree()
    

    
    def treeZipFolder(self):
        #dialog = simpledialog.askstring('Make Zip-File from current directory', 'current directory\n' + os.getcwd() + 
        #                                '\n\nEnter filename: ')
        
        ZipFolderDialog(self, 'Zip-Folder')
        
            
        #filename = dialog
        
        #dir = os.getcwd()
        #self.zipfolder(filename, dir)
        self.refreshTree()
    
    def treeGenerateTerminal(self):
        c = Configuration()     # -> in configuration.py
        system = c.getSystem()
        terminalCommand = c.getTerminal(system)

        thread = RunThread(terminalCommand)
        thread.start()

        
        
######################################################################


######################################################################
class RightPanel(tk.Frame):
    '''
        RightPanel .... containing textPad + rightButtonFrame + Buttons
    '''
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.initUI()

    
    def initUI(self):
        pathList = __file__.replace('\\', '/')
        pathList = __file__.split('/')[:-1]
        c = Configuration()
        self.password = c.getPassword()
        
        self.dir = ''
        for item in pathList:
            self.dir += item + '/'
        #print(self.dir)
        

        rightButtonFrame = ttk.Frame(self, height=25)
        rightButtonFrame.pack(side=tk.TOP, fill=tk.X)
        
        self.rightBottomFrame = ttk.Frame(self, height=25)
        self.rightBottomFrame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # notebook
        self.notebook = ttk.Notebook(self)
        self.frame1 = ttk.Frame(self.notebook)
        self.notebook.add(self.frame1, text='noname')
        
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.notebook.bind("<ButtonRelease-1>", self.tabChanged)
        self.notebook.bind("<ButtonRelease-3>", self.closeContext)
        
        # clipboard

        # textPad
        self.textPad = TextPad(self.frame1, undo=True, maxundo=-1, autoseparators=True)
        self.textPad.filename = None
        self.textPad.bind("<FocusIn>", self.onTextPadFocus)
        self.textPad.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        #textScrollY = ttk.Scrollbar(self.textPad)
        textScrollY = tk.Scrollbar(self.textPad, bg="#424242", troughcolor="#2d2d2d", highlightcolor="green", activebackground="green", highlightbackground="gray")
        textScrollY.config(cursor="left_ptr")
        self.textPad.configure(yscrollcommand=textScrollY.set)
        textScrollY.config(command=self.textPad.yview)
        textScrollY.pack(side=tk.RIGHT, fill=tk.Y)
                
        self.linenumber = TextLineNumbers(self.frame1, width=35, bg='black')
        self.linenumber.attach(self.textPad)
        self.linenumber.pack(side="left", fill="y")
        
        self.linenumber.bind('<ButtonRelease-1>', self.linenumberSelect)
        self.linenumber.bind('<ButtonRelease-3>', self.linenumberPopUp)
        
        # hold textPad and linenumber-widget
        self.TEXTPADS = {}
        self.LINENUMBERS = {}
        
        self.TEXTPADS[0] = self.textPad
        self.LINENUMBERS[0] = self.linenumber
        
        # Buttons
        newIcon = tk.PhotoImage(file=self.dir + 'images/new.png')
        newButton = ttk.Button(rightButtonFrame, image=newIcon, command=self.new)
        newButton.image = newIcon
        newButton.pack(side=tk.LEFT)
        self.createToolTip(newButton, 'Create New File')

        openIcon = tk.PhotoImage(file=self.dir + 'images/open.png')
        openButton = ttk.Button(rightButtonFrame, image=openIcon, command=self.open)
        openButton.image = openIcon
        openButton.pack(side=tk.LEFT)
        self.createToolTip(openButton, 'Open File')

        
        saveIcon = tk.PhotoImage(file=self.dir + 'images/save.png')
        saveButton = ttk.Button(rightButtonFrame, image=saveIcon, command=self.save)
        saveButton.image = saveIcon
        saveButton.pack(side=tk.LEFT)
        self.createToolTip(saveButton, 'Save File')

        printIcon = tk.PhotoImage(file=self.dir + 'images/print.png')
        printButton = ttk.Button(rightButtonFrame, image=printIcon, command=self.print)
        printButton.image = printIcon
        printButton.pack(side=tk.LEFT)
        self.createToolTip(printButton, 'Print File')

        
        undoIcon = tk.PhotoImage(file=self.dir + 'images/undo.png')
        self.undoButton = ttk.Button(rightButtonFrame, image=undoIcon, command=self.undo)
        self.undoButton.image = undoIcon
        self.undoButton.pack(side=tk.LEFT)
        self.createToolTip(self.undoButton, 'Undo')

        redoIcon = tk.PhotoImage(file=self.dir + 'images/redo.png')
        self.redoButton = ttk.Button(rightButtonFrame, image=redoIcon, command=self.redo)
        self.redoButton.image = redoIcon
        self.redoButton.pack(side=tk.LEFT)
        self.createToolTip(self.redoButton, 'Redo')

        zoomInIcon = tk.PhotoImage(file=self.dir + 'images/zoomIn.png')
        zoomInButton = ttk.Button(rightButtonFrame, image=zoomInIcon, command=self.zoomIn)
        zoomInButton.image = zoomInIcon
        zoomInButton.pack(side=tk.LEFT)
        self.createToolTip(zoomInButton, 'Zoom In')

        zoomOutIcon = tk.PhotoImage(file=self.dir + 'images/zoomOut.png')
        zoomOutButton = ttk.Button(rightButtonFrame, image=zoomOutIcon, command=self.zoomOut)
        zoomOutButton.image = zoomOutIcon
        zoomOutButton.pack(side=tk.LEFT)
        self.createToolTip(zoomOutButton, 'Zoom Out')

        settingsIcon = tk.PhotoImage(file=self.dir + 'images/settings.png')
        settingsButton = ttk.Button(rightButtonFrame, image=settingsIcon, command=self.settings)
        settingsButton.image = settingsIcon
        settingsButton.pack(side=tk.LEFT)
        self.createToolTip(settingsButton, 'Show Settings')

        runIcon = tk.PhotoImage(file=self.dir + 'images/run.png')
        runButton = ttk.Button(rightButtonFrame, image=runIcon, command=self.run)
        runButton.image = runIcon
        runButton.pack(side=tk.RIGHT)
        runButton.bind('<Button-3>', self.popupRun)
        self.createToolTip(runButton, 'Run File')
        
        terminalIcon = tk.PhotoImage(file=self.dir + 'images/terminal.png')
        terminalButton = ttk.Button(rightButtonFrame, image=terminalIcon, command=self.terminal)
        terminalButton.image = terminalIcon
        terminalButton.pack(side=tk.RIGHT)
        self.createToolTip(terminalButton, 'Open Terminal')

        interpreterIcon = tk.PhotoImage(file=self.dir + 'images/interpreter.png')
        interpreterButton = ttk.Button(rightButtonFrame, image=interpreterIcon, command=self.interpreter)
        interpreterButton.image = interpreterIcon
        interpreterButton.pack(side=tk.RIGHT)
        self.createToolTip(interpreterButton, 'Open Python Interpreter')

        viewIcon = tk.PhotoImage(file=self.dir + 'images/view.png')
        viewButton = ttk.Button(self.rightBottomFrame, image=viewIcon, command=self.overview)
        viewButton.image = viewIcon
        viewButton.pack(side=tk.RIGHT)
        self.createToolTip(viewButton, 'Class Overview')

        searchIcon = tk.PhotoImage(file=self.dir + 'images/search.png')
        searchButton = ttk.Button(self.rightBottomFrame, image=searchIcon, command=self.search)
        searchButton.image = searchIcon
        searchButton.pack(side=tk.RIGHT)
        self.createToolTip(searchButton, 'Search')

        self.searchBox = tk.Entry(self.rightBottomFrame, bg='black', fg='white')
        self.searchBox.configure(cursor="xterm green")
        self.searchBox.configure(insertbackground = "red")
        self.searchBox.configure(highlightcolor='#448dc4')

        self.searchBox.bind('<Key>', self.OnSearchBoxChange)
        self.searchBox.bind('<Return>', self.search)
        self.searchBox.pack(side=tk.RIGHT, padx=5)
        # self.searching = False

        # autocompleteEntry
        self.autocompleteEntry = ttk.Label(self.rightBottomFrame, text='---', font=('Mono', 13))
        self.autocompleteEntry.pack(side='left', fill='y', padx=5)
        self.textPad.entry = self.autocompleteEntry


        # Shortcuts
        self.textPad = self.shortcutBinding(self.textPad)
        

    def popupRun(self, event):
        self.runMenu = tk.Menu(self, tearoff=0, background='#000000',foreground='white',
                activebackground='green', activeforeground='white')
        self.runMenu.add_command(label="Run", command=self.run)
        self.runMenu.add_command(label="Run with sudo", command=self.runSudo)

        self.runMenu.post(event.x_root, event.y_root)


    def onTextPadModified(self, event=None):
        flag = self.textPad.edit_modified()
        if flag:
            x = self.notebook.index(self.notebook.select())
            filename = self.textPad.filename
            if filename == None:
                self.textPad.edit_modified(False)
                return
            else:
                if filename.endswith('*'):
                    self.textPad.edit_modified(False)
                    return
                else:
                    filename += '*'
                    file = filename.split('/')[-1]
                    self.notebook.tab(x, text=file)
                    self.textPad.filename = filename
                    self.update()
                    self.textPad.edit_modified(False)
    
            
    def shortcutBinding(self, textPad):
        textPad.bind('<F1>', self.help)
        textPad.bind('<Control-Key-n>', self.new)
        textPad.bind('<Control-Key-o>', self.open)
        textPad.bind('<Control-Key-s>', self.save)
        textPad.bind("<Control-Shift_L><S>", self.saveAs)
        textPad.bind("<Control-Shift_R><S>", self.saveAs)
        textPad.bind('<Control-Key-p>', self.print)
        textPad.bind('<Control-Key-z>', self.undo)
        textPad.bind('<Control-Shift_L><Z>', self.redo)
        textPad.bind('<Control-Key-f>', self.showSearch)
        textPad.bind('<Control-Key-g>', self.overview)
        textPad.bind('<F12>', self.settings)
        textPad.bind('<Alt-Up>', self.zoomIn)
        textPad.bind('<Alt-Down>', self.zoomOut)
        textPad.bind('<Alt-Right>', self.nextTab)
        textPad.bind('<Alt-Left>', self.changeToTreeview)
        textPad.bind('<Alt-F4>', self.quit)
        textPad.bind('<<Modified>>', self.onTextPadModified)

        # PopUp TextPad
        textPad.bind("<ButtonRelease-3>", self.textPadPopUp)
        textPad.bind("<ButtonRelease-1>", self.onTextPadFocus)
        
        # other binding for the textPad
        textPad.bind("<<Change>>", self.on_change)
        textPad.bind("<Configure>", self.on_change)


        return textPad

    def get_all_children(self, tree, item=""):
        children = tree.get_children(item)
        for child in children:
            children += self.get_all_children(tree, child)
        return children    

    def changeToTreeview(self, event):
        children = self.get_all_children(self.leftPanel.tree)
        item = children[0]
        self.leftPanel.tree.selection_set(item)
        self.leftPanel.tree.focus_set()

    
    def showSearch(self, event=None):
        self.searchBox.focus_set()
    
    def quit(self, event):
        self.master.master.destroy()
    
    def nextTab(self, event=None):
        tabs = self.notebook.tabs()
        if not tabs:
            return
        
        id = self.notebook.index(self.notebook.select())
        
        if id < len(tabs) - 1:
            id += 1
            self.notebook.select(id)
            self.tabChanged()
            self.textPad.focus_set()

        elif id == len(tabs) -1:
            id = 0
            self.notebook.select(id)
            self.tabChanged()
            self.textPad.focus_set()
        
        else:
            return
    
    def help(self, event=None):
        help = HelpDialog(self, "Help")
        self.textPad.focus_set()


    def createToolTip(self, widget, text):
        toolTip = ToolTip(widget)
        def enter(event):
            toolTip.showtip(text)
        def leave(event):
            toolTip.hidetip()
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)

    def OnSearchBoxChange(self, event=None):
        # self.searching = False
        self.start = 1.0
        if self.textPad:
            self.textPad.tag_remove('sel', "1.0", tk.END)

    def onTextPadFocus(self, event):
        filename = self.textPad.filename

        if not filename:
            return
        
        self.tabChanged()
    
    def linenumberPopUp(self, event):
        menu = tk.Menu(self.notebook, tearoff=False, background='#000000',foreground='white',
                activebackground='green', activeforeground='white')
        menu.add_command(label='Goto', compound=tk.LEFT, command=self.textPadGenerateGoto)
        menu.tk_popup(event.x_root, event.y_root, 0)

    
    def textPadPopUp(self, event):
        menu = tk.Menu(self.notebook, tearoff=False, background='#000000',foreground='white',
                activebackground='green', activeforeground='white')
        menu.add_command(label='Cut', compound=tk.LEFT, command=self.textPadGenerateCut)
        menu.add_command(label="Copy", compound=tk.LEFT, command=self.textPadGenerateCopy)
        menu.add_command(label="Paste", compound=tk.LEFT, command=self.textPadGeneratePaste)
        menu.add_separator()
        menu.add_command(label="Select All", compound=tk.LEFT, command=self.textPadSelectAll)
        menu.add_command(label="Highlight All", compound=tk.LEFT, command=self.textPadHighlightAll)
        menu.add_separator()
        menu.add_command(label='Goto', compound=tk.LEFT, command=self.textPadGenerateGoto)
        menu.add_separator()
        menu.add_command(label="Open Terminal", compound=tk.LEFT, command = self.terminal)
        menu.tk_popup(event.x_root, event.y_root, 0)

    def textPadGenerateCut(self, event=None):
        #self.textPad.event_generate('<<Cut>>')
        self.textPad.cut()
        return 'break'
    
    def textPadGenerateCopy(self, event=None):
        #self.textPad.event_generate('<<Copy>>')
        self.textPad.copy()
        return 'break'

        
    def textPadGeneratePaste(self, event=None):
        #self.textPad.event_generate('<<Paste>>')
        self.textPad.paste()
        return 'break'

    
    def textPadHighlightAll(self):
        text = self.textPad.get("1.0", "end")
        
        lines = text.count('\n')
        overlord = self.master.master.master
        
        self.textPad.delete('1.0', tk.END)
        self.textPad.insert("1.0", text)
        overlord.title('Loading ...')
        self.textPad.config(cursor="X_cursor")
        self.textPad.highlightAll2(lines, overlord)
        self.textPad.config(cursor='xterm')
        self.textPad.update()
    
    def textPadSelectAll(self):
        self.textPad.tag_add('sel', '1.0', 'end')
        self.textPad.focus_force()
    
    def textPadGenerateGoto(self, event=None):
        GotoDialog(self.textPad)
    
    def linenumberSelect(self, event):
        obj = event.widget.find_overlapping(event.x, event.y, event.x, event.y)
        line = self.linenumber.itemcget(obj, "text")
        if line:
            self.textPad.tag_add('sel', '%d.0' % int(line), '%d.end' % int(line))
            self.textPad.focus_force()
        else:
            return
            
    def on_change(self, event):
        self.linenumber.redraw()

    def tabChanged(self, event=None):
        tabs = self.notebook.tabs()
        
        if not tabs:
            return
        
        id = self.notebook.index(self.notebook.select())
        textPad = self.TEXTPADS[id]
        textPad.clipboard = self.textPad.clipboard
        self.textPad = textPad

        
        self.linenumber = self.LINENUMBERS[id]
        self.textPad.entry = self.autocompleteEntry
 
        # bind the linenumber widget
        self.linenumber.bind('<ButtonRelease-1>', self.linenumberSelect)
        self.linenumber.bind('<ButtonRelease-3>', self.linenumberPopUp)


        #print(self.textPad.filename)
        filename = self.textPad.filename
        
        if filename:
            self.master.master.master.title(self.textPad.filename)
            
            # change directory
            dirlist = filename.split('/')[:-1]
            directory = ''
            for item in dirlist:
                directory += item + '/'
                os.chdir(directory)
                for i in self.master.master.leftPanel.tree.get_children():
                    self.master.master.leftPanel.tree.delete(i)
                path = '.'
                abspath = os.path.abspath(path)
                root_node = self.master.master.leftPanel.tree.insert('', 'end', text=abspath, open=True)
                self.master.master.leftPanel.process_directory(root_node, abspath)
                self.master.master.leftPanel.refreshTree()


        else:
            self.master.master.master.title("Cross-Viper 1.0")
        
        
    
    def closeContext(self, event):
        tabs = self.notebook.tabs()
        if not tabs:
            return

        x = len(self.TEXTPADS) - 1
        self.notebook.select(x)
        self.tabChanged()
        self.master.master.master.title(self.textPad.filename)
        
        menu = tk.Menu(self.notebook, tearoff=False, background='#000000',foreground='white',
                activebackground='green', activeforeground='white')
        menu.add_command(label='Close', compound=tk.LEFT, command=self.closeTab)
        menu.tk_popup(event.x_root, event.y_root, 0)
        
    def closeTab(self, event=None):
        filename = self.textPad.filename
        if filename:
            if filename.endswith('*'):
                dialog = MessageYesNoDialog(self, 'File not saved', '\nSave now ?\n\n')
                result = dialog.result

                if result == 1:
                    self.save()
                    
                else:
                    i = len(self.TEXTPADS)
                    x = len(self.TEXTPADS) - 1

                    self.notebook.forget(x)
                    self.TEXTPADS.pop(x, None)
        
                    self.tabChanged()
                    self.linenumber.redraw()
                    return
                    
                    
        i = len(self.TEXTPADS)
        x = len(self.TEXTPADS) - 1

        self.notebook.forget(x)
        self.TEXTPADS.pop(x, None)
        
        self.tabChanged()
        self.linenumber.redraw()
        
    def new(self, event=None):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='noname', )

        textPad = TextPad(frame, undo=True, maxundo=-1, autoseparators=True)
        textPad.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        textScrollY = tk.Scrollbar(textPad, bg="#424242", troughcolor="#2d2d2d", highlightcolor="green", activebackground="green", highlightbackground="gray")
        textScrollY.config(cursor="double_arrow")
        textPad.configure(yscrollcommand=textScrollY.set)
        textScrollY.config(command=textPad.yview)
        textScrollY.config(cursor="left_ptr")
        textPad.configure(yscrollcommand=textScrollY.set)
        textScrollY.config(command=textPad.yview)
        textScrollY.pack(side=tk.RIGHT, fill=tk.Y)

        
        linenumber = TextLineNumbers(frame, width=35, bg='black')
        linenumber.attach(textPad)
        linenumber.pack(side="left", fill="y")
        
        textPad.bind("<<Change>>", self.on_change)
        textPad.bind("<Configure>", self.on_change)
        
        # Shortcuts
        textPad = self.shortcutBinding(textPad)

        l = len(self.notebook.tabs())
        l = l - 1

        self.TEXTPADS[l] = textPad
        self.LINENUMBERS[l] = linenumber
        x = len(self.TEXTPADS) - 1
        self.notebook.select(x)

        self.tabChanged()
        linenumber.redraw()
        
    def open(self, event=None, file=None):
        if len(self.TEXTPADS) -1 == -1:
            self.new()
            
        if not file:
            dir = os.getcwd()
            dir = self.checkPath(dir)
            
            dialog = OpenFileDialog(self, 'Open', 'Select File:')
            result = dialog.result
            obj = dialog.selected
            
            if result == 0:
                os.chdir(dir)
                self.leftPanel.refreshTree()
                return
            
            if obj is not None:
                if '>' in obj:
                    os.chdir(dir)
                    self.leftPanel.refreshTree()
                    return
                
                elif '/' in obj:
                    os.chdir(dir)
                    self.leftPanel.refreshTree()
                    return
                
                else:
                    filename = os.getcwd() + '/' + obj
                    filename = self.checkPath(filename)
            else:
                os.chdir(dir)
                self.leftPanel.refreshTree()
                return

        else:
            filename = file
        
        #print(file)
        makeNew = True
        
        if filename:
            index = None
            if self.textPad.filename == None or self.textPad.filename == 'noname':
                makeNew = False
                index = self.notebook.index(self.notebook.select())

            try:
                # count lines first
                linesInFile = 0
                theFile = open(filename, "r")
                while 1:
                    buffer = theFile.read(8192*1024)
                    if not buffer: break
                    linesInFile += buffer.count('\n')
                theFile.close()
                if linesInFile == 0:
                    linesInFile = 1
                
                with open(filename, 'r') as f:
                    text = f.read()
                    if makeNew:
                        self.new()
                    
                    if index == None:
                        index = len(self.TEXTPADS) - 1
                        #print('l', l)
                        self.notebook.select(index)
                    self.notebook.select(index)
                    self.update()
                    self.tabChanged()
                    
                    self.textPad.delete('1.0', tk.END)
                    self.textPad.insert("1.0", text)
                    self.leftPanel.refreshTree()

                    
                    overlord = self.master.master.master
                    
                    overlord.title('Loading ...')
                    self.textPad.config(cursor="X_cursor")
                    self.textPad.update()
                    #print(linesInFile)
                    self.textPad.highlightAll2(linesInFile, overlord)
                    self.textPad.config(cursor='xterm')
                    self.textPad.update()
                    self.textPad.filename = filename
                    file = filename.split('/')[-1]
                    self.notebook.tab(index, text=file)
                    overlord.title(self.textPad.filename)
                    self.textPad.updateAutoCompleteList()
                    
                    self.tabChanged()
                    #self.textPad.mark_set("insert", "1.0")
                    
            except Exception as e:
                #print(str(e))
                MessageDialog(self, 'Error', '\n' + str(e) + '\n')
                self.leftPanel.refreshTree()
                self.leftPanel.tree.focus_set()
            return
        
        self.leftPanel.refreshTree()

    def save(self, event=None):
        if len(self.TEXTPADS) -1 == -1:
            return
            
        if self.textPad.filename == None:
            d = os.getcwd()
            d = self.checkPath(d)
            dialog = SaveFileDialog(self, 'Save As', 'Enter Filename')
            self.leftPanel.refreshTree()
            result = dialog.result
            filename = dialog.filename


            if filename:
                try:
                    with open(filename, 'w') as f:
                        text = self.textPad.get("1.0",'end-1c')
                        f.write(text)
                        #l = len(self.TEXTPADS) - 1  # nicht richtig
                        id = self.notebook.index(self.notebook.select())
                        
                        self.textPad.filename = filename
                        file = filename.split('/')[-1]
                        self.notebook.tab(id, text=file)
                        self.master.master.master.title(self.textPad.filename)
                        self.tabChanged()
                        
                except Exception as e:
                    MessageDialog(self, 'Error', '\n' + str(e) + '\n')
                    return
        else:
            filename = self.textPad.filename
            if filename.endswith('*'):
                filename = filename.replace('*', '')
            
            try:
                with open(filename, 'w') as f:
                    text = self.textPad.get("1.0",'end-1c')
                    f.write(text)
                    #l = len(self.TEXTPADS) - 1
                    id = self.notebook.index(self.notebook.select())
                    self.textPad.filename = filename
                    file = filename.split('/')[-1]
                    self.notebook.tab(id, text=file)
                    self.master.master.master.title(self.textPad.filename)
                    self.tabChanged()
                    file = filename.split('/')[-1]
                    x = self.notebook.index(self.notebook.select())
                    self.notebook.tab(x, text=file)
            
            except Exception as e:
                    MessageDialog(self, 'Error', '\n' + str(e) + '\n')
                    return
        
        self.textPad.focus_set()
        self.leftPanel.refreshTree()
        
    def saveAs(self, event=None):

        if len(self.TEXTPADS) -1 == -1:
            return

        dialog = SaveFileDialog(self, 'Save As', 'Enter Filename')
        self.leftPanel.refreshTree()
        result = dialog.result
        filename = self.checkPath(dialog.filename)
        

        if result == 0:
            self.textPad.focus_set()
            self.rightPanel.refreshTree()
            return
        
        if filename.startswith('>'):
            filename = None
            self.textPad.focus_set()
            return
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    text = self.textPad.get("1.0",'end-1c')
                    f.write(text)
                    #l = len(self.TEXTPADS) - 1  # nicht richtig
                    id = self.notebook.index(self.notebook.select())
                        
                    self.textPad.filename = filename
                    file = filename.split('/')[-1]
                    self.notebook.tab(id, text=file)
                    self.master.master.master.title(self.textPad.filename)
                    self.tabChanged()
                    
            except Exception as e:
                MessageDialog(self, 'Error', '\n' + str(e) + '\n')
                self.leftPanel.refreshTree()

                return
        
        self.leftPanel.refreshTree()
        self.textPad.focus_set()


    def checkPath(self, dir):
        if dir:
            if '\\' in dir:
                path = dir.replace('\\', '/')
            else:
                path = dir
            return path

    
    def print(self, event=None):
        if platform.system().lower() == 'windows':
            if self.textPad:
                if self.textPad.filename is not None:
                    subprocess.call(['notepad.exe', '/p', self.textPad.filename])
        else:
            if self.textPad:
                if self.textPad.filename is not None:
                    subprocess.call(['lpr', self.textPad.filename])
        
        
    def undo(self, event=None):
        index = self.textPad.index("insert linestart")
        line = index.split('.')[0]
      
        line = int(line)
        
        try:
            self.textPad.edit_undo()
            self.textPad.focus_set()
            self.textPad.highlight(lineNumber=line)
            self.textPad.highlightThisLine()
        
        except Exception as e:
            MessageDialog(self, 'Error', '\n' + str(e) + '\n')
        
        
    
    def redo(self, event=None):
        #x = self.textPad.edit_modified()
        index = self.textPad.index('insert linestart')
        line = index.split('.')[0]
        
        line = int(line)
        
        try:
            self.textPad.edit_redo()
            self.textPad.focus_set()
            self.textPad.highlight(lineNumber=line)
            self.textPad.highlightThisLine()
        
        except Exception as e:
            MessageDialog(self, 'Error', '\n' + str(e) + '\n')
        
        
    def zoomIn(self, event=None):
        if self.textPad.fontSize < 30:
            self.textPad.fontSize += 1
            self.textPad.configFont()
            
            self.linenumber.fontSize +=1
            self.linenumber.configFont()
            self.linenumber.redraw()
            
            
    def zoomOut(self, event=None):
        if self.textPad.fontSize > 5:
            self.textPad.fontSize -= 1
            self.textPad.configFont()
            
            self.linenumber.fontSize -=1
            self.linenumber.configFont()
            self.linenumber.redraw()

    
    def settings(self, event=None):
        dialog = SettingsDialog(self)
    
    def search(self, start=None):
        self.textPad.tag_remove('sel', "1.0", tk.END)
        
        toFind = self.searchBox.get()
        pos = self.textPad.index(tk.INSERT)
        result = self.textPad.search(toFind, str(pos), stopindex=tk.END)
        
        if result:
            length = len(toFind)
            row, col = result.split('.')
            end = int(col) + length
            end = row + '.' + str(end)
            self.textPad.tag_add('sel', result, end)
            self.textPad.mark_set('insert', end)
            self.textPad.see(tk.INSERT)
            self.textPad.focus_force()
            self.searchBox.focus()
        else:
            self.textPad.mark_set('insert', '1.0')
            self.textPad.see(tk.INSERT)
            self.textPad.focus()
            self.setEndMessage(400)
            self.searchBox.focus()
            return

    
    def setMessage(self, text, seconds):
            self.textPad.entry.config(text=text)
            self.textPad.update()
            self.after(seconds, self.textPad.entry.config(text='---'))
            self.textPad.update()
        
    def setEndMessage(self, seconds):
            pathList = __file__.replace('\\', '/')
            pathList = __file__.split('/')[:-1]
        
            self.dir = ''
            for item in pathList:
                self.dir += item + '/'
            print(self.dir)
            #self.textPad.entry.config(text=text)
            #self.textPad.update()
            canvas = tk.Canvas(self.textPad, width=64, height=64)
            x = self.textPad.winfo_width() / 2
            y = self.textPad.winfo_height() / 2
            print('x', x)
            print('y', y)
            canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            #canvas.create_line(0, 50, 200, 50, fill="#476042")
            image = tk.PhotoImage(file = self.dir + 'images/last.png')
            canvas.create_image(0, 0,  anchor=tk.NW, image=image)
            self.textPad.update()
            self.after(seconds, self.textPad.entry.config(text='---'))
            canvas.destroy()
            self.textPad.update()

    

                
    def overview(self, event=None):
        ViewDialog(self.textPad, "Class - Overview", self.textPad)
        
    
    def interpreter(self):
        c = Configuration()     # -> in configuration.py
        system = c.getSystem()
        interpreterCommand = c.getInterpreter(system)

        thread = RunThread(interpreterCommand)
        thread.start()

    
    def terminal(self):
        c = Configuration()     # -> in configuration.py
        system = c.getSystem()
        terminalCommand = c.getTerminal(system)

        thread = RunThread(terminalCommand)
        thread.start()

    
    def run(self):
        if not self.textPad:
            return
        
        filepath = self.textPad.filename
        
        if not filepath:
            return
        
        self.save()

        file = filepath.split('/')[-1]
    
        c = Configuration()     # -> in configuration.py
        system = c.getSystem()
        runCommand = c.getRun(system).format(file)
                
        thread = RunThread(runCommand)
        thread.start()

    def runSudo(self):
        c = Configuration()
        self.password = c.getPassword()
        
        if not self.textPad:
            return
        
        filepath = self.textPad.filename
        
        if not filepath:
            return
        
        if not self.password:
            dialog = MessageSudoYesNoDialog(self, 'Enter password', '')
            password = dialog.password
            result = dialog.result
                        
            if result == 1:
                password = password

            else:
                password = None
                return
        else:
            password = self.password
            
        self.save()

        file = filepath.split('/')[-1]

        system = c.getSystem()
        runCommand = c.getRun(system).format(file)
        
        os.popen("sudo -S %s"%(runCommand), 'w').write(password + '\n')

            

class CrossViper(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, width=1000, height=100)
        self.pack(expand=True, fill=tk.BOTH)
        self.initUI()
        self.initStyle()
    

    def initStyle(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Treeview", background="black", 
                fieldbackground="black", foreground="white",
                selectbackground='green')
        self.style.configure("Treeview.Heading", background="black", foreground='white', relief='flat')
        self.style.map('Treeview.Heading', 
            foreground=[('pressed', 'white'),
                        ('focus', 'white'),
                        ('active', 'white')],
            background=[('pressed', '!focus', 'green'),
                        ('active', 'green')],
            highlightcolor=[('focus', 'green'),
                        ('!focus', 'white')],
            activerelief=[('pressed', 'groove'),
                    ('!pressed', 'ridge')])

        self.style.configure('TCheckbutton', background='black',
                fieldbackground='black', foreground='white')

        self.style.configure('TRadiobutton', background='black',
                fieldbackground='black', foreground='white')
        self.style.map('TRadiobutton',
            foreground=[('pressed', 'white'),
                        ('focus', 'white'),
                        ('active', 'white')],
            background=[('pressed', '!focus', 'green'),
                        ('active', 'green')],
            highlightcolor=[('focus', 'green'),
                        ('!focus', 'white')],
            activerelief=[('pressed', 'groove'),
                    ('!pressed', 'ridge')])


        self.style.configure('TSpinbox', background='black',
                fieldbackground='black', foreground='white')

        self.style.configure('TNotebook', background='black',
                fieldbackground='black', foreground='white')
        self.style.configure('TNotebook.Tab', background='black',
                fieldbackground='black', foreground='white')
        self.style.map('TNotebook.Tab',
            foreground=[('selected', 'yellow')],
            background=[('selected', 'black')])
            
        self.style.configure('TFrame', background='black',
                fieldbackground='black', foreground='white')

        self.style.configure('TLabel', background='black',
                fieldbackground='black', foreground='green')
        self.style.configure("White.TLabel", background='black',
                fieldbackground='black', foreground="white")
        self.style.configure("Red.TLabel", background='black',
                fieldbackground='black', foreground="red")

        self.style.configure('TPanedwindow', background='black',
                fieldbackground='black', foreground='white')

        self.style.configure('TEntry', background='black',
                fieldbackground='black', foreground='white')

        self.style.map('TEntry',
            foreground=[('pressed', 'white'),
                        ('focus', 'white'),
                        ('active', 'white')],
            background=[('pressed', '!focus', 'green'),
                        ('active', 'green')],
            highlightcolor=[('focus', 'green'),
                        ('!focus', 'white')],
            activerelief=[('pressed', 'groove'),
                    ('!pressed', 'ridge')])


        self.style.configure('TButton', background='black',
                fieldbackground='black', foreground='white')
        self.style.configure('Red', background='red')
        self.style.map('TButton',
            foreground=[('pressed', 'white'),
                        ('focus', 'white'),
                        ('active', 'white')],
            background=[('pressed', '!focus', 'green'),
                        ('active', 'green')],
            highlightcolor=[('focus', 'green'),
                        ('!focus', 'white')],
            activerelief=[('pressed', 'groove'),
                    ('!pressed', 'ridge')])

        
    def initUI(self):
        self.panedWindow = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.panedWindow.pack(fill=tk.BOTH, expand=1)
        self.rightPanel = RightPanel(self.panedWindow)
        #self.rightPanel.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        self.leftPanel = LeftPanel(self.panedWindow, self.rightPanel)
        
        # to know each other for communication
        self.leftPanel.rightPanel = self.rightPanel
        self.rightPanel.leftPanel = self.leftPanel
        
        #self.leftPanel.pack(side=tk.LEFT, fill=tk.Y)
        
        self.panedWindow.add(self.leftPanel)
        self.panedWindow.add(self.rightPanel)
        
        self.rightPanel.textPad.focus_set()

def center(win):
    # Center the root screen
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

if __name__ == '__main__':
    root = tk.Tk()

    app = CrossViper(master=None)
    app.master.title('Cross-Viper 1.0')
    #app.master.minsize(width=1000, height=800)
    root.geometry("1000x800+100+100")
    
    root['bg'] = 'black'
    #root.configure(cursor = "left_ptr green")


    dir = str(os.path.dirname(os.path.abspath(__file__))) + '/'
    dir += 'images/crossviper.ico'
    img = tk.PhotoImage(dir)
    root.tk.call('wm', 'iconphoto', root._w, img)
    
    center(root)
    app.mainloop()

###################################################################
# Yeni Viper IDE Sınıfı - 6502 Assembly & C64 odaklı
###################################################################

class ViperIDE(tk.Tk):
    """
    Viper IDE Ana Sınıfı
    6502 Assembly ve C64 odaklı geliştirme ortamı
    """
    
    def __init__(self):
        super().__init__()
        
        # Ana pencere ayarları
        self.title("Viper IDE - 6502 Assembly & C64 Development Environment")
        self.geometry("1200x800")
        
        # Sistem değişkenleri
        self.dir = os.path.dirname(os.path.abspath(__file__)) + "/"
        self.current_file = None
        self.clipboard_file = None
        
        # Syntax highlighter
        if SYNTAX_HIGHLIGHTER_AVAILABLE:
            self.syntax_highlighter = None  # Text widget oluşturulduktan sonra init edilecek
        else:
            self.syntax_highlighter = None
        
        # D64 System entegrasyonu
        if D64_SYSTEM_AVAILABLE:
            self.disassembler = None
            self.format_bridge = DisassemblyFormatBridge()
            self.assembly_formatters = AssemblyFormatters()
        
        # GUI oluştur
        self.create_gui()
        
        # Configuration yükle
        self.load_configuration()
        
    def create_gui(self):
        """Ana GUI arayüzünü oluşturur"""
        
        # Ana menü
        self.create_menubar()
        
        # Toolbar
        self.create_toolbar()
        
        # Ana panel (Notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # File Explorer Tab
        self.create_file_explorer_tab()
        
        # Code Editor Tab
        self.create_code_editor_tab()
        
        # Disassembly Tab (D64 system varsa)
        if D64_SYSTEM_AVAILABLE:
            self.create_disassembly_tab()
        
        # Status bar
        self.create_status_bar()
    
    def create_menubar(self):
        """Menü çubuğunu oluşturur"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        
        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V")
        
        # Assembly Menu
        asm_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Assembly", menu=asm_menu)
        asm_menu.add_command(label="Disassemble D64", command=self.disassemble_d64)
        asm_menu.add_command(label="Format Convert", command=self.format_convert)
        asm_menu.add_separator()
        asm_menu.add_command(label="Syntax Check", command=self.syntax_check)
        
        # Tools Menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Memory Map", command=self.show_memory_map)
        tools_menu.add_command(label="Opcode Reference", command=self.show_opcode_reference)
        
        # View Menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle File Explorer", command=self.toggle_file_explorer)
        view_menu.add_command(label="Toggle Syntax Highlighting", command=self.toggle_syntax_highlighting)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About Viper IDE", command=self.show_about)
        help_menu.add_command(label="6502 Reference", command=self.show_6502_reference)
    
    def create_toolbar(self):
        """Toolbar oluşturur"""
        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        
        # Toolbar buttons
        new_btn = tk.Button(toolbar, text="New", command=self.new_file)
        new_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        open_btn = tk.Button(toolbar, text="Open", command=self.open_file)
        open_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        save_btn = tk.Button(toolbar, text="Save", command=self.save_file)
        save_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Separator
        separator = tk.Frame(toolbar, width=2, bd=1, relief=tk.SUNKEN)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
        # Assembly format selector
        if D64_SYSTEM_AVAILABLE:
            tk.Label(toolbar, text="Format:").pack(side=tk.LEFT, padx=2)
            self.format_var = tk.StringVar(value="native")
            format_combo = ttk.Combobox(toolbar, textvariable=self.format_var, 
                                      values=list(self.assembly_formatters.supported_formats.keys()),
                                      state="readonly", width=12)
            format_combo.pack(side=tk.LEFT, padx=2, pady=2)
        
        toolbar.pack(side=tk.TOP, fill=tk.X)
    
    def create_file_explorer_tab(self):
        """File Explorer tab'ını oluşturur"""
        explorer_frame = tk.Frame(self.notebook)
        self.notebook.add(explorer_frame, text="Files")
        
        # Treeview for file browser
        self.file_tree = ttk.Treeview(explorer_frame)
        self.file_tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(explorer_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_tree.configure(yscrollcommand=v_scrollbar.set)
        
        # Initialize with current directory
        self.populate_file_tree()
        
        # Bind events
        self.file_tree.bind("<Double-1>", self.on_file_double_click)
    
    def create_code_editor_tab(self):
        """Code Editor tab'ını oluşturur"""
        editor_frame = tk.Frame(self.notebook)
        self.notebook.add(editor_frame, text="Editor")
        
        # Text editor with syntax highlighting
        if VIPER_MODULES_AVAILABLE:
            try:
                self.text_editor = TextPad(editor_frame)
                self.text_editor.pack(fill=tk.BOTH, expand=True)
            except:
                # Fallback to basic text widget
                self.text_editor = tk.Text(editor_frame, wrap=tk.NONE, font=('Courier', 10))
                self.text_editor.pack(fill=tk.BOTH, expand=True)
        else:
            self.text_editor = tk.Text(editor_frame, wrap=tk.NONE, font=('Courier', 10))
            self.text_editor.pack(fill=tk.BOTH, expand=True)
        
        # Syntax highlighter'ı initialize et
        if SYNTAX_HIGHLIGHTER_AVAILABLE and hasattr(self, 'text_editor'):
            self.syntax_highlighter = HybridHighlighter(self.text_editor)
        
        # Scrollbars for editor
        v_scrollbar = ttk.Scrollbar(editor_frame, orient=tk.VERTICAL, command=self.text_editor.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_editor.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(editor_frame, orient=tk.HORIZONTAL, command=self.text_editor.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_editor.configure(xscrollcommand=h_scrollbar.set)
        
        # Bind events for syntax highlighting
        self.text_editor.bind('<KeyRelease>', self.on_text_change)
    
    def create_disassembly_tab(self):
        """Disassembly tab'ını oluşturur (sadece D64 system varsa)"""
        if not D64_SYSTEM_AVAILABLE:
            return
        
        disasm_frame = tk.Frame(self.notebook)
        self.notebook.add(disasm_frame, text="Disassembly")
        
        # D64 file selector
        file_frame = tk.Frame(disasm_frame)
        file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(file_frame, text="D64 File:").pack(side=tk.LEFT)
        self.d64_file_var = tk.StringVar()
        d64_entry = tk.Entry(file_frame, textvariable=self.d64_file_var)
        d64_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5,0))
        
        browse_btn = tk.Button(file_frame, text="Browse", command=self.browse_d64_file)
        browse_btn.pack(side=tk.RIGHT, padx=(5,0))
        
        disasm_btn = tk.Button(file_frame, text="Disassemble", command=self.disassemble_d64)
        disasm_btn.pack(side=tk.RIGHT, padx=(5,0))
        
        # Disassembly output
        self.disasm_text = tk.Text(disasm_frame, wrap=tk.NONE, font=("Courier", 10))
        self.disasm_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Syntax highlighter for disassembly
        if SYNTAX_HIGHLIGHTER_AVAILABLE:
            self.disasm_highlighter = Assembly6502Highlighter(self.disasm_text)
        
        # Scrollbars
        disasm_v_scroll = ttk.Scrollbar(disasm_frame, orient=tk.VERTICAL, command=self.disasm_text.yview)
        disasm_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.disasm_text.configure(yscrollcommand=disasm_v_scroll.set)
    
    def create_status_bar(self):
        """Status bar oluşturur"""
        self.status_bar = tk.Label(self, text="Ready - Viper IDE v1.0", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def on_text_change(self, event=None):
        """Text değiştiğinde syntax highlighting'i günceller"""
        if self.syntax_highlighter:
            # Throttle syntax highlighting to avoid performance issues
            if hasattr(self, '_syntax_after_id'):
                self.after_cancel(self._syntax_after_id)
            
            self._syntax_after_id = self.after(500, self.syntax_highlighter.highlight)
    
    def populate_file_tree(self):
        """File tree'yi doldurur"""
        try:
            path = os.getcwd()
            root_node = self.file_tree.insert('', 'end', text=path, open=True)
            self.process_directory(root_node, path)
        except Exception as e:
            print(f"File tree populate hatası: {e}")
    
    def process_directory(self, parent, path):
        """Dizini process eder ve tree'ye ekler"""
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                
                if os.path.isdir(item_path):
                    node = self.file_tree.insert(parent, 'end', text=item, open=False)
                else:
                    self.file_tree.insert(parent, 'end', text=item)
        except PermissionError:
            pass
    
    # Event handlers
    def on_file_double_click(self, event):
        """File tree'de double click"""
        selection = self.file_tree.selection()
        if selection:
            item = selection[0]
            item_text = self.file_tree.item(item, 'text')
            
            if '.' in item_text:
                self.open_file_from_tree(item)
    
    def open_file_from_tree(self, tree_item):
        """Tree'den dosya aç"""
        path_parts = []
        current = tree_item
        
        while current:
            path_parts.insert(0, self.file_tree.item(current, 'text'))
            current = self.file_tree.parent(current)
        
        full_path = os.path.join(*path_parts)
        self.open_file(full_path)
    
    def new_file(self):
        """Yeni dosya oluştur"""
        if hasattr(self, 'text_editor'):
            self.text_editor.delete('1.0', tk.END)
        self.current_file = None
        self.status_bar.config(text="New file - Viper IDE")
    
    def open_file(self, filename=None):
        """Dosya aç"""
        if not filename:
            filename = filedialog.askopenfilename(
                title="Open File",
                filetypes=[
                    ("Assembly files", "*.asm *.s"),
                    ("C64 files", "*.prg *.d64"),
                    ("BASIC files", "*.bas *.basic"),
                    ("All files", "*.*")
                ]
            )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    if hasattr(self, 'text_editor'):
                        self.text_editor.delete('1.0', tk.END)
                        self.text_editor.insert('1.0', content)
                
                self.current_file = filename
                self.status_bar.config(text=f"Opened: {os.path.basename(filename)} - Viper IDE")
                
                # Apply syntax highlighting
                if self.syntax_highlighter:
                    self.syntax_highlighter.highlight()
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")
    
    def save_file(self):
        """Dosyayı kaydet"""
        if not self.current_file:
            self.save_file_as()
            return
        
        try:
            if hasattr(self, 'text_editor'):
                content = self.text_editor.get('1.0', tk.END + '-1c')
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                self.status_bar.config(text=f"Saved: {os.path.basename(self.current_file)} - Viper IDE")
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")
    
    def save_file_as(self):
        """Farklı kaydet"""
        filename = filedialog.asksaveasfilename(
            title="Save File As",
            filetypes=[
                ("Assembly files", "*.asm"),
                ("BASIC files", "*.bas"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            self.current_file = filename
            self.save_file()
    
    def browse_d64_file(self):
        """D64 dosyası seç"""
        filename = filedialog.askopenfilename(
            title="Select D64 File",
            filetypes=[("D64 files", "*.d64"), ("All files", "*.*")]
        )
        
        if filename:
            self.d64_file_var.set(filename)
    
    def disassemble_d64(self):
        """D64 dosyasını disassemble et"""
        if not D64_SYSTEM_AVAILABLE:
            messagebox.showerror("Error", "D64 system not available")
            return
        
        d64_file = self.d64_file_var.get()
        if not d64_file or not os.path.exists(d64_file):
            messagebox.showerror("Error", "Please select a valid D64 file")
            return
        
        try:
            from d64_reader import D64Reader
            
            reader = D64Reader()
            files = reader.read_d64(d64_file)
            
            for file_info in files:
                if file_info['type'] == 'PRG':
                    prg_data = file_info['data']
                    
                    start_addr = prg_data[0] + (prg_data[1] << 8)
                    machine_code = prg_data[2:]
                    
                    disassembler = ImprovedDisassembler(
                        start_addr, 
                        machine_code,
                        assembly_format=self.format_var.get() if hasattr(self, 'format_var') else 'native'
                    )
                    
                    asm_output = disassembler.get_assembly_output()
                    
                    if hasattr(self, 'disasm_text'):
                        self.disasm_text.delete('1.0', tk.END)
                        self.disasm_text.insert('1.0', asm_output)
                        
                        # Apply syntax highlighting to disassembly
                        if hasattr(self, 'disasm_highlighter'):
                            self.disasm_highlighter.highlight()
                    
                    self.status_bar.config(text=f"Disassembled: {file_info['name']} - Viper IDE")
                    break
            
        except Exception as e:
            messagebox.showerror("Error", f"Disassembly failed: {e}")
    
    def format_convert(self):
        """Format çevirme"""
        if not D64_SYSTEM_AVAILABLE:
            messagebox.showerror("Error", "Format conversion not available")
            return
        
        source_format = simpledialog.askstring("Format Convert", "Source format:")
        target_format = simpledialog.askstring("Format Convert", "Target format:")
        
        if source_format and target_format:
            try:
                if hasattr(self, 'text_editor'):
                    content = self.text_editor.get('1.0', tk.END + '-1c')
                    
                    result = self.format_bridge.convert_format(content, source_format, target_format)
                    
                    if result.success:
                        self.text_editor.delete('1.0', tk.END)
                        self.text_editor.insert('1.0', result.output)
                        self.status_bar.config(text=f"Converted: {source_format} → {target_format} - Viper IDE")
                        
                        if self.syntax_highlighter:
                            self.syntax_highlighter.highlight()
                    else:
                        messagebox.showerror("Error", f"Conversion failed: {result.error_message}")
                        
            except Exception as e:
                messagebox.showerror("Error", f"Format conversion error: {e}")
    
    def syntax_check(self):
        """Syntax kontrolü"""
        messagebox.showinfo("Syntax Check", "Syntax check functionality will be implemented")
    
    def show_memory_map(self):
        """C64 memory map göster"""
        memory_info = """C64 Memory Map:
$0000-$00FF: Zero Page
$0100-$01FF: Stack  
$0200-$03FF: Free RAM
$0400-$07FF: Screen Memory
$0800-$9FFF: Free RAM (38K)
$A000-$BFFF: BASIC ROM
$C000-$CFFF: Free RAM
$D000-$DFFF: I/O Area
  $D000-$D3FF: VIC-II
  $D400-$D7FF: SID
  $D800-$DBFF: Color RAM
  $DC00-$DCFF: CIA #1
  $DD00-$DDFF: CIA #2
$E000-$FFFF: KERNAL ROM"""
        messagebox.showinfo("C64 Memory Map", memory_info)
    
    def show_opcode_reference(self):
        """6502 opcode referansını göster"""
        opcode_info = """6502 Instruction Set:
Load/Store: LDA, LDX, LDY, STA, STX, STY
Transfer: TAX, TAY, TXA, TXS, TSX, TYA
Stack: PHA, PHP, PLA, PLP
Arithmetic: ADC, SBC, INC, INX, INY, DEC, DEX, DEY
Logic: AND, ORA, EOR, BIT
Shift: ASL, LSR, ROL, ROR
Compare: CMP, CPX, CPY
Branch: BCC, BCS, BEQ, BMI, BNE, BPL, BVC, BVS
Jump: JMP, JSR, RTS, RTI
Flag: CLC, CLD, CLI, CLV, SEC, SED, SEI
Other: BRK, NOP"""
        messagebox.showinfo("6502 Opcode Reference", opcode_info)
    
    def toggle_file_explorer(self):
        """File explorer'ı aç/kapat"""
        pass
    
    def toggle_syntax_highlighting(self):
        """Syntax highlighting aç/kapat"""
        if self.syntax_highlighter:
            self.syntax_highlighter.highlight()
    
    def show_about(self):
        """Hakkında penceresi"""
        about_text = """Viper IDE v1.0
6502 Assembly & C64 Development Environment

Based on CrossViper, enhanced for:
- 6502 Assembly syntax highlighting
- C64 BASIC support
- D64 file disassembly
- Multiple assembly formats
- Bridge system integration

Created for C64 reverse engineering and development."""
        messagebox.showinfo("About Viper IDE", about_text)
    
    def show_6502_reference(self):
        """6502 referans rehberi"""
        ref_text = """6502 Processor Reference:
- 8-bit microprocessor
- 64KB address space
- 3 registers: A (Accumulator), X, Y (Index)
- 256-byte stack ($0100-$01FF)
- 7 status flags: N, V, B, D, I, Z, C

Addressing Modes:
- Immediate: #$nn
- Zero Page: $nn
- Absolute: $nnnn
- Indexed: $nnnn,X or $nnnn,Y
- Indirect: ($nnnn)"""
        messagebox.showinfo("6502 Reference", ref_text)
    
    def load_configuration(self):
        """Konfigürasyon yükle"""
        try:
            if VIPER_MODULES_AVAILABLE:
                self.config = Configuration()
            else:
                self.config = None
        except:
            self.config = None

###################################################################
def run_viper_ide():
    """Viper IDE'yi çalıştır"""
    try:
        print("🐍 Viper IDE başlatılıyor...")
        app = ViperIDE()
        
        # Icon ayarla (eğer varsa)
        try:
            if os.path.exists("viper_images/crossviper.ico"):
                img = tk.PhotoImage(file="viper_images/crossviper.ico")
                app.tk.call('wm', 'iconphoto', app._w, img)
        except:
            pass
        
        print("✅ Viper IDE başlatıldı")
        app.mainloop()
        
    except Exception as e:
        print(f"❌ Viper IDE çalıştırma hatası: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_viper_ide()
