# ##### BEGIN GPL LICENSE BLOCK #####
#
#  JewelCraft jewelry design toolkit for Blender.
#  Copyright (C) 2015-2021  Mikhail Rachinskiy
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####


from bpy.types import Operator, PropertyGroup
from bpy.props import BoolProperty, FloatProperty, IntProperty, PointerProperty

from .. import var


class Dimensions(PropertyGroup):
    x: FloatProperty(name="Width", step=0.1, unit="LENGTH")
    y: FloatProperty(name="Length", step=0.1, unit="LENGTH")
    z1: FloatProperty(name="Top", step=0.1, unit="LENGTH")
    z2: FloatProperty(name="Bottom", step=0.1, unit="LENGTH")


def upd_coords_handle(self, context):
    self.girdle_dim.z1, self.table_z = self.table_z, self.girdle_dim.z1


def upd_coords_hole(self, context):
    self.hole_dim.z1, self.culet_z = self.culet_z, self.hole_dim.z1
    self.hole_dim.y, self.culet_size = self.culet_size, self.hole_dim.y


class OBJECT_OT_cutter_add(Operator):
    bl_label = "Add Cutter"
    bl_description = (
        "Create cutter for selected gems\n"
        "(Shortcut: hold Ctrl when using the tool to avoid properties reset)"
    )
    bl_idname = "object.jewelcraft_cutter_add"
    bl_options = {"REGISTER", "UNDO"}

    detalization: IntProperty(name="Detalization", default=32, min=12, soft_max=64, step=1)

    use_handle: BoolProperty(name="Handle", update=upd_coords_handle)
    handle_dim: PointerProperty(type=Dimensions)
    handle_shift: FloatProperty(name="Position Offset", step=0.1, unit="LENGTH")

    girdle_dim: PointerProperty(type=Dimensions)
    table_z: FloatProperty(name="Table", options={"HIDDEN"})

    use_hole: BoolProperty(name="Hole", update=upd_coords_hole)
    hole_dim: PointerProperty(type=Dimensions)
    hole_shift: FloatProperty(name="Position Offset", step=0.1, unit="LENGTH")
    culet_z: FloatProperty(name="Culet", options={"HIDDEN"})
    culet_size: FloatProperty(name="Length", options={"HIDDEN"})

    use_curve_seat: BoolProperty(name="Curve Seat")
    curve_seat_profile: FloatProperty(name="Profile", default=0.5, min=0.15, max=1.0, subtype="FACTOR")
    curve_seat_segments: IntProperty(name="Segments", default=15, min=2, soft_max=30, step=1)

    curve_profile_factor: FloatProperty(name="Factor", min=0.0, soft_max=1.0, step=1, subtype="FACTOR")
    curve_profile_segments: IntProperty(name="Segments", default=10, min=1, soft_max=30, step=1)

    bevel_corners_width: FloatProperty(name="Width", min=0.0, step=0.1, unit="LENGTH")
    bevel_corners_percent: FloatProperty(name="Width", min=0.0, max=50.0, step=1, subtype="PERCENTAGE")
    bevel_corners_segments: IntProperty(name="Segments", default=1, min=1, soft_max=30, step=1)
    bevel_corners_profile: FloatProperty(name="Profile", default=0.5, min=0.15, max=1.0, subtype="FACTOR")

    mul_1: FloatProperty(name="Factor 1", default=1.0, min=0.0, soft_max=2.0, subtype="FACTOR")
    mul_2: FloatProperty(name="Factor 2", default=1.0, min=0.0, soft_max=2.0, subtype="FACTOR")
    mul_3: FloatProperty(name="Factor 3", default=1.0, min=0.0, soft_max=2.0, subtype="FACTOR")

    def draw(self, context):
        from . import cutter_ui
        cutter_ui.draw(self, context)

    def execute(self, context):
        from ..lib import asset
        from . import cutter_mesh

        bm = cutter_mesh.get(self)
        asset.bm_to_scene(bm, name="Cutter", color=self.color)

        return {"FINISHED"}

    def invoke(self, context, event):
        from ..lib import asset
        from .cutter_presets import init_presets

        ob = context.object

        if not ob or not context.selected_objects:
            self.report({"ERROR"}, "At least one gem object must be selected")
            return {"CANCELLED"}

        asset.get_cut(self, ob)
        prefs = context.preferences.addons[var.ADDON_ID].preferences
        self.color = prefs.color_cutter

        if not event.ctrl:
            init_presets(self)

        if event.alt:
            self.use_hole = False

        wm = context.window_manager
        wm.invoke_props_popup(self, event)
        return self.execute(context)
