import maya.cmds as cmds

def pvShaderFXrestoreTextures():
    cmds.setAttr('hardwareRenderingGlobals.textureMaxResolution', 514)
    cmds.evalDeferred("cmds.setAttr('hardwareRenderingGlobals.textureMaxResolution', 512)")
    shaderfx_list = cmds.ls(type='ShaderfxShader')
    for sfx in shaderfx_list:
        try:
            cmds.shaderfx(sfxnode=sfx, edit_bool=[1298, 'value', False])
            cmds.evalDeferred("cmds.shaderfx(sfxnode=sfx, edit_bool=[1298, 'value', True])")
        except Exception, err:
            print(err)

#pvShaderFXrestoreTextures()