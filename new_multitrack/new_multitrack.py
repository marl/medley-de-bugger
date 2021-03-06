import sys
import os
import glob
import yaml
from PyQt4 import QtGui, QtCore
from functools import partial
import multitrack_utils as mu
from validation import get_dur
from validation import check_audio
from validation import create_problems
from validation import check_multitrack
import sox

INST_TAXONOMY = 'taxonomy.yaml'
ICON_FILE = 'medley-icon.png'


class FilePrompt(QtGui.QDialog):
    def __init__(self, parent=None):

        super(FilePrompt, self).__init__(parent)

        self.basedir = '.'

        self.mix_btn = QtGui.QPushButton('Select the Mix...', self)
        self.mix_btn.clicked.connect(self.findMix)

        self.mix_path = ""
        self.mix_choice = QtGui.QLabel()

        self.stem_btn = QtGui.QPushButton('Select the Stem Folder...', self)
        self.stem_btn.clicked.connect(self.findStems)

        self.stem_path = ""
        self.stem_choice = QtGui.QLabel()

        self.raw_btn = QtGui.QPushButton('Select the Raw Folder...', self)
        self.raw_btn.clicked.connect(self.findRaw)

        self.raw_path = ""
        self.raw_choice = QtGui.QLabel()

        self.save_btn = QtGui.QPushButton('Pick a Save location...', self)
        self.save_btn.clicked.connect(self.pickSaveDir)

        self.save_path = ""
        self.save_choice = QtGui.QLabel()

        # doesn't move to next until clicked
        self.next_btn = QtGui.QPushButton('Next', self)
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self.checkNext)

        grid = QtGui.QGridLayout()
        grid.setSpacing(10) 

        grid.addWidget(self.mix_btn, 1, 0)
        grid.addWidget(self.mix_choice, 1, 1)

        grid.addWidget(self.stem_btn, 2, 0)
        grid.addWidget(self.stem_choice, 2, 1)

        grid.addWidget(self.raw_btn, 3, 0)
        grid.addWidget(self.raw_choice, 3, 1)

        grid.addWidget(self.save_btn, 4, 0)
        grid.addWidget(self.save_choice, 4, 1)

        grid.addWidget(self.next_btn, 7, 2)

        self.setLayout(grid)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Locate Files')
        self.setWindowIcon(QtGui.QIcon('ICON_FILE'))
        self.center()

        self.show()

    def center(self):
        frame_gm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(
            QtGui.QApplication.desktop().cursor().pos())
        center_point = QtGui.QApplication.desktop().screenGeometry(
            screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def findMix(self):
        self.mix_path = str(QtGui.QFileDialog.getOpenFileName(
            self, "Select the Mix..,", '.', "Audio Files (*.wav)"))

        self.mix_choice.setText("...{}".format(self.mix_path[-30:]))
        self.basedir = os.path.dirname(self.mix_path)
        self.nextEnabled()

    def findStems(self):
        self.stem_path = str(QtGui.QFileDialog.getExistingDirectory(
            self, "Select the Stem directory...", self.basedir))
        self.stem_choice.setText("...{}".format(self.stem_path[-30:]))
        self.nextEnabled()

    def findRaw(self):
        self.raw_path = str(QtGui.QFileDialog.getExistingDirectory(
            self, "Select the raw audio directory...", self.basedir))
        self.raw_choice.setText("...{}".format(self.raw_path[-30:]))
        self.nextEnabled()

    def pickSaveDir(self):
        self.save_path = str(QtGui.QFileDialog.getExistingDirectory(
            self, "Select a save location...", self.basedir))
        self.save_choice.setText("...{}".format(self.save_path[-30:]))
        self.nextEnabled()

    def checkNext(self):
        if self.raw_path and self.stem_path and \
           self.mix_path and self.save_path:

            file_status = check_audio(
                self.raw_path, self.stem_path, self.mix_path
            )
            problems = create_problems(file_status)

            if len(problems) > 0:
                invalid_dialog = InvalidFormatCheck(problems, self, file_status, self.stem_path, self.raw_path)
                if not invalid_dialog.exec_():
                    sys.exit(-1)

            else:
                self.accept()

    def nextEnabled(self):

        if self.raw_path and self.stem_path and self.mix_path:
            self.next_btn.setEnabled(True)


# instead of ignore and continue add button to delete accidental silent files
class InvalidFormatCheck(QtGui.QDialog):
    def __init__(self, problems, raw_dialog, file_status, stem_path, raw_path):
        super(InvalidFormatCheck, self).__init__()
        self.problems = problems
        self.initUI()
        self.raw_dialog = raw_dialog
        self.stem_path = stem_path
        self.raw_path = raw_path
        self.file_status = file_status

    def initUI(self):


        self.vertical_layout = QtGui.QVBoxLayout(self)

        self.scroll_area = QtGui.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area_widget_contents = QtGui.QWidget()
        self.scroll_area_widget_contents.setGeometry(
            QtCore.QRect(0, 0, 380, 280))

        self.horizontallayout = QtGui.QHBoxLayout(
            self.scroll_area_widget_contents)

        self.grid_layout = QtGui.QGridLayout()

        self.horizontallayout.addLayout(self.grid_layout)

        self.scroll_area.setWidget(self.scroll_area_widget_contents)

        self.text_lines = []

        n_problems = len(self.problems)

        for i in range(n_problems):
            self.text_lines.append(QtGui.QLabel(self.problems[i]))
            self.text_lines[i].setText(self.problems[i])
            self.grid_layout.addWidget(self.text_lines[i])

        self.vertical_layout.addWidget(self.scroll_area)

        quit_btn = QtGui.QPushButton("Quit")
        quit_btn.clicked.connect(self.quit_clicked)

        back_btn = QtGui.QPushButton("Back")
        back_btn.clicked.connect(self.accept)

        remove_silent_btn = QtGui.QPushButton("Remove Silent Files")
        remove_silent_btn.clicked.connect(self.remove_silent_files)

        #this works for fileprompt->stem_info
        #works for 'not all stems have raw'
        #does not work for raw info -> meta

        self.grid_layout.addWidget(back_btn, n_problems, 0)
        self.grid_layout.addWidget(remove_silent_btn, n_problems, 1)
        self.grid_layout.addWidget(quit_btn, n_problems, 2)

        self.setGeometry(900, 400, 900, 400)
        self.setWindowTitle('Invalid Files')
        self.setWindowIcon(QtGui.QIcon('ICON_FILE'))
        self.center()

        self.show()

    def remove_silent_files(self):
        stem_files = glob.glob(os.path.join(self.stem_path, '*.wav'))
        raw_files = glob.glob(os.path.join(self.raw_path, '*.wav'))

        for f_path in (stem_files + raw_files):
            basename = os.path.basename(f_path)
            if not self.file_status[basename]['Silent']:
                os.remove(f_path)
        self.accept()

    def center(self):
        frame_gm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(
            QtGui.QApplication.desktop().cursor().pos())
        center_point = QtGui.QApplication.desktop().screenGeometry(
            screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def quit_clicked(self):
        QtCore.QCoreApplication.instance().quit()


class InvalidFiles(QtGui.QDialog):
    def __init__(self, problems, raw_dialog):
        super(InvalidFiles, self).__init__()
        self.problems = problems
        self.initUI()
        self.raw_dialog = raw_dialog

    def initUI(self):

        self.vertical_layout = QtGui.QVBoxLayout(self)

        self.scroll_area = QtGui.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area_widget_contents = QtGui.QWidget()
        self.scroll_area_widget_contents.setGeometry(
            QtCore.QRect(0, 0, 380, 280))

        self.horizontallayout = QtGui.QHBoxLayout(
            self.scroll_area_widget_contents)

        self.grid_layout = QtGui.QGridLayout()

        self.horizontallayout.addLayout(self.grid_layout)

        self.scroll_area.setWidget(self.scroll_area_widget_contents)

        self.text_lines = []

        n_problems = len(self.problems)

        for i in range(n_problems):
            self.text_lines.append(QtGui.QLabel(self.problems[i]))
            self.text_lines[i].setText(self.problems[i])
            self.grid_layout.addWidget(self.text_lines[i])

        self.vertical_layout.addWidget(self.scroll_area)

        quit_btn = QtGui.QPushButton("Quit")
        quit_btn.clicked.connect(self.quit_clicked)

        back_btn = QtGui.QPushButton("Back")
        back_btn.clicked.connect(self.accept)

        continue_btn = QtGui.QPushButton("Ignore and Continue")
        continue_btn.clicked.connect(self.accept_and_continue)

        #this works for fileprompt->stem_info
        #works for 'not all stems have raw'
        #does not work for raw info -> meta

        self.grid_layout.addWidget(back_btn, n_problems, 0)
        self.grid_layout.addWidget(continue_btn, n_problems, 1)
        self.grid_layout.addWidget(quit_btn, n_problems, 2)

        self.setGeometry(900, 400, 900, 400)
        self.setWindowTitle('Invalid Files')
        self.setWindowIcon(QtGui.QIcon('ICON_FILE'))
        self.center()

        self.show()

    def accept_and_continue(self):
        self.raw_dialog.accept()
        self.accept()

    def center(self):
        frame_gm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(
            QtGui.QApplication.desktop().cursor().pos())
        center_point = QtGui.QApplication.desktop().screenGeometry(
            screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def quit_clicked(self):
        QtCore.QCoreApplication.instance().quit()

class Metadata(QtGui.QDialog):

    def __init__(self, mix_path):
        super(Metadata, self).__init__()

        self.track_name = QtGui.QLineEdit()
        self.artist = QtGui.QLineEdit()
        self.album = QtGui.QLineEdit()
        self.composer = QtGui.QLineEdit()
        self.producer = QtGui.QLineEdit()
        self.website = QtGui.QLineEdit()
        self.mix_path = mix_path

        self.instrumental = QtGui.QComboBox()
        self.instrumental.addItems(["", "yes", "no"])

        self.excerpt = QtGui.QComboBox()
        self.excerpt.addItems(["", "yes", "no"])

        self.has_bleed = QtGui.QComboBox()
        self.has_bleed.addItems(["", "yes", "no"])

        self.genre = QtGui.QComboBox()
        self.genre.addItems(["", "Singer/Songwriter", "Rock", "Classical",
                             "Jazz", "Electronic/Fusion", "World/Folk",
                             "Musical Theatre", "Rap", "Pop"])

        self.track_origin = QtGui.QComboBox()
        self.track_origin.addItems(["", "Dolan Studio", "Weathervane Music",
                                    "Independent Artist", "Music Delta"])

        self.submit = QtGui.QPushButton('Submit')
        self.submit.clicked.connect(self.checkSubmit)

        self.ss_le = self.track_name.styleSheet()
        self.ss_cb = self.instrumental.styleSheet()
        self.complete = False

        self.initUI()

    def initUI(self):

        self.mix_play = QtGui.QPushButton()
        self.mix_play.setIcon(QtGui.QIcon(QtGui.QPixmap('play.png')))
        play_func = lambda: play_mix(self.mix_path)
        self.mix_play.clicked.connect(play_func)

        form = QtGui.QFormLayout()

        form.addRow("Preview mix:", self.mix_play) 
        form.addRow("Track Name*: ", self.track_name)
        form.addRow("Artist*: ", self.artist)
        form.addRow("Album*: ", self.album)
        form.addRow("Composer: ", self.composer)
        form.addRow("Producer: ", self.producer)
        form.addRow("Website: ", self.website)
        form.addRow("Instrumental*: ", self.instrumental)
        form.addRow("Excerpt*: ", self.excerpt)
        form.addRow("Has Bleed*: ", self.has_bleed)
        form.addRow("Genre*: ", self.genre)
        form.addRow("Origin*: ", self.track_origin)
        form.addRow(self.submit)

        self.setLayout(form)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Track Metadata')
        self.setWindowIcon(QtGui.QIcon('ICON_FILE'))
        self.center()

        self.show()

    def center(self):
        frame_gm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(
            QtGui.QApplication.desktop().cursor().pos())
        center_point = QtGui.QApplication.desktop().screenGeometry(
            screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def excerpt_go_back(self):
        self.complete = False

    def excerpt_continue(self):
        self.complete = True

    def checkSubmit(self):

        self.track_name.setStyleSheet(self.ss_le)
        self.artist.setStyleSheet(self.ss_le)
        self.instrumental.setStyleSheet(self.ss_cb)
        self.excerpt.setStyleSheet(self.ss_cb)
        self.has_bleed.setStyleSheet(self.ss_cb)
        self.genre.setStyleSheet(self.ss_cb)
        self.track_origin.setStyleSheet(self.ss_cb)

        self.complete = True

        # TODO: AFTER THESE ARE LEFT EMPTY AND BOX IS RED->format swithces and
        # you can't see options anymore
        if not self.track_name.displayText():
            self.track_name.setStyleSheet("border: 2px solid red;")
            self.complete = False
        if not self.artist.displayText():
            self.artist.setStyleSheet("border: 2px solid red;")
            self.complete = False
        if not self.instrumental.currentText():
            self.instrumental.setStyleSheet("border: 2px solid red;")
            self.complete = False

        if not self.excerpt.currentText():
            self.excerpt.setStyleSheet("border: 2px solid red;")
            self.complete = False
        if not self.has_bleed.currentText():
            self.has_bleed.setStyleSheet("border: 2px solid red;")
            self.complete = False
        if not self.genre.currentText():
            self.genre.setStyleSheet("border: 2px solid red;")
            self.complete = False
        if not self.track_origin.currentText():
            self.track_origin.setStyleSheet("border: 2px solid red;")
            self.complete = False

        ### Excerpt check ###
        dur = get_dur(self.mix_path) 
        if self.excerpt.currentText() == 'yes':
            if dur > 30.0:
                alert = QtGui.QMessageBox()
                alert.setText(
                    "You classified this file as an excerpt, but it's pretty "
                    "long. Are you sure it's an excerpt?"
                )
                
                no_button = QtGui.QPushButton('No') # go back
                no_button.clicked.connect(self.excerpt_go_back)
                yes_button = QtGui.QPushButton('Yes') # continue
                yes_button.clicked.connect(self.excerpt_continue)

                alert.addButton(no_button, 1)
                alert.addButton(yes_button, 1)

                alert.exec_()
            else:
                self.complete = True

        elif self.excerpt.currentText() == 'no':
            if dur < 60.0:
                alert = QtGui.QMessageBox()
                alert.setText(
                    "You did not classify this file as an excerpt, but it's "
                    "pretty short. Are you sure it's a full length song?"
                )
                
                no_button = QtGui.QPushButton('No') # go back
                no_button.clicked.connect(self.excerpt_go_back)
                yes_button = QtGui.QPushButton('Yes') # continue
                yes_button.clicked.connect(self.excerpt_continue)

                alert.addButton(no_button, 1)
                alert.addButton(yes_button, 1)
                alert.exec_()

        if self.complete:
            self.recordResponses()
            self.accept()

    def recordResponses(self):
        mdata = {}
        mdata["title"] = str(self.track_name.displayText())
        mdata["artist"] = str(self.artist.displayText())
        mdata["album"] = str(self.album.displayText())
        mdata["composer"] = str(self.composer.displayText())
        mdata["producer"] = str(self.producer.displayText())
        mdata["website"] = str(self.website.displayText())
        mdata["instrumental"] = str(self.instrumental.currentText())
        mdata["excerpt"] = str(self.excerpt.currentText())
        mdata["has_bleed"] = str(self.has_bleed.currentText())
        mdata["genre"] = str(self.genre.currentText())
        mdata["origin"] = str(self.track_origin.currentText())
        self.metadata = mdata


class Stems(QtGui.QDialog):
    def __init__(self, stem_dir):
        super(Stems, self).__init__()

        self.stem_dir = stem_dir
        self.stem_paths = glob.glob(os.path.join(self.stem_dir, '*.wav'))
        self.stem_names = [os.path.basename(f) for f in self.stem_paths]
        self.inst_dict = self.getInstMap()

        self.n_items = len(self.stem_names)

        self.stem_list = []
        self.stem_play = []
        self.stem_group = []
        self.stem_inst = []
        self.stem_melody = []
        self.stem_bass = []

        self.initUI()

    def initUI(self):

        for i in range(self.n_items):
            # Name of Stem #
            self.stem_list.append(QtGui.QLabel())
            self.stem_list[i].setText(self.stem_names[i])
            
            self.stem_play.append(QtGui.QPushButton())          
            play_function = lambda x: lambda: play_audio(self.stem_paths[x])
            self.stem_play[i].clicked.connect(play_function(i))
            self.stem_play[i].setIcon(
                QtGui.QIcon(QtGui.QPixmap('play.png')))

            # combo box for inst group #
            self.stem_group.append(QtGui.QComboBox())
            self.stem_group[i].addItem("")
            self.stem_group[i].addItems(sorted(self.inst_dict.keys()))
            self.stem_group[i].addItem("Main System")
            # combo box for instrument #
            self.stem_inst.append(QtGui.QComboBox())
            self.stem_inst[i].setEnabled(False)
            # connect group choice to insrument choices #
            self.stem_group[i].activated.connect(
                partial(self.loadInstCombobox, grp_cb=self.stem_group[i],
                        inst_cb=self.stem_inst[i]))
            # checkboxes #
            self.stem_melody.append(QtGui.QCheckBox())
            self.stem_bass.append(QtGui.QCheckBox())

        font = QtGui.QFont()
        font.setBold(True)

        file_header = QtGui.QLabel()
        file_header.setText("File Name")
        file_header.setFont(font)

        play_header = QtGui.QLabel()
        play_header.setText("Play")
        play_header.setFont(font)

        group_header = QtGui.QLabel()
        group_header.setText("Instrument Group")
        group_header.setFont(font)

        inst_header = QtGui.QLabel()
        inst_header.setText("Instrument")
        inst_header.setFont(font)

        melody_header = QtGui.QLabel()
        melody_header.setText("Contains Melody?")
        melody_header.setFont(font)

        bass_header = QtGui.QLabel()
        bass_header.setText("Contains Bass?")
        bass_header.setFont(font)

        self.submit = QtGui.QPushButton('Submit', self)
        self.submit.clicked.connect(self.checkSubmit)

        self.ss_cb = self.stem_inst[0].styleSheet()

        ##################################

        self.verticallayout = QtGui.QVBoxLayout(self)

        self.scroll_area = QtGui.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area_widget_contents = QtGui.QWidget()
        self.scroll_area_widget_contents.setGeometry(
            QtCore.QRect(0, 0, 380, 280))

        self.horizontallayout = QtGui.QHBoxLayout(
            self.scroll_area_widget_contents)

        form = QtGui.QGridLayout()

        self.horizontallayout.addLayout(form)

        self.scroll_area.setWidget(self.scroll_area_widget_contents)

        ##################################

        form.addWidget(file_header, 1, 0)
        form.addWidget(play_header, 1, 1) 
        form.addWidget(group_header, 1, 2)
        form.addWidget(inst_header, 1, 3)
        form.addWidget(melody_header, 1, 4)
        form.addWidget(bass_header, 1, 5)

        j = 2
        for i in range(self.n_items):
            form.addWidget(self.stem_list[i], j, 0)
            form.addWidget(self.stem_play[i], j, 1) 
            form.addWidget(self.stem_group[i], j, 2)
            form.addWidget(self.stem_inst[i], j, 3)
            form.addWidget(self.stem_melody[i], j, 4)
            form.addWidget(self.stem_bass[i], j, 5)
            j = j + 1

        self.verticallayout.addWidget(self.scroll_area)
        self.verticallayout.addWidget(self.submit)

        self.setGeometry(800, 300, 650, 250)
        self.setWindowTitle('Stem Info')
        self.setWindowIcon(QtGui.QIcon('ICON_FILE'))
        self.center()

        self.show()

    def center(self):
        frame_gm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(
            QtGui.QApplication.desktop().cursor().pos())
        center_point = QtGui.QApplication.desktop().screenGeometry(
            screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def getInstMap(self):
        f_handle = open(INST_TAXONOMY)
        taxonomy = yaml.load(f_handle)
        f_handle.close()
        inst_dict = {}

        for k in taxonomy.keys():
            inst_dict[k] = sorted(list(mu.get_dict_leaves(taxonomy[k])))
        return inst_dict

    def loadInstCombobox(self, grp_cb, inst_cb):

        group = str(grp_cb.currentText())
        if group in self.inst_dict.keys():
            inst_cb.clear()
            inst_cb.setEnabled(True)
            inst_cb.setStyleSheet(self.ss_cb)
            inst_cb.addItem("")
            inst_cb.addItems(self.inst_dict[group])
        elif group == "Main System":
            inst_cb.clear()
            inst_cb.setEnabled(True)
            inst_cb.setStyleSheet(self.ss_cb)
            inst_cb.addItem("Main System")
        else:
            inst_cb.clear()
            inst_cb.addItem("")
            inst_cb.setEnabled(False)


    def checkSubmit(self):

        for i in range(self.n_items):
            self.stem_inst[i].setStyleSheet(self.ss_cb)

        complete = True
        for i in range(self.n_items):
            if not self.stem_inst[i].currentText():
                self.stem_inst[i].setStyleSheet("border: 2px solid red;")
                complete = False

        if complete:
            self.recordResponses()
            self.accept()

    def recordResponses(self):
        stem_info = {}

        for i in range(self.n_items):
            k = self.stem_names[i]

            stem_info[k] = {}
            stem_info[k]['path'] = self.stem_paths[i]
            stem_info[k]['group'] = str(self.stem_group[i].currentText())
            stem_info[k]['inst'] = str(self.stem_inst[i].currentText())
            if self.stem_melody[i].isChecked():
                stem_info[k]['component'] = 'melody'
            elif self.stem_bass[i].isChecked():
                stem_info[k]['component'] = 'bass'
            else:
                stem_info[k]['component'] = ''

        self.mel_stems = [k for k in stem_info.keys()
                          if stem_info[k]['component'] == 'melody']
        self.n_stems = len(self.mel_stems)
        self.stem_info = stem_info


class Raw(QtGui.QDialog):
    def __init__(self, raw_dir, stem_info, stem_dir, mix_path):
        super(Raw, self).__init__()

        self.stem_dir = stem_dir
        self.mix_path = mix_path
        self.raw_dir = raw_dir
        self.stem_info = stem_info
        print stem_info

        self.stem_names = self.stem_info.keys()
        self.raw_paths = glob.glob(os.path.join(self.raw_dir, '*.wav'))
        self.stem_paths = glob.glob(os.path.join(self.stem_dir, '*.wav'))
        self.raw_names = [os.path.basename(f) for f in self.raw_paths]
        self.inst_dict = self.getInstMap()

        self.n_items = len(self.raw_names)

        self.raw_list = []
        self.raw_play = []
        self.raw_stem = []
        self.raw_group = []
        self.raw_inst = []
        self.initUI()


    def initUI(self):

        for i in range(self.n_items):
            # Name of Stem #
            self.raw_list.append(QtGui.QLabel())
            self.raw_list[i].setText(self.raw_names[i])

            # Play button #
            self.raw_play.append(QtGui.QPushButton())
            play_function = lambda x: lambda: play_audio(self.raw_paths[x])
            self.raw_play[i].clicked.connect(play_function(i))
            self.raw_play[i].setIcon(
                QtGui.QIcon(QtGui.QPixmap('play.png'))
            )

            # combo box for stem #
            self.raw_stem.append(QtGui.QComboBox())
            self.raw_stem[i].addItem("")
            self.raw_stem[i].addItems(sorted(self.stem_names))

            # combo box for inst group #
            self.raw_group.append(QtGui.QComboBox())
            self.raw_group[i].addItem("")
            self.raw_group[i].addItems(sorted(self.inst_dict.keys()))
            self.raw_group[i].addItem("Main System")

            # combo box for instrument #
            self.raw_inst.append(QtGui.QComboBox())
            self.raw_inst[i].setEnabled(False)

            # connect group choice to insrument choices #
            self.raw_group[i].activated.connect(
                partial(self.loadInstCombobox, grp_cb=self.raw_group[i],
                        inst_cb=self.raw_inst[i]))
            self.raw_stem[i].activated.connect(
                partial(self.loadStemInst, stem_cb=self.raw_stem[i],
                        group_cb=self.raw_group[i], inst_cb=self.raw_inst[i]))

        font = QtGui.QFont()
        font.setBold(True)

        file_header = QtGui.QLabel()
        file_header.setText("File Name")
        file_header.setFont(font)

        play_header = QtGui.QLabel()
        play_header.setText("Play")
        play_header.setFont(font)

        stem_header = QtGui.QLabel()
        stem_header.setText("Associated Stem")
        stem_header.setFont(font)

        group_header = QtGui.QLabel()
        group_header.setText("Instrument Group")
        group_header.setFont(font)

        inst_header = QtGui.QLabel()
        inst_header.setText("Instrument")
        inst_header.setFont(font)

        self.submit = QtGui.QPushButton('Submit', self)
        self.submit.clicked.connect(self.checkSubmit)

        self.ss_cb = self.raw_inst[0].styleSheet()

        ##########################

        self.verticallayout = QtGui.QVBoxLayout(self)

        self.scroll_area = QtGui.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area_widget_contents = QtGui.QWidget()
        self.scroll_area_widget_contents.setGeometry(
            QtCore.QRect(0, 0, 380, 280))

        self.horizontallayout = QtGui.QHBoxLayout(
            self.scroll_area_widget_contents)

        form = QtGui.QGridLayout()

        self.horizontallayout.addLayout(form)

        self.scroll_area.setWidget(self.scroll_area_widget_contents)

        ##########################

        form.addWidget(file_header, 1, 0)
        form.addWidget(play_header, 1, 1)
        form.addWidget(stem_header, 1, 2)
        form.addWidget(group_header, 1, 3)
        form.addWidget(inst_header, 1, 4)

        j = 2
        for i in range(self.n_items):
            form.addWidget(self.raw_list[i], j, 0)
            form.addWidget(self.raw_play[i], j, 1)
            form.addWidget(self.raw_stem[i], j, 2)
            form.addWidget(self.raw_group[i], j, 3)
            form.addWidget(self.raw_inst[i], j, 4)
            j = j + 1

        self.verticallayout.addWidget(self.scroll_area)
        self.verticallayout.addWidget(self.submit)

        self.setGeometry(900, 400, 750, 250)
        self.setWindowTitle('Raw Info')
        self.setWindowIcon(QtGui.QIcon('ICON_FILE'))
        self.center()

        self.show()

    def center(self):
        frame_gm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(
            QtGui.QApplication.desktop().cursor().pos())
        center_point = QtGui.QApplication.desktop().screenGeometry(
            screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def getInstMap(self):
        f_handle = open(INST_TAXONOMY)
        taxonomy = yaml.load(f_handle)
        f_handle.close()
        inst_dict = {}

        for k in taxonomy.keys():
            inst_dict[k] = sorted(list(mu.get_dict_leaves(taxonomy[k])))
        return inst_dict

    def loadStemInst(self, stem_cb, group_cb, inst_cb):
        stem_name = str(stem_cb.currentText())
        if stem_name in self.stem_info.keys():
            group_default = self.stem_info[stem_name]['group']
            inst_default = self.stem_info[stem_name]['inst']
            group_idx = group_cb.findText(group_default)
            group_cb.setCurrentIndex(group_idx)
            self.loadInstCombobox(group_cb, inst_cb)
            inst_idx = inst_cb.findText(inst_default)
            inst_cb.setCurrentIndex(inst_idx)

    def loadInstCombobox(self, grp_cb, inst_cb):

        group = str(grp_cb.currentText())
        if group in self.inst_dict.keys():
            inst_cb.clear()
            inst_cb.setEnabled(True)
            inst_cb.setStyleSheet(self.ss_cb)
            inst_cb.addItem("")
            inst_cb.addItems(self.inst_dict[group])
        elif group == "Main System":
            inst_cb.clear()
            inst_cb.setEnabled(True)
            inst_cb.setStyleSheet(self.ss_cb)
            inst_cb.addItem("Main System")
        else:
            inst_cb.clear()
            inst_cb.addItem("")
            inst_cb.setEnabled(False)

    def recordResponses(self):
        raw_info = {}
        for i in range(self.n_items):
            k = self.raw_names[i]

            raw_info[k] = {}
            raw_info[k]['path'] = self.raw_paths[i]
            raw_info[k]['inst'] = str(self.raw_inst[i].currentText())
            raw_info[k]['stem'] = str(self.raw_stem[i].currentText())
        self.raw_info = raw_info

    def checkSubmit(self):

        for i in range(self.n_items):
            self.raw_inst[i].setStyleSheet(self.ss_cb)
            self.raw_stem[i].setStyleSheet(self.ss_cb)

        complete = True
        stem_choices = []
        for i in range(self.n_items):
            stem_choices.append(str(self.raw_stem[i].currentText()))
            if not self.raw_inst[i].currentText():
                self.raw_inst[i].setStyleSheet("border: 2px solid red;")
                self.raw_stem[i].setStyleSheet("border: 2px solid red;")
                complete = False

        if set(self.stem_names) != set(stem_choices):
            not_all_stems = NotAllStems()
            if not not_all_stems.exec_():
                sys.exit(-1)
            complete = False

        if complete:
            self.recordResponses()

        file_status = check_multitrack(
            self.raw_paths, self.stem_paths, self.mix_path, self.raw_info
        )
        problems = create_problems(file_status)

        if len(problems) > 0:
            invalid_dialog = InvalidFiles(problems, self)
            if not invalid_dialog.exec_():
                sys.exit(-1)
        else:
            self.accept()


class MelRank(QtGui.QDialog):
    def __init__(self, stem_info):
        super(MelRank, self).__init__()
        self.mel_stems = [k for k in stem_info.keys()
                          if stem_info[k]['component'] == 'melody']
        self.n_stems = len(self.mel_stems)
        print 'n stems'
        print self.n_stems
        print 'mel stems'
        print self.mel_stems
        self.ranking = []

        self.initUI()

    def initUI(self):
        self.verticallayout = QtGui.QVBoxLayout(self)

        self.scroll_area = QtGui.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area_widget_contents = QtGui.QWidget()
        self.scroll_area_widget_contents.setGeometry(
            QtCore.QRect(0, 0, 380, 280))

        self.horizontallayout = QtGui.QHBoxLayout(
            self.scroll_area_widget_contents)

        form = QtGui.QGridLayout()
        self.horizontallayout.addLayout(form)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)

        self.rows = [QtGui.QButtonGroup(self.scroll_area_widget_contents)
                     for i in range(self.n_stems)]
        buttons = [
            [QtGui.QRadioButton("%s" % (i + 1)) for i in range(self.n_stems)]
            for j in range(self.n_stems)
        ]
        stem_labels = []
        for i, item in enumerate(buttons):
            stem_labels.append(QtGui.QLabel())
            stem_labels[i].setText(self.mel_stems[i])
            form.addWidget(stem_labels[i], i + 1, 0)
            for j, button in enumerate(item):
                self.rows[i].addButton(button)
                form.addWidget(button, i + 1, j + 1)
                if j == 0:
                    button.setChecked(True)

        self.submit = QtGui.QPushButton('Submit', self)
        self.submit.clicked.connect(self.checkSubmit)

        self.verticallayout.addWidget(self.scroll_area)
        self.verticallayout.addWidget(self.submit)

        self.setGeometry(800, 300, 650, 250)
        self.setWindowTitle('Melody Ranking')
        self.setWindowIcon(QtGui.QIcon('ICON_FILE'))
        self.center()

        # assign the widget to the main window
        self.show()

    def center(self):
        frame_gm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(
            QtGui.QApplication.desktop().cursor().pos()
        )
        center_point = QtGui.QApplication.desktop().screenGeometry(
            screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def checkSubmit(self):
        self.ranking = [
            [self.mel_stems[i], self.rows[i].checkedButton().text()]
            for i in range(self.n_stems)
        ]
        ranks = [val[1] for val in self.ranking]
        complete = True
        if len(set(ranks)) < len(ranks):
            complete = False

        if complete:
            self.accept()


class NotAllStems(QtGui.QDialog):
    def __init__(self):
        super(NotAllStems, self).__init__()
        self.initUI()

    def initUI(self):

        self.vertical_layout = QtGui.QVBoxLayout(self)

        message = QtGui.QLabel("Not all stems have raw files.")
        self.vertical_layout.addWidget(message)

        back_btn = QtGui.QPushButton("Back")
        back_btn.clicked.connect(self.accept)
        self.vertical_layout.addWidget(back_btn)

        self.setLayout(self.vertical_layout)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Error')
        self.setWindowIcon(QtGui.QIcon('ICON_FILE'))
        self.center()

        self.show()

    def center(self):
        frame_gm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(
            QtGui.QApplication.desktop().cursor().pos())
        center_point = QtGui.QApplication.desktop().screenGeometry(
            screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())


def play_audio(file_path):
    print file_path
    tfm = sox.Transformer()
    tfm.norm(db_level=0.0)
    tfm.silence()
    tfm.trim(0, 5)
    tfm.fade(fade_in_len=0.5, fade_out_len=0.5)
    tfm.preview(file_path)


def play_mix(file_path):
    print file_path
    tfm = sox.Transformer()
    tfm.norm(db_level=0.0)
    tfm.silence()
    tfm.trim(0, 10)
    tfm.fade(fade_in_len=0.5, fade_out_len=0.5)
    tfm.preview(file_path)


def process_data(save_path, metadata, mix_path, stem_info, raw_info, ranking):

    NM = mu.NewMultitrack(save_path)

    NM.setArtist(metadata["artist"])
    NM.setTitle(metadata["title"])
    NM.setAlbum(metadata["album"])
    NM.setComposer(metadata["composer"])
    NM.setProducer(metadata["producer"])
    NM.setWebsite(metadata["website"])
    NM.setInstrumental(metadata["instrumental"])
    NM.setExcerpt(metadata["excerpt"])
    NM.setHasBleed(metadata["has_bleed"])
    NM.setGenre(metadata["genre"])
    NM.setOrigin(metadata["origin"])

    NM.fillMetadata()
    NM.makeFileStructure()

    NM.addMixFile(mix_path)

    stem_name_map = dict.fromkeys(stem_info.keys())
    for stem in stem_info:
        idx = NM.addStemFile(stem_info[stem]['path'], stem_info[stem]['inst'],
                             stem_info[stem]['component'])
        stem_name_map[stem] = idx

    NM.setRanking([[NM.stem_fchange_dict[r[0]], r[1]] for r in ranking])

    for raw in raw_info:
        stem_idx = stem_name_map[raw_info[raw]['stem']]
        NM.addRawFile(raw_info[raw]['path'], stem_idx,
                      raw_info[raw]['inst'])

    NM.writeMetadataFile()
    NM.writeRankingFile()

def main():

    app = QtGui.QApplication(sys.argv)

    file_prompt = FilePrompt()
    if not file_prompt.exec_():
        sys.exit(-1)

    st = Stems(file_prompt.stem_path)
    if not st.exec_():
        sys.exit(-1)

    if st.n_stems > 0:
        mr = MelRank(st.stem_info)
        ranking = mr.ranking
        if not mr.exec_():
            sys.exit(-1)
    else:
        ranking = []

    rw = Raw(
        file_prompt.raw_path, st.stem_info, 
        file_prompt.stem_path, file_prompt.mix_path
    )
    if not rw.exec_():
        sys.exit(-1)

    meta = Metadata(file_prompt.mix_path)
    if not meta.exec_():
        sys.exit(-1)

    save_path = file_prompt.save_path
    metadata = meta.metadata
    mix_path = file_prompt.mix_path
    stem_info = st.stem_info
    raw_info = rw.raw_info
    process_data(save_path, metadata, mix_path, stem_info, raw_info, ranking)

    mbox = QtGui.QMessageBox()
    mbox.setText("Processing complete. Press OK to Exit.")
    mbox.exec_()

    app.quit()
    sys.exit(-1)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
