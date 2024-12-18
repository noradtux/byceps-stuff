#!/usr/bin/env python3

from xml.dom import minidom
import json
import re
import sys

rotate_re = re.compile(r'rotate\(([0-9\.]+)\)')

doc = minidom.parse(sys.argv[1])

layer = [g for g in doc.getElementsByTagName('g')
         if g.getAttribute('inkscape:label') == 'seats'][0]

area_title = layer.getElementsByTagName('title')[0].childNodes[0].data

groups = [group for group in layer.getElementsByTagName('g')]

for group in groups:
    group_title = group.getElementsByTagName('title')[0].childNodes[0].data

    seats = [rect for rect in group.getElementsByTagName('rect')]

    for seat in seats:
        transform = seat.getAttribute('transform')
        m = rotate_re.match(transform)
        rotation = float(m[1] if m else 0)

        print(json.dumps({
            'area_title': area_title,
            'label': seat.getAttribute('inkscape:label'),
            'category_title': group_title,
            'coord_x': int(float(seat.getAttribute('x'))),
            'coord_y': int(float(seat.getAttribute('y'))),
            'rotation': rotation,
            }))
