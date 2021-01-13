# pyopenlayersmaplib
A python lib to draw points, paths, circle and road on a OSM map

``` Python
from pyolmapslib import pyolmaps

# create map object giving lat, lon, zoom to center map preview
mymap = pyolmaps.maps(41.885166, 12.519041, 17)

# Draw points
pointarray = [[41.883399, 12.520617, '000000', 'punto1'], [41.883939, 12.520829, '0000FF', 'punto2'], [41.885046, 12.521275, 'FF0000', 'punto3']]
mymap.addpointarray(pointarray)
# mymap.addsinglepoint(pointarray[0]) - use addsinglepoint instead of addpointarray for insert single point

# Draw paths
patharray = [[41.883399, 12.520617, 41.883939, 12.520829, '000000', 'seg1'], [41.883939, 12.520829, 41.885046, 12.521275, '0000FF', 'seg2']]
mymap.addpatharray(patharray)
# mymap.addsinglepath(patharray[0]) - use addsinglepath instead of addpatharray for insert single path

# Draw road using point and post-creating path between them
mymap.addroad(pointarray)

# Draw radcircle
mymap.addradcircle(circlecenter, radius)

# Create final html
mymap.draw('OLMAP.html')
```

## Example screenshot

### Draw point

![](https://github.com/andreamagnante/pyopenlayersmaplib/blob/main/repoimg/pointExample.png)

### Draw path

![](https://github.com/andreamagnante/pyopenlayersmaplib/blob/main/repoimg/pathblackExample.png)

![](https://github.com/andreamagnante/pyopenlayersmaplib/blob/main/repoimg/pathcolorExample.png)

### Draw road and radcircle

![](https://github.com/andreamagnante/pyopenlayersmaplib/blob/main/repoimg/roadExample.png)
