
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import functools
import maya.cmds as cmds
import logging
from an_classControllers import AnControllers  


ABOUT_SCRIPT = "\n"\
            "Latest updates:                \n"\
            "27.01.2021    -start writing   \n"\
            "                               \n"\
            "Created by Andrey Belyaev      \n"\
            "andreikin@mail.ru"

HELP_LABEL ="Select a chain of bones (more than two joints) on the basis of which will be\n" \
             "created FK controllers  and a dynamic curve"

HELP_TEXT = "\n" \
            "1 Build the bone chain by placing the joints where the controllers should be.\n" \
            "2 Adjust their orientation - the controllers will be oriented in a similar way\n" \
            "3 Make sure the bones are out of the collision objects \n" \
            "4 The root joint must have a parent, to which the system will be attached later\n" \
            "5 Choose 'Create dynanmics sistem'\n" \

MAX_VERTEX_NUM = 40
MAX_JOINT_NUM = 40


class HairStrand_UI(QMainWindow):
    def __init__(self):
        super(HairStrand_UI, self).__init__()
        # Window
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Hair strand rigging system")
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.__menu_bar()  # help and About script windows
        self.__libel()  # text on top
        self.__option_box()
        self.__buttons()

    def __menu_bar(self):
        menuBar = QMenuBar()
        self.setMenuBar(menuBar)
        menu = QMenu("Help")
        menuBar.addMenu(menu)

        help_action = QAction("Help", self)
        menu.addAction(help_action)
        help_action.triggered.connect(functools.partial(self.text_dialog, "Help"))

        about_script_action = QAction("About script", self)
        menu.addAction(about_script_action)
        about_script_action.triggered.connect(functools.partial(self.text_dialog, "ABOUT_PROGRAM"))

    def text_dialog(self, text_type):
        help_dialog = QMessageBox()
        if text_type == "Help":
            help_dialog.setWindowTitle("Help window")
            help_dialog.setText(HELP_TEXT)
        else:
            help_dialog.setWindowTitle("About program")
            help_dialog.setText(ABOUT_SCRIPT)
        help_dialog.setStandardButtons(QMessageBox.Cancel)
        help_dialog.exec_()

    def __libel(self):
        self.help_label = QLabel(HELP_LABEL)
        self.verticalLayout.addWidget(self.help_label)

    def __option_box(self):
        self.option_box = QGroupBox("Options:")
        self.option_box_layout = QVBoxLayout(self.option_box)
        # text line Prefix
        self.pfx_layout = QHBoxLayout()
        self.pfx_label = QLabel("Prefix:")
        self.pfx_layout.addWidget(self.pfx_label)
        self.pfx_lineEdit = QLineEdit(self.option_box)
        self.pfx_layout.addWidget(self.pfx_lineEdit)
        self.option_box_layout.addLayout(self.pfx_layout)
        # slider Points number
        self.curve_hLayout = QHBoxLayout()
        self.curve_label = QLabel("Points number :")
        self.curve_hLayout.addWidget(self.curve_label)
        self.curve_horizontal_slider = QSlider()
        self.curve_horizontal_slider.setMinimum(3)
        self.curve_horizontal_slider.setMaximum(MAX_VERTEX_NUM)
        self.curve_horizontal_slider.setValue(10)
        self.curve_horizontal_slider.setSliderPosition(10)
        self.curve_horizontal_slider.setOrientation(Qt.Horizontal)
        self.curve_hLayout.addWidget(self.curve_horizontal_slider)
        self.curve_spin_box = QSpinBox()
        self.curve_spin_box.setMinimum(3)
        self.curve_spin_box.setMaximum(MAX_VERTEX_NUM)
        self.curve_spin_box.setValue(10)
        self.curve_hLayout.addWidget(self.curve_spin_box)
        self.curve_horizontal_slider.valueChanged.connect(self.curve_spin_box.setValue)
        self.curve_spin_box.valueChanged.connect(self.curve_horizontal_slider.setValue)
        self.option_box_layout.addLayout(self.curve_hLayout)
        # slider Joints number
        self.horizontalLayout_2 = QHBoxLayout()
        self.joints_label = QLabel("Joints number :")
        self.horizontalLayout_2.addWidget(self.joints_label)
        self.joints_horizontal_slider = QSlider()
        self.joints_horizontal_slider.setMinimum(3)
        self.joints_horizontal_slider.setMaximum(MAX_JOINT_NUM)
        self.joints_horizontal_slider.setSliderPosition(10)
        self.joints_horizontal_slider.setOrientation(Qt.Horizontal)
        self.horizontalLayout_2.addWidget(self.joints_horizontal_slider)
        self.joints_spin_box = QSpinBox()
        self.joints_spin_box.setObjectName(u"joints_spin_box")
        self.joints_spin_box.setMinimum(3)
        self.joints_spin_box.setMaximum(MAX_JOINT_NUM)
        self.joints_spin_box.setValue(10)
        self.horizontalLayout_2.addWidget(self.joints_spin_box)
        self.joints_horizontal_slider.valueChanged.connect(self.joints_spin_box.setValue)
        self.joints_spin_box.valueChanged.connect(self.joints_horizontal_slider.setValue)
        self.option_box_layout.addLayout(self.horizontalLayout_2)

        self.verticalLayout.addWidget(self.option_box)

    def __buttons(self):
        self.buttons_layout = QHBoxLayout()
        self.delete_button = QPushButton("Delete dynanmics sistem")
        self.buttons_layout.addWidget(self.delete_button)
        self.delete_button.clicked.connect(self.delete_rig)
        self.create_button = QPushButton("Create dynanmics sistem")
        self.buttons_layout.addWidget(self.create_button)
        self.verticalLayout.addLayout(self.buttons_layout)
        self.create_button.clicked.connect(self.create_rig)

    def get_data_from_ui(self):
        self.prefx = self.pfx_lineEdit.text()
        self.point_number = self.curve_horizontal_slider.value()
        self.joint_number = self.joints_horizontal_slider.value()
        return self.prefx, self.point_number, self.joint_number


class HairStrandRig(HairStrand_UI):
    def __init__(self):
        super(HairStrandRig, self).__init__()
        
        
    def get_objects_and_chek_it(self):
        self.temp_joints = cmds.ls(sl=True)
        if len(self.temp_joints)<3:
            logging.getLogger().error("Necessary to select at least three joints")
            return False
        # get an object to which the whole system is attached by constraint
        try:
            self.parent_object = cmds.listRelatives(self.temp_joints[0], parent = True)[0]
        except TypeError:
            self.parent_object = None
            logging.getLogger().warning("No parent, so the system will not be attached!")
        return True
    
    
    def create_rig(self):
        self.get_data_from_ui()
        if self.get_objects_and_chek_it():
            self.rig_grp = cmds.group(empty = True, name = self.prefx+'Rig_grp')
            self.controllers_placement()
            self.curve = self.building_basic_curve()
            self.dynamic_curve = self.building_dynamic_curve()
     
    def controllers_placement(self):
        self.controls=[]
        self.fk_grp = cmds.group(empty = True, name = self.prefx+'FK_grp')
        cmds.parent(self.fk_grp, self.rig_grp)
        if self.parent_object:
            cmds.parentConstraint(self.parent_object, self.fk_grp) 
        for i, tmp_jnt in enumerate(self.temp_joints):
            ctrl = AnControllers(self.prefx+str(i)+"_CT")
            ctrl.makeController(shapeType= "fk", orient="X", pos=tmp_jnt )
            self.controls.append(ctrl)
            if i == 0:
                cmds.parent(ctrl.oriGrp, self.fk_grp) 
            else:
                cmds.parent(ctrl.oriGrp, self.controls[i-1].name) 
           
    def building_basic_curve(self):
        return None
        
    def building_dynamic_curve(self):
        return None
        
    def delete_rig(self):
        print ("delete_rig")
 
def hair_strand_rig():
    win = HairStrandRig()
    win.show()
  
hair_strand_rig() 
  
























  