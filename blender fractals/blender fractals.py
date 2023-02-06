import bpy
from mathutils import Vector, Euler, Quaternion
from mathutils import Quaternion as Quat
from random import random


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


def generate_parent(name='group.001', sc=1):
    '''Генерировать родителя
    возвращает объект'''
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD')
    parent = bpy.context.selected_objects[0]
    parent.name = name
    parent.empty_display_size = sc/5
    return parent


def new_seg(
        mesh,
        sc = 1,
        pos = Vector((0,0,0)),
        rot = Euler((0,0,0)),
        name = 'segment.001', 
        ):
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = pos
    obj.scale *= sc
    obj.rotation_euler = rot
    return obj
    

def vetka(mesh,
        sc = 1,
        pos = Vector((0,0,0)),
        rot = Euler((0,0,0)),
        n = 0,
        var = 0.3,
        ) -> None:
    if n == 0:
        obj = new_seg(mesh, sc, pos, rot)
        return obj
    else:
        parent = generate_parent('vetka.001', sc)
        var_rad = rad( 180*(random()*var - var/2) )
        
        # Ствол
        vetka (mesh, .5, n=n-1).parent = parent
        # Верхушка
        cur_pos = Vector((0, 0, 0.45))
        vetka (mesh, .5, cur_pos, n=n-1 ).parent = parent
        # 1 ветка
        var_rad = rad( 180*(random()*var - var/2) )
        cur_rot = Euler(( rad(30), 0, var_rad ))
        cur_pos = Vector((0, 0, 0.25))
        vetka (mesh, .5, cur_pos, cur_rot, n=n-1 ).parent = parent
        # 2 ветка
        var_rad = rad( 180*(random()*var - var/2) )
        cur_rot = Euler(( rad(30), 0, rad(120) + var_rad ))
        vetka (mesh, .5, cur_pos, cur_rot, n=n-1 ).parent = parent
        # 3 ветка
        var_rad = rad( 180*(random()*var - var/2) )
        cur_rot = Euler(( rad(30), 0, rad(240) + var_rad))
        vetka (mesh, .5, cur_pos, cur_rot, n=n-1 ).parent = parent
        # применить трансформации
        parent.scale *= sc
        parent.location = pos
        parent.rotation_euler = rot
        return parent


def elka(mesh,
        sc = 1,
        pos = Vector((0,0,0)),
        rot = Euler((0,0,0)),
        n = 0,
        var = 0.3,
        ) -> None:
    parent = generate_parent('tree.001', sc)
    var_rad = rad( 180*(random()*var - var/2) )
    # Ствол
    for i in range(n+1):
        new_seg(mesh, 1/(n+1), Vector((0, 0, (1/(n+1))*i )) ).parent = parent
    
    # 1 ветка
    var_rad = rad( 180*(random()*var - var/2) )
    cur_rot = Euler(( rad(150), 0, var_rad ))
    cur_pos = Vector((0, 0, 0.85))
    vetka (mesh, 1, cur_pos, cur_rot, n=n ).parent = parent
    # 2 ветка
    var_rad = rad( 180*(random()*var - var/2) )
    cur_rot = Euler(( rad(150), 0,rad(120) + var_rad ))
    vetka (mesh, 1, cur_pos, cur_rot, n=n ).parent = parent
    # 3 ветка
    var_rad = rad( 180*(random()*var - var/2) )
    cur_rot = Euler(( rad(150), 0,rad(240) + var_rad))
    vetka (mesh, 1, cur_pos, cur_rot, n=n ).parent = parent
    parent.scale *= sc
    parent.location = pos
    parent.rotation_euler = rot
    return parent
    

clear_scene()
segment_mesh = generate_segment()
 
n = 4
h = -n*0.86
r = 0
for i in range(n):
    elka(segment_mesh, n = n-i,
        pos = Vector((0, 0, h:=h+(n-i+1)*.65 )),
        rot = Euler((0, 0, rad(r:=r+30) )),
        sc = n-i )