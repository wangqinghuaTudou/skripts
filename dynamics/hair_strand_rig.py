
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



DEFOULT_PREFIX = "haersStrand"
MAX_VERTEX_NUM = 40
DEFOULT_VERTEX_NUM = 4
MAX_JOINT_NUM = 40
DEFOULT_JOINT_NUM = 12

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
        self.pfx_lineEdit = QLineEdit(DEFOULT_PREFIX)
        self.pfx_layout.addWidget(self.pfx_lineEdit)
        self.option_box_layout.addLayout(self.pfx_layout)
        # slider Points number
        self.curve_hLayout = QHBoxLayout()
        self.curve_label = QLabel("Points number :")
        self.curve_hLayout.addWidget(self.curve_label)
        self.curve_horizontal_slider = QSlider()
        self.curve_horizontal_slider.setMinimum(1)
        self.curve_horizontal_slider.setMaximum(MAX_VERTEX_NUM)
        #self.curve_horizontal_slider.setValue(DEFOULT_VERTEX_NUM)
        self.curve_horizontal_slider.setSliderPosition(DEFOULT_VERTEX_NUM)
        self.curve_horizontal_slider.setOrientation(Qt.Horizontal)
        self.curve_hLayout.addWidget(self.curve_horizontal_slider)
        self.curve_spin_box = QSpinBox()
        self.curve_spin_box.setMinimum(1)
        self.curve_spin_box.setMaximum(MAX_VERTEX_NUM)
        self.curve_spin_box.setValue(DEFOULT_VERTEX_NUM)
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
        self.joints_horizontal_slider.setSliderPosition(DEFOULT_JOINT_NUM)
        self.joints_horizontal_slider.setOrientation(Qt.Horizontal)
        self.horizontalLayout_2.addWidget(self.joints_horizontal_slider)
        self.joints_spin_box = QSpinBox()
        self.joints_spin_box.setObjectName(u"joints_spin_box")
        self.joints_spin_box.setMinimum(3)
        self.joints_spin_box.setMaximum(MAX_JOINT_NUM)
        self.joints_spin_box.setValue(DEFOULT_JOINT_NUM)
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




class HairStrandRig(HairStrand_UI):
    
    def create_rig(self):
        self.get_data_from_ui()
        if self.get_objects_and_chek_it():
            self.rig_grp = cmds.group(empty = True, name = self.prefx+'Rig_grp')
            self.fk_rigging()
            self.building_base_curve()
            self.building_dynamic_curve()
            
    def get_data_from_ui(self):
        self.prefx = self.pfx_lineEdit.text()
        if not self.prefx:
            logging.getLogger().warning("You did not enter a prefix, the default value will be used !")
            self.prefx = DEFOULT_PREFIX   
        self.point_number = self.curve_horizontal_slider.value()
        self.joint_number = self.joints_horizontal_slider.value()
  
    def get_objects_and_chek_it(self):
        self.ctrl_joints = cmds.ls(sl=True)
        if len(self.ctrl_joints)<3:
            logging.getLogger().error("Necessary to select at least three joints")
            return False
        # get an object to which the whole system is attached by constraint
        try:
            self.parent_object = cmds.listRelatives(self.ctrl_joints[0], parent = True)[0]
        except TypeError:
            self.parent_object = None
            logging.getLogger().warning("No parent, so the system will not be attached!")
        return True
    
    def fk_rigging(self):
        self.controls=[]
        self.fk_grp = cmds.group(empty = True, name = self.prefx+'FK_grp')
        cmds.parent(self.fk_grp, self.rig_grp)
        if self.parent_object:
            cmds.parentConstraint(self.parent_object, self.fk_grp)
        for i, jnt in enumerate(self.ctrl_joints[:-1]):
            ctrl = AnControllers(self.prefx+str(i)+"_CT")
            ctrl.makeController(shapeType= "fk", orient="X", pos=jnt )
            self.controls.append(ctrl)
            if i == 0:
                cmds.parent(ctrl.oriGrp, self.fk_grp) 
            else:
                cmds.parent(ctrl.oriGrp, self.controls[i-1].name) 
            cmds.parentConstraint(ctrl.name, jnt)
           
    def building_base_curve(self):
        point_position = []
        for jnt in self.ctrl_joints:
            jnt_coordinates = cmds.xform(jnt, query=True, translation=True, worldSpace=True)
            point_position.append(jnt_coordinates)
        self.base_curve = cmds.curve(p=point_position, degree=2, name=self.prefx+'FK_crv')
        
        skCluster = cmds.skinCluster(self.ctrl_joints, self.base_curve, toSelectedBones=True, normalizeWeights=True)[0] 
        cmds.rebuildCurve(self.base_curve, 
                            rebuildType=0, 
                            spans=self.point_number, 
                            constructionHistory=True)
        cmds.parent(self.base_curve, self.rig_grp)

    def building_dynamic_curve(self):
        self.input_curve = cmds.duplicate(name=self.prefx+'Input_crv', inputConnections=True)
        
        mm.eval('makeCurvesDynamic 2 { "0", "0", "1", "1", "0"};')
        crv_shape= cmds.listRelatives (self.input_curve, shapes=True)[1]
        print crv_shape
        folicle = cmds.listConnections (crv_shape+".local") [0]
        cmds.setAttr (folicle+".pointLock", 0)
        folShape = cmds.listRelatives (folicle, shapes=True)[0]
        dynCurveShape = cmds.connectionInfo (folShape+".outCurve", destinationFromSource=True)[0].split('.')[0]   
        self.dynCurve = cmds.listRelatives (dynCurveShape, parent=True)[0]		 
        self.hairSysShape = cmds.connectionInfo (folShape+".outHair", destinationFromSource=True)[0].split('.')[0] 
        hairSys = cmds.listRelatives (self.hairSysShape, parent=True)[0] 
        dynCurveGrp = cmds.listRelatives (self.dynCurve, parent=True)[0]
        self.dynCurve = cmds.rename (self.dynCurve,  self.prefx+'Dynamics_crv')
        cmds.parent(hairSys, dynCurveGrp, self.rig_grp)
        
        
        
        cmds.select (self.dynCurve+'.cv[0:2]')
        dyn_constraint = mm.eval('createNConstraint transform 0;')
        print dyn_constraint
        
        
    def delete_rig(self):
        print ("delete_rig")
 
def hair_strand_rig():
    win = HairStrandRig()
    win.show()
  
hair_strand_rig() 
  
























  