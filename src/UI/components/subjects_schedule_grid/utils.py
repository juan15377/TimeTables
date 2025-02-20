# functions in use
import numpy as np
import flet as ft 
def replace_element(vector, start, end, element):
    left_part = vector[0:start]
    right_part = vector[end+1:]

    return np.concatenate((left_part, [element], right_part))

def insert_elements(vector, pos, new_elements):
    vector = np.insert(vector, pos, new_elements)
    vector = np.delete(vector, len(new_elements) + pos)
    return vector

def get_absolute_position(vector, req_pos):
    c = 0
    position = 0
    for ele in vector:
        if c == req_pos:
            return position
        if type(ele) == ft.Container:  # it is a block on the board, if not a subject block
            c = c + 1
            position = position + 1
            if c == req_pos:
                return position
            continue
        size = ele.size
        c = c + size
        position = position + 1
        if c == req_pos:
            return position