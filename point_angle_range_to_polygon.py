'''
Script tool to create coverage polygons for radio towers.
'''
import arcpy

def createPointAngleRangePolygons():
    """azimuth: angle central to the coverage polygon.
       range: radius of the coverage polygon. Must be in meters.
       beamwidth: full arc of coverage. It is centered on the azimuth.
       Output polygons will have the same spatial reference as the input point features"""
    pointFeatures = r".\Temp.gdb\point_angle"
    azimuthField = "azimuth"
    rangeField = "range"
    beamWidthField = "beamwidth"
    #Polygon feature class will created by the tool. 
    outputPolygonFeatures = r".\Temp.gdb\pgon_angle4"
    polygons = []
    
    cursorFields = ["SHAPE@", azimuthField, rangeField, beamWidthField]
    with arcpy.da.SearchCursor(pointFeatures, cursorFields) as cursor:
        for row in cursor:
            centerPoint = row[0]
            azimuth = row[1]
            rangeDist = row[2]
            beamWidth = row[3]
            
            startAngle = (azimuth + (360 - (beamWidth / 2.0))) % 360
            print startAngle
            radiusPoints = [centerPoint.centroid]
            for i in range(int(beamWidth) + 1):
                angle = (startAngle + i) % 360
                print angle
                radPoint = centerPoint.pointFromAngleAndDistance(angle, rangeDist)
                radiusPoints.append(radPoint.centroid)
                
            polygons.append(
                arcpy.Polygon(
                    arcpy.Array(radiusPoints), 
                    centerPoint.spatialReference))
            print 
            
    arcpy.CopyFeatures_management(polygons, outputPolygonFeatures)

if __name__ == "__main__":
    createPointAngleRangePolygons()
    