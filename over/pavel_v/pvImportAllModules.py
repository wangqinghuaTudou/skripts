import os
import sys
import maya.OpenMaya as om

# modules_path = 'D:/Work/settings/for_rigging/'

def pvImportAllModules(current_path):
    content_list = os.listdir(current_path)
    directories_list = [d for d in content_list if os.path.isdir(os.path.join(current_path, d))]
    files_list = [f for f in content_list if os.path.isfile(os.path.join(current_path, f))]
    if files_list:
        for f in files_list:
            if '.py' in f and not '.pyc' in f:
                try:
                    system_paths = list(sys.path)
                    sys.path.insert(0, current_path)
                    module = __import__(f.split('.')[0])
                    sys.path[:] = system_paths
                    globals().update(vars(module))
                except Exception, err:
                    om.MGlobal.displayWarning('Info: %s'%err)
    if directories_list:
        for d in directories_list:
            deep_path = os.path.join(current_path, d)
            pvImportAllModules(deep_path)
    om.MGlobal.displayInfo('Info: Modules from directory "%s" imported successfully.'%current_path)

# pvImportAllModules(modules_path)