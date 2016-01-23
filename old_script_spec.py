'''
Created on Jan 22, 2016

@author: kwalker
'''

#Import modules
import arcgisscripting, math, string, os, sys, fpformat, operator

try:

    #Create the object
    gp = arcgisscripting.create()
    gp.overwriteoutput = 1

    gp.addmessage("********************************************")
    gp.addmessage("* zzz Make Polygons From Angles And Points *")
    gp.addmessage("*           (Create Pie Segments)          *")
    gp.addmessage("********************************************\n")

    #Collect Azimuth, Radius and point parameters
    fc = string.replace(gp.getparameterastext(0),"\\","/")
    fields = gp.listfields(fc)
    descfc = gp.describe(fc)
    sr = descfc.spatialreference
    azi1fld = gp.getparameterastext(1)
    azi2fld = gp.getparameterastext(3)
    radius1fld = gp.getparameterastext(2)
    radius2fld = gp.getparameterastext(4)

    #Check for output featureclass
    outfc  = string.replace(fc, ".shp", "_polygon.shp")
    lstfc = string.split(fc, "/")
    for fd in lstfc:
        fn = fd
    #If existance
    if gp.exists(outfc):
        gp.addmessage("Deleting " + outfc)
        gp.delete_management(outfc)
    #folder name
    folder = string.replace(fc, "/" + fn, "")
    gp.refreshcatalog(folder)
    gp.workspace = folder
    #Create tehe feature class
    gp.addmessage("Creating a polygon featureclass " + outfc)
    sf = string.replace(outfc,folder + "/", "")
    gp.createfeatureclass_management(folder, sf, "POLYGON", fc, "SAME_AS_TEMPLATE", "SAME_AS_TEMPLATE", sr)
    gp.refreshcatalog(folder)

    #Open search and insert cursors
    n = 0
    insrecs = gp.insertcursor(outfc)
    recs = gp.searchcursor(fc)
    rec = recs.next()
    while rec:

        #Parameter values
        pt = rec.shape.getpart(0)
        azi1 = 360 - rec.getvalue(azi1fld) + 90
        azi1 = operator.mod(azi1, 360)
        radius1 = rec.getvalue(radius1fld) 
        azi2 = 360 - rec.getvalue(azi2fld) + 90
        azi2 = operator.mod(azi2, 360)
        radius2 = rec.getvalue(radius2fld)
        if azi2 < azi1:
            while azi2 < azi1:
                azi2 = azi2 + 360

        #Make a new polygon and add the first point
        newPolygon = gp.createobject("array")
        newPolygon.add (pt)

        #Second point
        if azi1 > 360:
            testAngle = operator.mod(azi1, 360)
        else:
            testAngle = azi1

        #Make point
        x = pt.x + (math.cos(math.radians(testAngle)) * radius1)
        y = pt.y + (math.sin(math.radians(testAngle)) * radius1)
        newPt = gp.createobject("point")
        newPt.x = x
        newPt.y = y
        newPolygon.add (newPt)
                
        #Increments
        e = 0
        incAngle = azi1 + 1
        while incAngle < azi2:
            e = e + 1
            incAngle = incAngle + 1

        #Get the rate of change
        dRadius = radius1 - radius2
        ratio = dRadius / e
        azi1 = azi1 + 1
        radius = radius1

        #Loop through each degree
        while azi1 < azi2:
            radius = radius + ratio
            if azi1 > 360:
                testAngle = operator.mod(azi1, 360)
            else:
                testAngle = azi1

            #Make pont                
            x = pt.x + (math.cos(math.radians(testAngle)) * radius)
            y = pt.y + (math.sin(math.radians(testAngle)) * radius)
            newPt = gp.createobject("point")
            newPt.x = x
            newPt.y = y
            newPolygon.add (newPt)
            azi1 = azi1 + 1

        #Second to last point
        #Get a test angle
        if azi2 > 360:
            testAngle = operator.mod(azi2, 360)
        else:
            testAngle = azi2

        #Make point            
        x = pt.x + (math.cos(math.radians(testAngle)) * radius2)
        y = pt.y + (math.sin(math.radians(testAngle)) * radius2)
        newPt = gp.createobject("point")
        newPt.x = x
        newPt.y = y
        newPolygon.add (newPt)

        #Add the first point
        newPolygon.add (pt)        

        #Add feature
        insrec = insrecs.newrow()
        insrec.shape = newPolygon
        fld = fields.reset()
        fld = fields.next()
        while fld:
            if fld.name <> "Shape" and fld.name <> "FID":
                insrec.setvalue ( fld.name, rec.getvalue(fld.name))
            fld = fields.next()
        insrecs.insertrow(insrec)

        #Next records        
        n = n + 1
        rec = recs.next()        
    

    #gp.addmessage no of features
    gp.refreshcatalog(folder)
    gp.addmessage("\n" + str(n) + " features stored")

    #Completion message
    gp.addmessage("\n** SUSAN IS VERY COOL **\n")    


except:

    #Error
    gp.addmessage("\n** Error Encountered **\n")


finally:

    #Cleanup
    del gp