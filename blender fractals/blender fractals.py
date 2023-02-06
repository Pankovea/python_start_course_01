import bpy
from mathutils import Vector, Euler, Quaternion
from mathutils import Quaternion as Quat
from random import random
from bpy.types import Mesh, Object

PI = 3.1415926535
SIZE = (0.1, 0.1, 1)

def rad(r: float) -> float:
    'Перевод градусов в радианы'
    return r * PI / 180

def clear_scene() -> None:
    'Очищает сцену'
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)


def generate_segment() -> Mesh:
    '''Генерирует сегмент
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


def generate_parent(name='group.001', sc=1) -> Object:
    '''Генерирует родителя
       возвращает объект-пустышку'''
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD')
    parent = bpy.context.selected_objects[0]
    parent.name = name
    parent.empty_display_size = sc/5
    return parent


def new_seg(
        mesh: Mesh,
        sc: float = 1,
        pos: Vector = Vector((0,0,0)),
        rot: Euler = Euler((0,0,0)),
        name: str = 'segment.001', 
    ) -> Object:
    '''Создаёт объект на основе mesh
       и возвращает его'''
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = pos
    obj.scale *= sc
    obj.rotation_euler = rot
    return obj
    

def vetka(
        mesh: Mesh,
        sc: float = 1,
        pos: Vector = Vector((0,0,0)),
        rot: Euler = Euler((0,0,0)),
        n: int = 0,
        var: float = 0.3,
    ) -> Object:
    '''Рекурсивная функция.
       Создаёт ветку с глубиной рекурсии n'''
    if n == 0:
        # Базовый случай, просто сегмент
        obj = new_seg(mesh, sc, pos, rot)
        return obj
    else:
        # рекурентный случай
        parent = generate_parent('vetka.001', sc) # Объект пустышка - родитель
        
        # Ствол
        vetka (mesh, .5, n=n-1).parent = parent   # Создаём ствол и назначаем родителя
        # Ствол 2-ой сегмент - Верхушка
        cur_pos = Vector((0, 0, 0.45))            # Сдвиг вверх
        vetka (mesh, .5, cur_pos, n=n-1 ).parent = parent
        # 1 ветка
        var_rad = rad( 180*(random()*var - var/2)) # Случайный поворот ветки в радианах
        cur_rot = Euler(( rad(30) + var_rad/4, 0, var_rad ))   # по Х - на 30 градусов, по Z - случайно
        cur_pos = Vector((0, 0, 0.25))             # Начало ветки на 0,25 по Z
        vetka (mesh, .5, cur_pos, cur_rot, n=n-1 ).parent = parent  # Создать ветку размером 0.5
        # 2 ветка                                  всё аналогично предыдущей, только сдвиг не меняется
        var_rad = rad( 180*(random()*var - var/2) )
        cur_rot = Euler(( rad(30) + var_rad/4, 0, rad(120) + var_rad ))
        vetka (mesh, .5, cur_pos, cur_rot, n=n-1 ).parent = parent
        # 3 ветка
        var_rad = rad( 180*(random()*var - var/2) )
        cur_rot = Euler(( rad(30) + var_rad/4, 0, rad(240) + var_rad))
        vetka (mesh, .5, cur_pos, cur_rot, n=n-1 ).parent = parent
        # применить трансформации для роителя, а значит и для всех его потомков, то есть для всей ветки
        parent.scale *= sc
        parent.location = pos
        parent.rotation_euler = rot
        return parent


def elka(
        mesh: Mesh,
        sc: float = 1,
        pos: Vector = Vector((0,0,0)),
        rot: Euler = Euler((0,0,0)),
        n: int = 0,
        var: float = 0.3,
    ) -> Object:
    '''Создаёт ёлку с ветками с глубиной рекурсии n'''
    
    parent = generate_parent('tree.001', sc)
    # Ствол состоит из n+1 сегментов
    for i in range(n):
        sc_seg = 1/(n+0)
        pos_seg = Vector((0, 0, sc_seg*i ))
        new_seg(mesh, sc_seg*1.1, pos_seg ).parent = parent
    
    # 1 ветка
    var_rad = rad( 180*(random()*var - var/2) )    # Случайный поворот
    cur_rot = Euler(( rad(150) + var_rad/4, 0, var_rad ))      # Вветка направлена вниз 150 градусов
    cur_pos = Vector((0, 0, 0.85))                 # позиция роста 0.85
    vetka (mesh, 1, cur_pos, cur_rot, n=n ).parent = parent
    # 2 ветка
    var_rad = rad( 180*(random()*var - var/2) )
    cur_rot = Euler(( rad(150) + var_rad/4, 0,rad(120) + var_rad ))
    vetka (mesh, 1, cur_pos, cur_rot, n=n ).parent = parent
    # 3 ветка
    var_rad = rad( 180*(random()*var - var/2) )
    cur_rot = Euler(( rad(150) + var_rad/4, 0,rad(240) + var_rad))
    vetka (mesh, 1, cur_pos, cur_rot, n=n ).parent = parent
    # применить трансформации для роителя, а значит и для всех его потомков, то есть для всей ветки
    parent.scale *= sc
    parent.location = pos
    parent.rotation_euler = rot
    return parent
    
#######################################
#
#   Основная работа в сцене
#
#######################################

import time 
start = time.time()

clear_scene()                      # очистить сцену
segment_mesh = generate_segment()  # Создать основной сегмент
 
n = 4           # Высота ёлки. При n = 3 - 1,5 сек, при n = 4 - 64 сек
h = 0           # Используется для рассчёта координаты следующего n-1 уровня ёлки
r = -30         # Начальный поворот уровня. Далее для следующего уровня +30 градусов
# Следующий цикл создаёт снизу вверх сначала уровни с большими ветками с глубиной рекурсии n
# Высота сегмента равна n метров (минус нахлёст)
# поднимаясь вверх глубина рекурсии веток уменьшается на 1 
for i in range(n):                                  # i = 0, 1, ... n-1
    elka(segment_mesh, 
        n = n-i,                                    # n = n, n-1 ... 1
        pos = Vector((0, 0, h)),                    # h = 0, (n-1)*0.85, предыдущ значение + (n-2)*0.85
        rot = Euler((0, 0, rad( r := r + 30 ) )),   # Сразу проворачиваем на 30 градусов в радианах
        sc = n-i )                                  # высота сегмента n, n-1 ... 1
    h += (n-i) * .75   # 0.75 - это коэффициет нахлёста уровней друг на друга
print('Время выполнения:', round(time.time() - start, 2), 'секунд')