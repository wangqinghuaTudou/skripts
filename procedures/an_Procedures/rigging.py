
class Rigging:

    def __init__(self, pfx):
        self.pfx = pfx
        self.parent = None
        self.grp = pfx + "rigging_grp"
        self.initial_setting = None  # position of object without rigging
        self.current_setting = None  # position and values of object with rigging

    def rig_visibility(self):
        pass

    def delete_rigging(self):
        pass

    def save_rigging_state(self):
        pass



