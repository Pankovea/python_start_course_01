import bpy
from mathutils import Vector, Euler, Quaternion
from mathutils import Quaternion as Quat
#from math import degrees

PI = 3.1415926535
SIZE = (0.1, 0.1, 1)

def rad(r):
    return r * PI / 180

def clear_scene():
    '''Очистить сцену'''
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)


def generate_segment():
    '''Генерировать сегмент
    возвращает мэш'''
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, SIZE[2]/2 - SIZE[0]/2), scale=SIZE)
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=True)
    bpy.ops.object.modifier_add(type='BEVEL')
    bpy.context.object.modifiers["Фаска"].width = SIZE[0] * 0.9 / 2
    bpy.context.object.modifiers["Фаска"].segments = 6
    bpy.ops.object.shade_smooth()
    bpy.ops.object.modifier_apply(modifier="Фаска")
    mesh = bpy.context.selected_objects[0].data
    bpy.ops.object.delete(use_global=False)
    return mesh


def new_seg(
        mesh,
        sc = 1,
        coord = Vector((0,0,0)),
        rot = Quat((1.0, 0.0, 0.0, 0.0)),  # Euler((0,0,0), 'XYZ'),
        name = 'segment.001', 
        ):
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = coord
    obj.scale *= sc
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = rot
    return obj
    

def vetka(mesh,
        sc = 1,
        coord = Vector((0,0,0)),
        rot = Quat((1.0, 0.0, 0.0, 0.0)),  # Euler((0,0,0), 'XYZ'),
        ) -> None:
    new_seg(mesh, sc, coord + Vector((0, 0, 0  )), rot )
    cur_vec = Vector((0, 0, 0.9))
    cur_vec.rotate(rot)
    cur_vec += coord
    new_seg(mesh, sc, cur_vec, rot )

    cur_rot = rot.rotation_difference( Euler((rad(30), 0, 0), 'XYZ').to_quaternion() ).inverted()
    new_seg(mesh, sc, cur_vec, cur_rot )

    cur_rot = rot.rotation_difference( Euler((rad(30), 0, rad(120)), 'XYZ').to_quaternion() ).inverted()
    new_seg(mesh, sc, cur_vec, cur_rot )

    cur_rot = rot.rotation_difference( Euler((rad(30), 0, rad(240)), 'XYZ').to_quaternion() ).inverted()
    new_seg(mesh, sc, cur_vec, cur_rot )


#def fract_vetka(n, mesh, sc, coord: Vector, rot: Euler):
#    if n == 1:
#        vetka(segment_mesh, 1, Vector((0, 0, 0  )), Euler((0, 0, 0), 'XYZ'))
#        vetka(segment_mesh, 1, Vector((0, 0, 0.9)), Euler((0, 0, 0), 'XYZ'))
#        vetka(segment_mesh, 1, Vector((0, 0, 0.9)), Euler((rad(-30), 0, 0       ), 'XYZ'))
#        vetka(segment_mesh, 1, Vector((0, 0, 0.9)), Euler((rad(-30), 0, rad(120)), 'XYZ'))
#        vetka(segment_mesh, 1, Vector((0, 0, 0.9)), Euler((rad(-30), 0, rad(240)), 'XYZ'))
#    else:
#        fract_vetka(n-1)


clear_scene()
segment_mesh = generate_segment()
vetka(segment_mesh, 1, Vector((-1, 1, 0  )), Euler((rad(0), rad(45), 0), 'XYZ').to_quaternion() )
#vetka(segment_mesh)

#v0 = Vector((0,0,0))
#v1 = Vector((-1, -1, -1))
#v1.normalize()
#rot = v1.rotation_difference(v0).to_euler()
#obj.rotation_euler = rot