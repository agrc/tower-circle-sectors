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
    outputPolygonFeatures = outputPolygons
    polygons = []
    #Setup field list for point search cursor and polygon insert cursor    
    cursorFields = [f.name for f in arcpy.ListFields(pointFeatures)]
    cursorFields.remove('SHAPE')
    cursorFields.append("SHAPE@")
    polygonInsCursor = arcpy.da.InsertCursor(outputPolygonFeatures, cursorFields)
    with arcpy.da.SearchCursor(pointFeatures, cursorFields) as cursor:
        for row in cursor:
            centerPoint = row[len(cursorFields) - 1]
            azimuth = row[cursor.fields.index(azimuthField)]
            rangeDist = row[cursor.fields.index(rangeField)]
            beamWidth = row[cursor.fields.index(beamWidthField)]
            
            startAngle = (azimuth + (360 - (beamWidth / 2.0))) % 360
            radiusPoints = [centerPoint.centroid]
            #Create a point every 1 degree around the arc
            for i in range(int(beamWidth) + 1):
                angle = (startAngle + i) % 360
                radPoint = centerPoint.pointFromAngleAndDistance(angle, rangeDist)
                radiusPoints.append(radPoint.centroid)
            #Use point row as polygon insert row with new polygon geometery subsituted for point
            newRow = [f for f in row]
            newRow[len(newRow) - 1] = arcpy.Polygon(arcpy.Array(radiusPoints), centerPoint.spatialReference)   
            polygonInsCursor.insertRow(newRow)

    del polygonInsCursor 
            

if __name__ == "__main__":
    testing = True
    if testing:
        points = r".\data\Temp.gdb\point_angle"
        azimuthField = "azimuth"
        rangeField = "range"
        beamWidthField = "beamwidth"
        outputWorkspace = r".\data\Temp.gdb"
        uniqueString = time.strftime("%Y%m%d_%H%M%S")
        outputPolygons = "CircleSectors_" + uniqueString
        arcpy.SetParameter(5, outputPolygons) 
    else:
        points = arcpy.GetParameterAsText(0)
        azimuthField = arcpy.GetParameterAsText(1)
        rangeField = arcpy.GetParameterAsText(2)
        beamWidthField = arcpy.GetParameterAsText(3)
        outputWorkspace = arcpy.GetParameterAsText(4)
        uniqueString = time.strftime("%Y%m%d_%H%M%S")
        outputPolygons = "CircleSectors_" + uniqueString
        arcpy.SetParameter(5, outputPolygons)
    
    arcpy.AddMessage("Version 1.1")
    pointsSpatialRef = arcpy.Describe(points).spatialReference
    arcpy.CreateFeatureclass_management (outputWorkspace, 
                                         outputPolygons, 
                                         "POLYGON", 
                                         points,
                                         spatial_reference=pointsSpatialRef)
    createPointAngleRangePolygons(points, 
                                  os.path.join(outputWorkspace, outputPolygons),
                                  azimuthField, 
                                  rangeField, 
                                  beamWidthField)
    arcpy.AddMessage("completed")
    