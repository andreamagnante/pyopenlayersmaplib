
class maps:

    def __init__(self, centerLat, centerLng, zoom):
        self.center = (float(centerLat), float(centerLng))
        self.zoom = int(zoom)
        self.grids = None
        self.paths = []
        self.points = []
        self.roadpoints = []
        self.roadpaths = []
        self.radcirclecenter = []
        self.radcircleradius = []
        self.gridsetting = None

    def addsinglepoint(self, point):
        # point = [lat, lon, pointcolor, pointtitle]
        self.points.append(point)

    def addpointarray(self, pointarray):
        for x in pointarray:
            # x = [lat, lon, pointcolor, pointtitle]
            self.points.append(x)

    def addsinglepath(self, path):
        # path = [lat1, lon1, lat2, lon2, pathcolor, pathtitle]
        self.paths.append(path)

    def addpatharray(self, patharray):
        for x in patharray:
            # x = [lat1, lon1, lat2, lon2, pathcolor, pathtitle]
            self.paths.append(x)

    def addroad(self, roadpointsarray):
        for i, x in enumerate(roadpointsarray):
            # x = [lat, lon, pointcolor, pointtitle]
            self.roadpoints.append(x)
            if i > 0:
                # [lat1, lon1, lat2, lon2, pathcolor, pathtitle]
                self.roadpaths.append([roadpointsarray[i-1][0], roadpointsarray[i-1][1], x[0], x[1], x[2], "seg"])

    def addradcircle(self, radcirclecenter, radcircleradius):
        self.radcirclecenter.append(radcirclecenter)
        self.radcircleradius.append(radcircleradius)

    def draw(self, htmlfile):
        f = open(htmlfile, 'w')
        f.write('<!doctype html>\n')
        f.write('\t<head>\n')
        f.write('')
        f.write('\t\t<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/openlayers/4.6.4/ol.css" type="text/css">\n')
        f.write('\t\t<style>\n')
        f.write('\t\t\thtml, body {\n')
        f.write('\t\t\t\tmargin: 0;\n')
        f.write('\t\t\t\theight: 100%;\n')
        f.write('\t\t\t\tbody: 100%;\n')
        f.write('\t\t\t}\n')
        f.write('\t\t\t.map {\n')
        f.write('\t\t\t\theight: 100%;\n')
        f.write('\t\t\t\twidth: 100%;\n')
        f.write('\t\t\t}\n')
        f.write('\t\t</style>\n')
        f.write('\t\t<script src="https://cdnjs.cloudflare.com/ajax/libs/openlayers/4.6.4/ol.js"></script>\n')
        f.write('\t\t<title>OpenLayers Map</title>\n')
        f.write('\t</head>\n')
        f.write('\t<body>\n')
        f.write('\t\t<div id="map" class="map"></div>\n')
        f.write('\t\t<script type="text/javascript">\n')
        f.write('\t\tvar map = new ol.Map({\n')
        f.write('\t\t\ttarget: "map",\n')
        f.write('\t\t\tlayers: [\n')
        f.write('\t\t\t\tnew ol.layer.Tile({\n')
        f.write('\t\t\t\tsource: new ol.source.OSM()\n')
        f.write('\t\t\t})\n')
        f.write('\t\t\t],\n')
        f.write('\t\t\tview: new ol.View({\n')
        f.write('\t\t\t\tcenter: ol.proj.fromLonLat([12.519041, 41.885166]),\n')
        f.write('\t\t\t\tzoom: 18\n')
        f.write('\t\t\t})\n')
        f.write('\t\t});\n')
        f.write('\n')
        if len(self.points) > 0 or len(self.roadpoints) > 0:
            f.write('\t\tmap.on("click", function (evt) {\n')
            f.write('\t\t\tvar feature = map.forEachFeatureAtPixel(evt.pixel, function (feature) {\n')
            f.write('\t\t\t\treturn feature;\n')
            f.write('\t\t\t});\n')
            f.write('\t\t\tif (feature) {\n')
            f.write('\t\t\t\tif (feature.get("pointcoordinates") != null) {\n')
            f.write('\t\t\t\t\talert("pointcoordinates: " + feature.get("pointcoordinates") +"; pointtitle: "+ feature.get("pointtitle"));\n')
            f.write('\t\t\t\t} else {\n')
            f.write('\t\t\t\t\talert("roadpointcoordinates: " + feature.get("roadpointcoordinates") + "; roadpointtitle: " + feature.get("roadpointtitle"));\n')
            f.write('\t\t\t\t}\n')
            f.write('\t\t\t}\n')
            f.write('\t\t});\n')
            f.write('\n')
        if len(self.radcirclecenter) > 0:
            self.drawradcircle(f)
        if len(self.points) > 0:
            self.drawpoints(f)
        if len(self.paths) > 0:
            self.drawpaths(f)
        if len(self.roadpoints) > 0 and len(self.roadpaths) > 0:
            self.drawroad(f)
        f.write('\t\t</script>\n')
        f.write('\t</body>\n')
        f.write('</html>\n')

    def drawpoints(self, f):
        pointstring = 'var pointarray = ['
        for i, x in enumerate(self.points):
            if i != len(self.points)-1:
                pointstring = pointstring + '[' + str(x[0]) + ', ' + str(x[1]) + ', "' + x[2] + '", "' + x[3] + '"], '
            else:
                pointstring = pointstring + '[' + str(x[0]) + ', ' + str(x[1]) + ', "' + x[2] + '", "' + x[3] + '"]'
        pointstring = pointstring + '];'
        f.write('\t\t%s\n' % pointstring)
        f.write('\n')
        f.write('\t\tfor (i = 0; i < pointarray.length; i++){\n')
        f.write('\t\t\tif (pointarray[i][2] != "park"){\n')
        f.write('\t\t\t\tvar markerurl = "https://chart.apis.google.com/chart?cht=mm&chs=32x32&chco=FFFFFF,"+ pointarray[i][2] +",000000&ext=.png"\n')
        f.write('\t\t\t} else {\n')
        f.write('\t\t\t\tvar markerurl = "https://developers.google.com/maps/documentation/javascript/examples/full/images/parking_lot_maps.png"\n')
        f.write('\t\t\t}\n')
        f.write('\t\t\tvar pointstyle = new ol.style.Style({\n')
        f.write('\t\t\t\timage: new ol.style.Icon({\n')
        f.write('\t\t\t\t\tanchor: [0.5, 30],\n')
        f.write('\t\t\t\t\tanchorXUnits: "fraction",\n')
        f.write('\t\t\t\t\tanchorYUnits: "pixels",\n')
        f.write('\t\t\t\t\tsrc: markerurl,\n')
        f.write('\t\t\t\t}),\n')
        f.write('\t\t\t});\n')
        f.write('\n')
        f.write('\t\t\tvar pointlayer = new ol.layer.Vector({\n')
        f.write('\t\t\t\tsource: new ol.source.Vector({\n')
        f.write('\t\t\t\t\tfeatures: [\n')
        f.write('\t\t\t\t\t\tnew ol.Feature({\n')
        f.write('\t\t\t\t\t\t\tgeometry: new ol.geom.Point(ol.proj.fromLonLat([pointarray[i][1], pointarray[i][0]])),\n')
        f.write('\t\t\t\t\t\t\tpointtitle: pointarray[i][3],\n')
        f.write('\t\t\t\t\t\t\tpointcoordinates: [pointarray[i][0], pointarray[i][1]]\n')
        f.write('\t\t\t\t\t\t})\n')
        f.write('\t\t\t\t\t]\n')
        f.write('\t\t\t\t})\n')
        f.write('\t\t\t});\n')
        f.write('\n')
        f.write('\t\t\tpointlayer.setStyle(pointstyle)\n')
        f.write('\t\t\tmap.addLayer(pointlayer);\n')
        f.write('\t\t}\n')
        f.write('\n')

    def drawpaths(self, f):
        pathstring = 'var patharray = ['
        for i, x in enumerate(self.paths):
            if i != len(self.paths) - 1:
                pathstring = pathstring + '[' + str(x[0]) + ', ' + str(x[1]) + ', ' + str(x[2]) + ', ' + str(x[3]) + ', "' + x[4] + '", "' + x[5] + '"], '
            else:
                pathstring = pathstring + '[' + str(x[0]) + ', ' + str(x[1]) + ', ' + str(x[2]) + ', ' + str(x[3]) + ', "' + x[4] + '", "' + x[5] + '"]'
        pathstring = pathstring + '];'
        f.write('\t\t%s\n' % pathstring)
        f.write('\n')
        f.write('\t\tfor (i = 0; i < patharray.length; i++){\n')
        f.write('\t\t\tvar lonlat1 = ol.proj.fromLonLat([patharray[i][1], patharray[i][0]]);\n')
        f.write('\t\t\tvar lonlat2 = ol.proj.fromLonLat([patharray[i][3], patharray[i][2]]);\n')
        f.write('\t\t\tvar pathstyle = [\n')
        f.write('\t\t\t\tnew ol.style.Style({\n')
        f.write('\t\t\t\t\tstroke: new ol.style.Stroke({\n')
        f.write('\t\t\t\t\t\tcolor: "#"+patharray[i][4],\n')
        f.write('\t\t\t\t\t\twidth: 4\n')
        f.write('\t\t\t\t\t})\n')
        f.write('\t\t\t\t})\n')
        f.write('\t\t\t];\n')
        f.write('\n')
        f.write('\t\t\tvar pathlayer = new ol.layer.Vector({\n')
        f.write('\t\t\t\tsource: new ol.source.Vector({\n')
        f.write('\t\t\t\t\tfeatures: [new ol.Feature({\n')
        f.write('\t\t\t\t\t\tgeometry: new ol.geom.LineString([lonlat1, lonlat2]),\n')
        f.write('\t\t\t\t\t\tfirstcoordinates: [patharray[i][1], patharray[i][0]],\n')
        f.write('\t\t\t\t\t\tsecondcoordinates: [patharray[i][3], patharray[i][2]],\n')
        f.write('\t\t\t\t\t\tpathtitle: patharray[i][5],\n')
        f.write('\t\t\t\t\t})]\n')
        f.write('\t\t\t\t})\n')
        f.write('\t\t\t});\n')
        f.write('\n')
        f.write('\t\t\tpathlayer.setStyle(pathstyle);\n')
        f.write('\t\t\tmap.addLayer(pathlayer);\n')
        f.write('\t\t}\n')
        f.write('\n')

    def drawroad(self, f):
        roadpointstring = 'var roadpointarray = ['
        for i, x in enumerate(self.roadpoints):
            if i != len(self.roadpoints) - 1:
                roadpointstring = roadpointstring + '[' + str(x[0]) + ', ' + str(x[1]) + ', "' + x[2] + '", "' + x[3] + '"], '
            else:
                roadpointstring = roadpointstring + '[' + str(x[0]) + ', ' + str(x[1]) + ', "' + x[2] + '", "' + x[3] + '"]'
        roadpointstring = roadpointstring + '];'
        f.write('\t\t%s\n' % roadpointstring)
        f.write('\n')
        roadpathstring = 'var roadpatharray = ['
        for i, x in enumerate(self.roadpaths):
            if i != len(self.roadpaths) - 1:
                roadpathstring = roadpathstring + '[' + str(x[0]) + ', ' + str(x[1]) + ', ' + str(x[2]) + ', ' + str(
                    x[3]) + ', "' + x[4] + '", "' + x[5] + '"], '
            else:
                roadpathstring = roadpathstring + '[' + str(x[0]) + ', ' + str(x[1]) + ', ' + str(x[2]) + ', ' + str(
                    x[3]) + ', "' + x[4] + '", "' + x[5] + '"]'
        roadpathstring = roadpathstring + '];'
        f.write('\t\t%s\n' % roadpathstring)
        f.write('\n')
        f.write('\t\tvar count = 0\n')
        f.write('\t\taddpartialroad()\n')
        f.write('\t\tvar button = document.createElement("Button");\n')
        f.write('\t\tbutton.addEventListener(\'click\', addpartialroad)\n')
        f.write('\t\tbutton.innerHTML = "Add Next Marker"\n')
        f.write('\t\tbutton.style = "bottom:0;left:44%;position:absolute;font-size:40px";\n')
        f.write('\t\tdocument.body.appendChild(button);\n')
        f.write('\n')
        f.write('\t\tfunction sleep(ms){\n')
        f.write('\t\t\treturn new Promise( resolver => setTimeout(resolver, ms));\n')
        f.write('\t\t};\n')
        f.write('\n')
        f.write('\t\tasync function addpartialroad(){\n')
        f.write('\t\t\tcolor = roadpointarray[count][2]\n')
        f.write('\t\t\twhile (roadpointarray[count][2] == color){\n')
        f.write('\t\t\t\tif (roadpointarray[count][2] != "park"){\n')
        f.write('\t\t\t\t\tvar markerurl = "https://chart.apis.google.com/chart?cht=mm&chs=32x32&chco=FFFFFF,"+ roadpointarray[count][2] +",000000&ext=.png"\n')
        f.write('\t\t\t\t} else {\n')
        f.write('\t\t\t\t\tvar markerurl = "https://developers.google.com/maps/documentation/javascript/examples/full/images/parking_lot_maps.png"\n')
        f.write('\t\t\t\t}\n')
        f.write('\t\t\t\tvar roadpointstyle = new ol.style.Style({\n')
        f.write('\t\t\t\t\timage: new ol.style.Icon({\n')
        f.write('\t\t\t\t\t\tanchor: [0.5, 30],\n')
        f.write('\t\t\t\t\t\tanchorXUnits: "fraction",\n')
        f.write('\t\t\t\t\t\tanchorYUnits: "pixels",\n')
        f.write('\t\t\t\t\t\tsrc: markerurl,\n')
        f.write('\t\t\t\t\t}),\n')
        f.write('\t\t\t\t});\n')
        f.write('\n')
        f.write('\t\t\t\tvar roadpointlayer = new ol.layer.Vector({\n')
        f.write('\t\t\t\t\tsource: new ol.source.Vector({\n')
        f.write('\t\t\t\t\t\tfeatures: [\n')
        f.write('\t\t\t\t\t\t\tnew ol.Feature({\n')
        f.write('\t\t\t\t\t\t\t\tgeometry: new ol.geom.Point(ol.proj.fromLonLat([roadpointarray[count][1], roadpointarray[count][0]])),\n')
        f.write('\t\t\t\t\t\t\t\troadpointtitle: roadpointarray[count][3],\n')
        f.write('\t\t\t\t\t\t\t\troadpointcoordinates: [roadpointarray[count][0], roadpointarray[count][1]]\n')
        f.write('\t\t\t\t\t\t\t})\n')
        f.write('\t\t\t\t\t\t]\n')
        f.write('\t\t\t\t\t})\n')
        f.write('\t\t\t\t});\n')
        f.write('\n')
        f.write('\t\t\t\troadpointlayer.setStyle(roadpointstyle)\n')
        f.write('\t\t\t\tmap.addLayer(roadpointlayer);\n')
        f.write('\n')
        f.write('\t\t\t\tif (count > 0){\n')
        f.write('\t\t\t\t\tvar lonlat1 = ol.proj.fromLonLat([roadpatharray[count-1][1], roadpatharray[count-1][0]]);\n')
        f.write('\t\t\t\t\tvar lonlat2 = ol.proj.fromLonLat([roadpatharray[count-1][3], roadpatharray[count-1][2]]);\n')
        f.write('\t\t\t\t\tvar roadpathstyle = [\n')
        f.write('\t\t\t\t\t\tnew ol.style.Style({\n')
        f.write('\t\t\t\t\t\t\tstroke: new ol.style.Stroke({\n')
        f.write('\t\t\t\t\t\t\t\tcolor: "#"+roadpatharray[count-1][4],\n')
        f.write('\t\t\t\t\t\t\t\twidth: 4\n')
        f.write('\t\t\t\t\t\t\t})\n')
        f.write('\t\t\t\t\t\t})\n')
        f.write('\t\t\t\t\t];\n')
        f.write('\n')
        f.write('\t\t\t\t\tvar roadpathlayer = new ol.layer.Vector({\n')
        f.write('\t\t\t\t\t\tsource: new ol.source.Vector({\n')
        f.write('\t\t\t\t\t\t\tfeatures: [new ol.Feature({\n')
        f.write('\t\t\t\t\t\t\t\tgeometry: new ol.geom.LineString([lonlat1, lonlat2]),\n')
        f.write('\t\t\t\t\t\t\t\tfirstcoordinates: [roadpatharray[count-1][1], roadpatharray[count-1][0]],\n')
        f.write('\t\t\t\t\t\t\t\tsecondcoordinates: [roadpatharray[count-1][3], roadpatharray[count-1][2]],\n')
        f.write('\t\t\t\t\t\t\t\troadpathtitle: roadpatharray[count-1][5],\n')
        f.write('\t\t\t\t\t\t\t})]\n')
        f.write('\t\t\t\t\t\t})\n')
        f.write('\t\t\t\t\t});\n')
        f.write('\n')
        f.write('\t\t\t\t\troadpathlayer.setStyle(roadpathstyle);\n')
        f.write('\t\t\t\t\tmap.addLayer(roadpathlayer);\n')
        f.write('\t\t\t\t}\n')
        f.write('\t\t\t\tcount = count+1\n')
        f.write('\t\t\t\tawait sleep(50)\n')
        f.write('\t\t\t}\n')
        f.write('\t\t}\n')

    def drawradcircle(self, f):
        f.write('\t\tradcirclestyle = new ol.style.Style({\n')
        f.write('\t\t\ttstroke: new ol.style.Stroke({\n')
        f.write('\t\t\t\tcolor: "blue",\n')
        f.write('\t\t\t\twidth: 1\n')
        f.write('\t\t\t}),\n')
        f.write('\t\t\tfill: new ol.style.Fill({\n')
        f.write('\t\t\t\tcolor: "rgba(0, 0, 255, 0.1)"\n')
        f.write('\t\t\t})\n')
        f.write('\t\t})\n')
        f.write('\n')
        f.write('\t\tvar radcirclecenter = ol.proj.fromLonLat([%s, %s]);\n' % (str(self.radcirclecenter[0][1]), str(self.radcirclecenter[0][0])))
        f.write('\t\tvar radcirclelayer = new ol.layer.Vector({\n')
        f.write('\t\t\tsource: new ol.source.Vector({\n')
        f.write('\t\t\t\tprojection: "EPSG:4326",\n')
        f.write('\t\t\t\tfeatures: [new ol.Feature(new ol.geom.Circle(radcirclecenter, %s))]\n' % str(self.radcircleradius[0]))
        f.write('\t\t\t}),\n')
        f.write('\t\t});\n')
        f.write('\n')
        f.write('\t\tradcirclelayer.setStyle(radcirclestyle)\n')
        f.write('\t\tmap.addLayer(radcirclelayer);\n')
        f.write('\n')