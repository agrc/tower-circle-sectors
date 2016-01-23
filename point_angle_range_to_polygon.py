'''
Created on Jan 22, 2016

@author: kwalker
'''
import arcpy
def createPointAngleRangePolygons():
    pointFeatures = r"C:\KW_Working\TEMP\Temp.gdb\point_angle"
    xField = ""
    yField = ""
    azimuthField = "azimuth"
    rangeField = "range"
    beamWidthField = "beamwidth"
    
    polygonFeatures = r"C:\KW_Working\TEMP\Temp.gdb\pgon_angle"
    pgon = []
    
    cursorFields = ["SHAPE@", azimuthField, rangeField, beamWidthField]
    
    with arcpy.da.SearchCursor(pointFeatures, cursorFields) as cursor:
        for row in cursor:
            startAngle
            point1 = row[0].pointFromAngleAndDistance(row[1], row[2])
            print point1.JSON
            point2 = row[0].pointFromAngleAndDistance((row[1] + row[3]) % 360.0, row[2])
            print point2.WKT
            pgon.append(
                arcpy.Polygon(
                    arcpy.Array([row[0].centroid, point1.centroid, point2.centroid]), 
                    row[0].spatialReference))
            print 
            
    arcpy.CopyFeatures_management(pgon, polygonFeatures)

def calculateRadiusPoints ():