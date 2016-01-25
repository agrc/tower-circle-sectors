'''
Script tool to create coverage polygons for radio towers.
'''
import arcpy, os, time

def createPointAngleRangePolygons(points, outputPolygons, azimuthField, rangeField, beamWidthField):
    """azimuth: angle central to the coverage polygon.
       range: radius of the coverage polygon. Must be in meters.
       beamwidth: full arc of coverage. It is centered on the azimuth.
       Output polygons will have the same spatial reference as the input point features"""
    pointFeatures = points
    azimuthField = azimuthField
    rangeField = rangeField
    beamWidthField = beamWidthField
    #Polygon feature class will created by the tool. 
    outputPolygonFeatures = outputPolygons
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
            #Create a point every 1 degree around the arc
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
    points = arcpy.GetParameterAsText(0)
    azimuthField = arcpy.GetParameterAsText(1)
    rangeField = arcpy.GetParameterAsText(2)
    beamWidthField = arcpy.GetParameterAsText(3)
    outputDirectory = arcpy.GetParameterAsText(4)
    uniqueString = time.strftime("%Y%m%d%H%M%S")
    outputPolygons = os.path.join(outputDirectory, "CircleSectors_" + uniqueString)
    arcpy.SetParameter(5, outputPolygons)
    
    arcpy.AddMessage("Version 1.0")
    createPointAngleRangePolygons(points, outputPolygons, azimuthField, rangeField, beamWidthField)
    arcpy.AddMessage("completed")
    