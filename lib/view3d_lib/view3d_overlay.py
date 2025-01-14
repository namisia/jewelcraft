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


import bgl
import gpu
from gpu_extras.batch import batch_for_shader
from mathutils import Vector


def restore_gl() -> None:
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glDisable(bgl.GL_LINE_SMOOTH)
    bgl.glDisable(bgl.GL_DEPTH_TEST)
    bgl.glDepthMask(bgl.GL_TRUE)
    bgl.glLineWidth(1.0)


def draw_axis(self, context):
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glEnable(bgl.GL_LINE_SMOOTH)
    bgl.glLineWidth(self.axis_width)

    if not self.axis_in_front:
        bgl.glEnable(bgl.GL_DEPTH_TEST)

    shader = gpu.shader.from_builtin("3D_SMOOTH_COLOR")
    shader.bind()

    for mat in self.mats:
        axis_start = mat.translation
        axis_x_end = mat @ Vector((self.axis_size, 0.0, 0.0))
        axis_y_end = mat @ Vector((0.0, self.axis_size, 0.0))
        axis_z_end = mat @ Vector((0.0, 0.0, self.axis_size))

        colors = (
            (1.0, 0.25, 0.25, 1.0), (1.0, 0.5, 0.25, 1.0),
            (0.25, 1.0, 0.25, 1.0), (0.25, 0.85, 0.6, 1.0),
            (0.25, 0.25, 1.0, 1.0), (0.0, 0.7, 1.0, 1.0),
        )
        coords = (
            axis_start, axis_x_end,
            axis_start, axis_y_end,
            axis_start, axis_z_end,
        )
        indxs = ((0, 1), (2, 3), (4, 5))

        batch = batch_for_shader(shader, "LINES", {"pos": coords, "color": colors}, indices=indxs)
        batch.draw(shader)

    restore_gl()
