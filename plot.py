#!/usr/bin/env python3

import sys, re
import matplotlib.pyplot as plt
from collections import defaultdict
import json
from iso2to3 import *

plt.box(False)

img = plt.imread('blank-world-map.png')

width = 2048*3
height = 1024*3

fig, ax = plt.subplots(figsize=(width/1000.0,height/1000.0), frameon=False)
ax.imshow(img, extent=(0, width, 0, height))

ax.set_axis_off()
ax.set_xlim(left=0, right=width)
ax.set_ylim(bottom=0, top=height)

def lon2x(lat):
    return width*((float(lat) + 180) % 360)/360
def lat2y(lon):
    return height*((90+float(lon)) / 180)

langs = {}
with open('mapdata.tsv') as fin:
    for line in fin:
        if '.' in line and '#' not in line:
            ls = line.strip().split('\t')
            langs[ls[0]] = (ls[1], ls[2])

points = []

valid_codes = []
#
#with open('versions.tsv') as fin:
##tab:blue	o	1.0	10	hun spa eng swe ces ita gle deu fra fin
#
#    for line in fin:
#        line = re.sub('\t\t*', '\t', line)
#        ls = line.split()
#        color = ls[0]
#        mark = ls[1]
#        codes = ls[4:]
#        ver = ls[2]
#        valid_codes = [x for x in codes if x in langs]
#        points.append(ax.scatter([lon2x(langs[x][0]) for x in valid_codes],
#                                 [lat2y(langs[x][1]) for x in valid_codes],
#                                 s=2,
#                                 c=color,
#                                 marker=mark))
##        plt.savefig('%s_map.png' % ver, dpi=1000)
#
#plt.savefig('map.png', dpi=1000)
#
for p in points:
    p.remove()

size_ranges = [
    (range(1, 5), 1),
    (range(5, 10), 2),
    (range(10, 50), 3),
    (range(50, 100), 4),
    (range(100, 500), 5),
    (range(500, 1000), 6),
    (range(1000, 100000000000000), 7),
]

size_colours = ['#462b8c', '#524994', '#60649c', '#6f7ea2', '#7f98a8', '#8fb3ac' ,'#a0cdb0', '#b2e8b2']
size_colours.reverse()

sizes = defaultdict(list)
#with open('languages-sizes.tsv') as fin:

cvlangs_json = json.loads(open('languages.json').read())

#   {
#      "id" : 75860,
#      "is_contributable" : 1,
#      "locale" : "tn",
#      "localizedPercentage" : 85,
#      "recordedHours" : 0,
#      "sentencesCount" : {
#         "currentCount" : 1324,
#         "targetSentenceCount" : 750
#      },
#      "speakersCount" : 0,
#      "validatedHours" : 0
#   },
#

codes = []
recorded_hours = {}

for cvlang in cvlangs_json:
    if cvlang['is_contributable'] != 1:
        continue
    locale = cvlang['locale']
    if locale not in langs:
       print('!!', locale, 'not found.')
       if locale in iso2to3 and iso2to3[locale] != '_':
           print('!!!', locale, '→', iso2to3[locale])
           locale = iso2to3[locale]
    codes.append(locale)
    s = cvlang['recordedHours']
    if locale not in recorded_hours:
        recorded_hours[locale] = cvlang['recordedHours']
    if s < 1:
        sizes[0].append(locale)
        continue
    for r, v in size_ranges:
        if s in r:
            sizes[v].append(locale)
            break

missing = []
for sz in sorted(sizes.keys()):
    cds = sizes[sz]
    valid_codes = [x for x in cds if x in langs]
    print(sz, '] codes:', cds)
    print(sz, '] valid:', valid_codes)
    for vc in valid_codes:
        print('  ', vc, recorded_hours[vc])
    for c in set(cds) - set(valid_codes):
       missing.append(c)
    ax.scatter([lon2x(langs[x][0]) for x in cds if x in valid_codes],
               [lat2y(langs[x][1]) for x in cds if x in valid_codes],
               #s=(1.5*sz+1),
               s=2,
               #c='gray',
               c=size_colours[sz],
               #c='#' + '%x' % (10) * 2 +  '%x' % (abs(sz-7)) * 2 + '%x' % (10) * 2,
               marker='o')
plt.savefig('size_map.png', dpi=1000)

print('Missing:', missing)
