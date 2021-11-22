import maya.cmds as cmds
import maya.mel as mm
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import functools
import logging
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin  # for parent ui to maya

ABOUT_SCRIPT = "\n" \
               "Latest updates:                                     \n" \
               "19.11.2021    -added a second dyn constrraint       \n" \
               "31.05.2021    -added 'Add polygonal geometry' item  \n" \
               "31.05.2021    -added Change range menu              \n" \
               "26.02.2021    -added ability to scale               \n" \
               "24.02.2021    -added choice of solvers              \n" \
               "03.02.2021    -added attribute prefix to control    \n" \
               "                                                    \n" \
               "Created by Andrey Belyaev                           \n" \
               "andreikin@mail.ru"

HELP_LABEL = "Select a chain of bones (more than two joints) on the basis of which will be\n" \
             "created FK controllers  and a dynamic curve\n"

HELP_TEXT = "\n" \
            "1 Build the bone chain by placing the joints where the controllers should be.\n" \
            "2 Adjust their orientation - the controllers will be oriented in a similar way\n" \
            "3 Make sure the bones are out of the collision objects \n" \
            "4 The root joint must have a parent, to which the system will be attached later\n" \
            "5 Choose 'Create dynamics system'\n" \
            "\n" \
            "For normal scaling, create a scale constraint for the group with Fk controllers\n" \
            "\n" \
            "To create driver attribute on a switch - select the nucleus, then the switch and\n" \
            "press the button 'Connect nucleus'\n" \
            "\n" \
            "To create polygonal roup, specify the prefix, the number of bones and select\n" \
            "the curve, on the basis of which the geometry will be built."

logger = logging.getLogger(__name__)
logger.handlers = []
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s  line: %(lineno)s   - function  %(funcName)s() %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO) # DEBUG, INFO, WARNING, ERROR, CRITICAL

DEFAULT_PREFIX = "rope"
MAX_VERTEX_NUM = 50
DEFAULT_VERTEX_NUM = 4
MAX_JOINT_NUM = 50
DEFAULT_JOINT_NUM = 12
POINT_NUM_IN_DYN_CONSTRAINT = 2


class RopeRigSystem_UI(MayaQWidgetBaseMixin, QMainWindow):
    def __init__(self):
        super(RopeRigSystem_UI, self).__init__()
        self.setWindowTitle("Rope rigging system")
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.verticalLayout = QVBoxLayout(self.centralwidget)

        # menu_bar
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        menu = QMenu("Help")
        menu_bar.addMenu(menu)
        help_action = QAction("Help", self)
        menu.addAction(help_action)
        help_action.triggered.connect(functools.partial(self.text_dialog, "Help"))
        about_script_action = QAction("About script", self)
        menu.addAction(about_script_action)
        about_script_action.triggered.connect(functools.partial(self.text_dialog, "ABOUT_PROGRAM"))

        val_menu = QMenu("Change range")
        menu_bar.addMenu(val_menu)
        max_action = QAction("Set range 800", self)
        val_menu.addAction(max_action)
        max_action.triggered.connect(lambda: self.set_maximum_values(800))
        mid_action = QAction("Set range 400", self)
        val_menu.addAction(mid_action)
        mid_action.triggered.connect(lambda: self.set_maximum_values(400))
        min_action = QAction("Set range 50", self)
        val_menu.addAction(min_action)
        min_action.triggered.connect(lambda: self.set_maximum_values(50))

        misc_menu = QMenu("Misc")
        menu_bar.addMenu(misc_menu)
        add_skin_joints_action = QAction("Add polygonal geometry", self)
        misc_menu.addAction(add_skin_joints_action)
        add_skin_joints_action.triggered.connect(self.add_joint_on_curve)

        # text 
        self.help_label = QLabel(HELP_LABEL)
        self.verticalLayout.addWidget(self.help_label)

        # option_box 
        self.option_box = QGroupBox("Options:")
        self.option_box_layout = QVBoxLayout(self.option_box)
        self.form_layout = QFormLayout()

        # text line Prefix
        self.pfx_lineEdit = QLineEdit(DEFAULT_PREFIX)
        regexp = QRegExp('^([A-Za-z0-9_]+)$')
        validator = QRegExpValidator(regexp)
        self.pfx_lineEdit.setValidator(validator)
        label_prefix = QLabel("Prefix:")
        self.pfx_lineEdit.setClearButtonEnabled(True)
        self.pfx_lineEdit.setPlaceholderText("Type the prefix to create system")
        self.form_layout.addRow(label_prefix, self.pfx_lineEdit)

        # combobox
        self.solver_combobox = QComboBox()
        self.solver_combobox.addItem("New solver")
        self.getSolvers()
        label_connect = QLabel("Connect to:")
        self.form_layout.addRow(label_connect, self.solver_combobox)
        self.option_box_layout.addLayout(self.form_layout)

        # line
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.option_box_layout.addWidget(self.line)

        # slider controllers size
        self.controll_hLayout = QHBoxLayout()
        self.controll_label = QLabel("Controller size :")
        self.controll_label.setFixedSize(90, 20)
        self.controll_hLayout.addWidget(self.controll_label)
        self.controll_horizontal_slider = QSlider()
        self.controll_horizontal_slider.setRange(1, 50)
        self.controll_horizontal_slider.setSliderPosition(10)
        self.controll_horizontal_slider.setOrientation(Qt.Horizontal)
        self.controll_hLayout.addWidget(self.controll_horizontal_slider)
        self.controll_lineEdit = QLineEdit()
        self.controll_lineEdit.setMaximumSize(QSize(42, 20))
        self.controll_hLayout.addWidget(self.controll_lineEdit)
        self.controll_lineEdit.setText(str(1.0))
        self.controll_horizontal_slider.valueChanged.connect(self.valueHandler)
        self.option_box_layout.addLayout(self.controll_hLayout)

        # slider Points number
        self.curve_hLayout = QHBoxLayout()
        self.curve_label = QLabel("Points number :")
        self.curve_label.setFixedSize(90, 20)
        self.curve_hLayout.addWidget(self.curve_label)
        self.curve_horizontal_slider = QSlider()
        self.curve_horizontal_slider.setMinimum(1)
        self.curve_horizontal_slider.setMaximum(MAX_VERTEX_NUM)
        self.curve_horizontal_slider.setSliderPosition(DEFAULT_VERTEX_NUM)
        self.curve_horizontal_slider.setOrientation(Qt.Horizontal)
        self.curve_hLayout.addWidget(self.curve_horizontal_slider)
        self.curve_spin_box = QSpinBox()
        self.curve_spin_box.setMinimum(1)
        self.curve_spin_box.setMaximum(MAX_VERTEX_NUM)
        self.curve_spin_box.setValue(DEFAULT_VERTEX_NUM)
        self.curve_hLayout.addWidget(self.curve_spin_box)
        self.curve_horizontal_slider.valueChanged.connect(self.curve_spin_box.setValue)
        self.curve_spin_box.valueChanged.connect(self.curve_horizontal_slider.setValue)
        self.option_box_layout.addLayout(self.curve_hLayout)

        # slider Joints number
        self.horizontalLayout_2 = QHBoxLayout()
        self.joints_label = QLabel("Joints number :")
        self.joints_label.setFixedSize(90, 20)
        self.horizontalLayout_2.addWidget(self.joints_label)
        self.joints_horizontal_slider = QSlider()
        self.joints_horizontal_slider.setMinimum(3)
        self.joints_horizontal_slider.setMaximum(MAX_JOINT_NUM)
        self.joints_horizontal_slider.setSliderPosition(DEFAULT_JOINT_NUM)
        self.joints_horizontal_slider.setOrientation(Qt.Horizontal)
        self.horizontalLayout_2.addWidget(self.joints_horizontal_slider)
        self.joints_spin_box = QSpinBox()
        self.joints_spin_box.setObjectName(u"joints_spin_box")
        self.joints_spin_box.setMinimum(3)
        self.joints_spin_box.setMaximum(MAX_JOINT_NUM)
        self.joints_spin_box.setValue(DEFAULT_JOINT_NUM)
        self.horizontalLayout_2.addWidget(self.joints_spin_box)
        self.joints_horizontal_slider.valueChanged.connect(self.joints_spin_box.setValue)
        self.joints_spin_box.valueChanged.connect(self.joints_horizontal_slider.setValue)
        self.option_box_layout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.option_box)

        self.check_box_layout = QHBoxLayout()
        self.label_start = QLabel("Start constraint :")
        self.label_start.setFixedSize(110, 20)
        self.check_box_layout.addWidget(self.label_start)
        self.start_check_box = QCheckBox()
        self.start_check_box.setCheckState(Qt.Checked)
        self.start_check_box.setFixedSize(70, 20)
        self.check_box_layout.addWidget(self.start_check_box)
        self.label_end = QLabel("End constraint :")
        self.label_end.setFixedSize(110, 20)
        self.check_box_layout.addWidget(self.label_end)
        self.end_check_box = QCheckBox()
        self.end_check_box.setCheckState(Qt.Checked)
        self.check_box_layout.addWidget(self.end_check_box)
        self.option_box_layout.addLayout(self.check_box_layout)

        # buttons 
        self.buttons_layout = QHBoxLayout()
        self.connect_nucleus_button = QPushButton("Connect nucleus")
        self.buttons_layout.addWidget(self.connect_nucleus_button)
        self.connect_nucleus_button.clicked.connect(self.connect_nucleus)
        self.create_button = QPushButton("Create dynamics system")
        self.buttons_layout.addWidget(self.create_button)
        self.verticalLayout.addLayout(self.buttons_layout)
        self.create_button.clicked.connect(self.create_rig)

        logger.debug(" executed")

    def valueHandler(self, value):
        scaledValue = float(value) / 10
        self.controll_lineEdit.setText(str(scaledValue))

    def text_dialog(self, text_type):
        help_dialog = QMessageBox()
        help_dialog.setWindowFlags(Qt.WindowStaysOnTopHint)
        if text_type == "Help":
            help_dialog.setWindowTitle("Help window")
            help_dialog.setText(HELP_TEXT)
        else:
            help_dialog.setWindowTitle("About program")
            help_dialog.setText(ABOUT_SCRIPT)
        help_dialog.setStandardButtons(QMessageBox.Cancel)
        help_dialog.exec_()
        logger.debug(" executed")


class RopeRigSystemRig(RopeRigSystem_UI):
    def create_rig(self):
        logger.debug(" Rope rig system started ")
        self.get_data_from_ui()
        if self.get_objects_and_chek_it():
            self.rig_grp = cmds.group(empty=True, name=self.prefx + 'Rig_grp')
            self.fk_rigging()
            self.building_base_curve()
            self.building_dynamic_curve()
            self.fk_dynamics_mix_system()
            self.add_skin_joints()
            an_connectRigVis(self.rig_grp, [self.input_curve,
                                            self.hair_sys,
                                            self.dyn_curve_grp,
                                            self.follicle,
                                            self.loc, ])

            logger.info("Rope rigging successfully complete.")

    def set_maximum_values(self, val):
        self.curve_horizontal_slider.setRange(1, val)
        self.joints_horizontal_slider.setRange(3, val)
        self.curve_spin_box.setMaximum(val)
        self.joints_spin_box.setMaximum(val)

    def get_data_from_ui(self):
        self.prefx = self.pfx_lineEdit.text()
        if not self.prefx:
            logging.getLogger().warning("You did not enter a prefix, the default value will be used!")
            self.prefx = DEFAULT_PREFIX
        self.ctrl_size = float(self.controll_lineEdit.text()) * 0.9
        self.point_number = self.curve_horizontal_slider.value()
        self.joint_number = self.joints_horizontal_slider.value()

    def get_objects_and_chek_it(self):
        self.joints = cmds.ls(sl=True)
        if cmds.objExists(self.prefx + 'Rig_grp'):
            cmds.error("Scene already contains objects with this prefix, choose another ")
        if len(self.joints) < 3:
            logging.getLogger().error("Necessary to select at least three joints!")
            return False
        for jnt in self.joints:
            if not cmds.nodeType(jnt) == "joint":
                logging.getLogger().error("Necessary to select at least three joints!")
                return False
        # get an object to which the entire system will be bound by the constraint
        try:
            self.parent_object = cmds.listRelatives(self.joints[0], parent=True)[0]
        except TypeError:
            self.parent_object = None
            logging.getLogger().warning("No parent, so the system will not be attached!")
        return True

    def fk_rigging(self):
        self.controls = []
        self.fk_grp = cmds.group(empty=True, name=self.prefx + 'FK_grp')
        cmds.parent(self.fk_grp, self.rig_grp)
        if self.parent_object:
            cmds.parentConstraint(self.parent_object, self.fk_grp)
        for i, jnt in enumerate(self.joints[:-1]):
            ctrl = Controllers(self.prefx + str(i) + "_CT")
            ctrl.makeController(shapeType="fk", orient="X", pos=jnt, size=self.ctrl_size)
            ctrl.hideAttr(['sx', 'sy', 'sz', 'v'])
            self.controls.append(ctrl)
            if i == 0:
                cmds.parent(ctrl.oriGrp, self.fk_grp)
            else:
                cmds.parent(ctrl.oriGrp, self.controls[i - 1].name)
            cmds.parentConstraint(ctrl.name, jnt)
            # add attribute to determine whether the controller belongs to dynamic system
            cmds.addAttr(ctrl.name, longName='prefix', dt='string', keyable=False)
            cmds.setAttr(ctrl.name + ".prefix", self.prefx, type="string")

        if self.end_check_box.checkState():
            self.dyn_ctrl = Controllers(self.prefx + "End_ctrl")
            self.dyn_ctrl.makeController(shapeType="sphere", orient="X", pos=self.joints[-1], size=self.ctrl_size/2)
            self.dyn_ctrl.hideAttr(['sx', 'sy', 'sz', 'v'])
            cmds.parent(self.dyn_ctrl.oriGrp, self.controls[-1].name)
            cmds.parentConstraint(self.dyn_ctrl.name, self.joints[-1])
        logger.debug(" executed")

    def building_base_curve(self):
        point_position = []
        for jnt in self.joints:
            jnt_coordinates = cmds.xform(jnt, query=True, translation=True, worldSpace=True)
            point_position.append(jnt_coordinates)
        self.base_curve = cmds.curve(p=point_position, degree=2, name=self.prefx + 'FK_crv')
        skinCluster = cmds.skinCluster(self.joints, self.base_curve, toSelectedBones=True, normalizeWeights=True)[0]
        cmds.skinPercent(skinCluster, self.base_curve+'.cv['+str(self.point_number-2)+']', transformValue=[(self.joints[-1], 1.0)])
        cmds.rebuildCurve(self.base_curve,
                          rebuildType=0,
                          spans=self.point_number,
                          constructionHistory=True)
        cmds.parent(self.base_curve, self.rig_grp)
        logger.debug(" executed")

    def building_dynamic_curve(self):
        existing_solvers = cmds.ls(type="nucleus")
        self.input_curve = cmds.duplicate(name=self.prefx + 'Input_crv', inputConnections=True)[0]
        mm.eval('makeCurvesDynamic 2 { "0", "0", "1", "1", "0"};')
        crv_shape = cmds.listRelatives(self.input_curve, shapes=True)[1]
        # getting names of all dynamics objects and rename it
        self.follicle = cmds.listConnections(crv_shape + ".local")[0]
        self.follicle = cmds.rename(self.follicle, self.prefx + '_follicle')
        cmds.setAttr(self.follicle + ".pointLock", 0)
        fol_shape = cmds.listRelatives(self.follicle, shapes=True)[0]
        dyn_curve_shape = cmds.connectionInfo(fol_shape + ".outCurve", destinationFromSource=True)[0].split('.')[0]
        self.dyn_curve = cmds.listRelatives(dyn_curve_shape, parent=True)[0]
        self.hair_sys_shape = cmds.connectionInfo(fol_shape + ".outHair", destinationFromSource=True)[0].split('.')[0]
        self.hair_sys = cmds.listRelatives(self.hair_sys_shape, parent=True)[0]
        self.setup_mix_attribut()
        self.hair_sys = cmds.rename(self.hair_sys, self.prefx + '_hairSystem')
        self.dyn_curve_grp = cmds.listRelatives(self.dyn_curve, parent=True)[0]
        self.dyn_curve = cmds.rename(self.dyn_curve, self.prefx + 'Dynamics_crv')

        if self.start_check_box.checkState():
            cmds.select(self.dyn_curve + '.cv[0:{}]'.format(POINT_NUM_IN_DYN_CONSTRAINT))
            dynamicConstraintShape = mm.eval('createNConstraint transform 0;')[0]
            self.dyn_constraint = cmds.listRelatives(dynamicConstraintShape, parent=True)[0]
            cmds.parentConstraint(self.controls[0].name, self.dyn_constraint)
            cmds.parent(self.dyn_constraint, self.rig_grp)
            cmds.addAttr(self.controls[0].name, ln="constraint_enable", at="enum", en="off:on", keyable=True, dv=True)
            cmds.connectAttr(self.controls[0].name + ".constraint_enable", dynamicConstraintShape + ".enable", )
            an_connectRigVis(self.rig_grp, [self.dyn_constraint, ])

        if self.end_check_box.checkState():
            p_range = '.cv[{}:{}]'.format(self.point_number - POINT_NUM_IN_DYN_CONSTRAINT+2, self.point_number +2)
            cmds.select(self.dyn_curve + p_range)
            end_dyn_constraint_shape = mm.eval('createNConstraint transform 0;')[0]
            self.end_dyn_constraint = cmds.listRelatives(end_dyn_constraint_shape, parent=True)[0]
            cmds.parentConstraint(self.dyn_ctrl.name, self.end_dyn_constraint)
            cmds.parent(self.end_dyn_constraint, self.rig_grp)
            cmds.addAttr(self.dyn_ctrl.name, ln="constraint_enable", at="enum", en="off:on", keyable=True, dv=True)
            cmds.connectAttr(self.dyn_ctrl.name + ".constraint_enable", end_dyn_constraint_shape + ".enable", )
            an_connectRigVis(self.rig_grp, [self.end_dyn_constraint, ])
        cmds.parent(self.hair_sys, self.dyn_curve_grp, self.rig_grp)

        # handling solver
        combo_box_value = self.solver_combobox.currentText()
        if combo_box_value == "New solver":
            if existing_solvers:
                cmds.select(self.hair_sys)
                mm.eval('assignNSolver ""')
        else:
            cmds.select(self.hair_sys)
            mm.eval('assignNSolver "{}"'.format(combo_box_value))
        self.refresh_combo_box_list()
        logger.debug(" executed")

    def refresh_combo_box_list(self):
        self.solver_combobox.clear()
        self.solver_combobox.addItem("New solver")
        self.getSolvers()

    def getSolvers(self):
        solvers = cmds.ls(type="nucleus")
        for solver in solvers:
            self.solver_combobox.addItem(solver)

    def setup_mix_attribut(self):
        soft_suffix = "_soft"
        hard_suffix = "_hard"
        atributes = {"stretchResistance": (0, 200),
                     "compressionResistance": (0, 200),
                     "bendResistance": (0, 200),
                     "mass": (0, 10),
                     "drag": (0, 1),
                     "damp": (0, 10)}
        self.controls[0].addDevideAttr()
        driver_attr = self.controls[0].name
        cmds.addAttr(driver_attr, longName="stiffness", keyable=True, minValue=0, maxValue=1)
        for atrribut in atributes:
            default_val = cmds.getAttr(self.hair_sys_shape + "." + atrribut)
            cmds.addAttr(self.hair_sys,
                         longName=atrribut + soft_suffix,
                         keyable=True,
                         minValue=atributes[atrribut][0],
                         maxValue=atributes[atrribut][1],
                         defaultValue=default_val)
            cmds.addAttr(self.hair_sys,
                         longName=atrribut + hard_suffix,
                         keyable=True,
                         minValue=atributes[atrribut][0],
                         maxValue=atributes[atrribut][1],
                         defaultValue=default_val * 4)
            blend_node = cmds.createNode('blendTwoAttr', n=atrribut + 'Blend_nod')
            cmds.connectAttr(self.hair_sys + "." + atrribut + soft_suffix, blend_node + ".input[0]")
            cmds.connectAttr(self.hair_sys + "." + atrribut + hard_suffix, blend_node + ".input[1]")
            cmds.connectAttr(blend_node + ".output", self.hair_sys_shape + "." + atrribut)
            cmds.connectAttr(driver_attr + ".stiffness", blend_node + ".attributesBlender")
        logger.debug(" executed")

    def fk_dynamics_mix_system(self):
        cmds.addAttr(self.controls[0].name,
                     longName="fk_dyn_mix",
                     keyable=True,
                     defaultValue=1,
                     minValue=0,
                     maxValue=1)
        bldShape = cmds.blendShape(self.dyn_curve, self.base_curve,
                                   origin="world",
                                   name=self.prefx + 'blendShape')[0]
        cmds.connectAttr(self.controls[0].name + ".fk_dyn_mix", bldShape + "." + self.dyn_curve)
        logger.debug(" executed")

    def add_joint_on_curve(self):
        self.prefx = self.pfx_lineEdit.text()
        self.base_curve = cmds.ls(sl=True)
        self.joint_number = self.joints_horizontal_slider.value()
        self.loc, self.jointsNames, skin_jnt_grp = jntOnCurvNonSpline(self.base_curve, self.joint_number, self.prefx)

    def add_skin_joints(self):
        self.loc, self.jointsNames, skin_jnt_grp = jntOnCurvNonSpline(self.base_curve, self.joint_number, self.prefx)
        cmds.parent(skin_jnt_grp, self.rig_grp)
        cmds.parent(self.loc, self.controls[0].name)
        an_connectRigVis(self.rig_grp, self.jointsNames)
        logger.debug(" executed")
        for jnt in self.jointsNames:
            cmds.connectAttr(self.fk_grp + ".scale", jnt + ".scale")

    def connect_nucleus(self):
        nucleus, switch = "", ""
        try:
            nucleus, switch = cmds.ls(sl=True)
        except ValueError:
            cmds.error("Select nucleus, then switch  and click the 'connect' button ")

        if not cmds.objExists(switch + ".haer_dynamics"):
            cmds.addAttr(switch, ln="haer_dynamics", at="enum", en="off:on", keyable=True)
        cmds.connectAttr(switch + ".haer_dynamics", nucleus + ".enable")
        logger.debug(" executed")


class Controllers(object):
    def __init__(self, name=None):
        self.name = name
        self.conGrp = None
        self.oriGrp = None
        self.color = 17
        self.defColor = {'cntrIk': 20, 'cntrFk': 17, 'left': 18, 'right': 13, 'add': 20}

    def addDevideAttr(self, attrName='_'):
        while cmds.objExists(self.name + '. ' + attrName):
            attrName = attrName + '_'
        cmds.addAttr(self.name, ln=attrName, keyable=True)
        cmds.setAttr(self.name + '. ' + attrName, lock=True)

    def gropeCT(self):  # made ori and con groups and place controller to it whith zero transforms
        names = divideName(self.name)
        self.conGrp = cmds.group(em=True, n=names[0] + names[1] + '_con')
        self.oriGrp = cmds.group(self.conGrp, n=names[0] + names[1] + '_ori')
        cmds.delete(cmds.parentConstraint(self.name, self.oriGrp))
        cmds.parent(self.name, self.conGrp)
        return [self.name, self.conGrp, self.oriGrp]

    def shapePresets(self, ct_type):  ## points coordinates puts in tuple for several curves !!!!!!!!!

        if ct_type == 'sphere':
            return {'degree': 3, 'point':
                [[[0, 0.0, -0.475], [0, -0.12, -0.47], [0, -0.27, -0.39], [0, -0.43, -0.24], [0, -0.5, 0.03],
                  [0, -0.36, 0.36], [0, 0.0, 0.51], [0, 0.36, 0.36], [0, 0.5, 0.03], [0, 0.42, -0.23], [0, 0.28, -0.39],
                  [0, 0.11, -0.47], [0, 0.0, -0.47]],
                 [[0.0, 0.475, 0.0], [-0.12, 0.47, 0], [-0.27, 0.39, 0], [-0.43, 0.24, 0], [-0.5, -0.03, 0],
                  [-0.36, -0.36, 0], [0.0, -0.51, 0.0], [0.36, -0.36, 0],
                  [0.5, -0.03, 0], [0.42, 0.23, 0], [0.28, 0.39, 0], [0.11, 0.47, 0], [0.0, 0.47, 0.0]],
                 [[0.0, 0, -0.475], [-0.12, 0, -0.47], [-0.27, 0, -0.39],
                  [-0.43, 0, -0.24], [-0.5, 0, 0.03], [-0.36, 0, 0.36], [0.0, 0, 0.51], [0.36, 0.0, 0.36],
                  [0.5, 0, 0.03], [0.42, 0, -0.23], [0.28, 0, -0.39],
                  [0.11, 0, -0.47], [0.0, 0, -0.47]]]}

        elif ct_type == 'fk':
            return {'degree': 3, 'point': [
                [[0.353, 0, 0.853], [0.530, 0, 0.780], [0.707, 0, 0.707], [0.780, 0, 0.530], [0.926, 0, 0.176],
                 [1.0, 0, 0.0],
                 [0.926, 0, -0.17], [0.780, 0, -0.53], [0.707, 0, -0.70], [0.530, 0, -0.78], [0.176, 0.0, -0.92],
                 [0.0, 0.0, -0.99], [-0.17, 0.0, -0.92], [-0.53, 0, -0.78], [-0.70, 0, -0.70],
                 [-0.78, 0, -0.53], [-0.92, 0, -0.17], [-0.99, 0, 0.0], [-0.92, 0, 0.176], [-0.78, 0, 0.530],
                 [-0.70, 0, 0.707], [-0.53, 0, 0.780], [-0.17, 0.0, 0.926], [0.0, 0.0, 0.999],
                 [0.176, 0.0, 0.926], [0.353, 0, 0.853]]]}

        elif ct_type == 'circle':
            return {'degree': 3, 'point': [
                [[0, 0.0, 1.000], [-0.36, 0.0, 0.989], [-0.84, 0.0, 0.668], [-1.09, 0.0, -0.01], [-0.77, 0.0, -0.79],
                 [0, 0.0, -1.11],
                 [0.776, 0.0, -0.79], [1.098, 0.0, -0.01], [0.844, 0.0, 0.668], [0.354, 0.0, 0.992], [0, 0.0, 1.000]]]}


    def hideAttr(self, attrs):
        for attr in attrs:
            cmds.setAttr(self.name + "." + attr, lock=True, keyable=False)

    def showTransAttrs(self):
        for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']:
            cmds.setAttr(self.name + "." + attr, lock=False, keyable=True)

    def moveCt(self, coord):  # ofset controller (shape)
        claster = cmds.cluster(self.name)
        cmds.move(coord[0], coord[1], coord[2], claster)
        cmds.delete(self.name, ch=True)

    def renameCtShapes(self):
        pfx = divideName(self.name)[0] + divideName(self.name)[1]
        s_list = cmds.listRelatives(self.name, s=True)
        for sp in s_list:
            for i in xrange(1, 1000):
                num = '0' + str(i) if len(str(i)) == 1 else str(i)
                if not cmds.objExists(pfx + num + '_shape'):
                    cmds.rename(sp, pfx + num + '_shape')
                    break

    def makeController(self, shapeType, size=1.0, offset=[0, 0, 0], orient="Y", pos='', posType='parent'):
        ctrl = cmds.curve(n=self.name, d=self.shapePresets(shapeType)['degree'],
                          p=self.shapePresets(shapeType)['point'][0])  # Make first curve
        if len(self.shapePresets(shapeType)['point']) > 1:  # if the point list is array, built  more curves
            for pList in self.shapePresets(shapeType)['point'][1:]:
                crv = cmds.curve(d=self.shapePresets(shapeType)['degree'], p=pList)
                child = cmds.listRelatives(crv, c=True)[0]
                cmds.parent(child, ctrl, s=True, r=True)
                cmds.delete(crv)
        self.gropeCT()
        if type(orient) == list:
            self.rotateCt(orient)  ### orient
        else:
            if orient == 'Z': self.rotateCt([-90, 0, 0])
            if orient == 'X': self.rotateCt([-90, -90, 0])
        self.setCtSize(size)
        self.moveCt(offset)
        if not shapeType == 'axis': self.addColor(color=self.color)
        if pos: self.placeCT(pos, posType)
        self.renameCtShapes()
        return self

    def setCtSize(self, size=1):  # cet size of coordinates
        Len = max(cmds.getAttr(self.name + ".boundingBoxMaxX") - cmds.getAttr(self.name + ".boundingBoxMinX"),
                  cmds.getAttr(self.name + ".boundingBoxMaxY") - cmds.getAttr(self.name + ".boundingBoxMinY"),
                  cmds.getAttr(self.name + ".boundingBoxMaxZ") - cmds.getAttr(self.name + ".boundingBoxMinZ"))
        claster = cmds.cluster(self.name)
        cmds.move(0.0, 0.0, 0.0, claster[1] + '.scalePivot')
        cmds.scale(size / Len, size / Len, size / Len, claster[1], r=True)
        cmds.delete(self.name, ch=True)

    def addColor(self, switch=None, color='cntrFk'):  # add color atributes to switch, connect  it to controller
        shape = cmds.listRelatives(self.name, s=True)
        if switch:  # if switch specify
            for each in self.defColor.keys():
                if not mm.eval("attributeExists \"" + each + '_color' + "\"" + switch):
                    cmds.addAttr(switch, ln=each + '_color', dv=self.defColor[each], min=0, max=32, keyable=False)
            for eachShape in shape:
                cmds.setAttr(eachShape + ".overrideEnabled", 1)
                cmds.connectAttr(switch + '.' + color + '_color', eachShape + ".overrideColor", f=True)
        else:  # if switch not specify
            if type(color) is str:
                self.color = self.defColor[color]
            else:
                self.color = color
            for eachShape in shape:
                cmds.setAttr(eachShape + ".overrideEnabled", 1)
                cmds.setAttr(eachShape + ".overrideColor", self.color)

    def rotateCt(self, coord):  # ofset controller (shape)
        claster = cmds.cluster(self.name)
        cmds.xform(claster[1], os=True, piv=(0, 0, 0))
        cmds.rotate(coord[0], coord[1], coord[2], claster)
        cmds.delete(self.name, ch=True)


    def placeCT(self, target, tape="parent", aimAndAp=[]):
        """
        @param[in] tape    - you specify one of placment tapes: "parent", "point", "orient", "polyVector"
        """
        if tape == "parent":
            cmds.delete(cmds.parentConstraint(target, self.oriGrp))
        elif tape == "point":
            cmds.delete(cmds.pointConstraint(target, self.oriGrp))
        elif tape == "orient":
            cmds.delete(cmds.orientConstraint(target, self.oriGrp))
        else:  # place polyVector controller, target - root ik jnt (shoulder)
            tmpJnt = cmds.duplicate(target, rc=True)
            ikHandl = cmds.ikHandle(shf=False, sol="ikRPsolver", sj=tmpJnt[0], ee=tmpJnt[2])

            posStart = cmds.xform(tmpJnt[0], q=True, t=True, ws=True)
            pozEnd = cmds.xform(tmpJnt[2], q=True, t=True, ws=True)
            valPv = cmds.getAttr(ikHandl[0] + ".poleVector")[0]
            posIkDef = [posStart[0] + valPv[0], posStart[1] + valPv[1], posStart[2] + valPv[2]]
            pozMiddl = [(posStart[0] + pozEnd[0]) / 2, (posStart[1] + pozEnd[1]) / 2, (posStart[2] + pozEnd[2]) / 2]

            posIkDefJnt = cmds.joint(p=posIkDef, children=False)
            jntPV = cmds.joint(p=pozMiddl)
            jntPVEnd = cmds.joint(p=pozMiddl)

            cmds.aimConstraint(target, jntPV, aim=[1, 0, 0], u=[0, 0, 1], wut="object", wuo=posIkDefJnt)
            cmds.setAttr(jntPVEnd + '.translateZ', abs(cmds.getAttr(tmpJnt[1] + ".tx")))
            cmds.delete(cmds.pointConstraint(jntPVEnd, self.oriGrp), tmpJnt, posIkDefJnt)


def an_connectRigVis(ctrlObject, objList):
    if not cmds.objExists(ctrlObject + '.rigVis'):  cmds.addAttr(ctrlObject, ln="rigVis", at="enum", en="off:on",
                                                                 keyable=True)  # cmds.addAttr  (info['grp'][0],  ln='rigVis',  keyable=True, dv=0, min=0, max=5, at="enum", en="off:on")                           #if attr Exists - create it
    for each in objList:

        if not cmds.connectionInfo(each + ".v", id=True) and not cmds.objExists(each + '.rigVis'):
            cmds.connectAttr(ctrlObject + '.rigVis', each + ".v")
        if cmds.objExists(each + '.rigVis'):
            cmds.connectAttr(ctrlObject + '.rigVis', each + '.rigVis')


def jntOnCurvNonSpline(curve_name, jnt_num=10, pfx='', geo=True):
    pfx = curve_name + 'JntOnCurve' if not pfx else pfx
    curve_shape = cmds.listRelatives(curve_name, s=True)[0]
    jointsNames = range(jnt_num + 1)
    rigGrp = cmds.group(n=pfx + 'Joints_grp', em=True)
    jointsNames = range(jnt_num)
    curve_len = cmds.arclen(curve_name)

    cmds.select(cl=True, sym=True)
    for i, string in enumerate(range(jnt_num)):
        jointsNames[i] = cmds.joint(relative=True,
                                    name=pfx + str(i) + '_jnt',
                                    position=[curve_len / (jnt_num - 1), 0, 0])
    if geo:
        geo = cmds.polyCylinder(name=pfx + 'Skin_geo',
                                radius=curve_len / jnt_num / 8,
                                height=curve_len,
                                subdivisionsY=jnt_num - 1,
                                subdivisionsX=6,
                                axis=[1, 0, 0])[0]
        cmds.delete(cmds.pointConstraint(jointsNames[0], jointsNames[-1], geo))
        cmds.skinCluster(jointsNames, geo, tsb=True, normalizeWeights=True)
        cmds.parent(geo, rigGrp)

    for i, string in enumerate(range(jnt_num)):
        cmds.select(cl=True, sym=True)
        cmds.parent(jointsNames[i], rigGrp)
        point_on_curve_info = cmds.createNode('pointOnCurveInfo', n=pfx + str(i) + '_poci')
        cmds.setAttr(point_on_curve_info + ".turnOnPercentage", 1)
        cmds.setAttr(point_on_curve_info + ".parameter", 1.0 / (jnt_num - 1) * i)
        cmds.connectAttr(curve_shape + '.worldSpace[0]', point_on_curve_info + '.inputCurve')
        cmds.connectAttr(point_on_curve_info + '.position', jointsNames[i] + '.translate')
        if not i == 0:
            cmds.aimConstraint(jointsNames[i - 1], jointsNames[i],
                               aim=[-1, 0, 0],
                               upVector=[0, 0, 1],
                               worldUpVector=[0, 0, 1],
                               worldUpType='objectrotation',
                               worldUpObject=jointsNames[i - 1])
    loc = cmds.spaceLocator(name=pfx + 'Up_loc')[0]
    cmds.parent(loc, jointsNames[0])
    for attr in ['tx', 'ty', 'tz']:    cmds.setAttr(loc + '.' + attr, 0)
    cmds.setAttr(loc + '.tz', curve_len / (jnt_num - 1))
    cmds.parent(loc, w=True)
    cmds.aimConstraint(jointsNames[1], jointsNames[0],
                       aim=[1, 0, 0],
                       upVector=[0, 0, 1],
                       worldUpVector=[0, 0, 1],
                       worldUpType='object',
                       worldUpObject=loc)
    cmds.parent(loc, rigGrp)
    return loc, jointsNames, rigGrp


def divideName(name):
    pref = ''
    suff = ''
    for each in ['l_', 'r_', 'up_', 'dw_', 'fr_', 'bk_', 'mid_']:
        size = len(each)
        if each in name[:size]:
            pref = each
    ferstPart = name[len(pref):]

    for each in ['_CT', '_jnt', '_bind', '_grp', '_ori', '_con', '_geo']:
        size = len(each)
        if each in name[-size:]:
            suff = each
    name = ferstPart[:-len(suff)] if suff else ferstPart
    return pref, name, suff


def rope_rig_system():
    global dyn_win
    try:
        dyn_win.deleteLater()
    except NameError:
        pass
    dyn_win = RopeRigSystemRig()
    dyn_win.show()


rope_rig_system()

