# tower-circle-sectors
ArcGIS tool used to create coverage areas from cell tower points.
- The ArcGIS tool box containing the tool is located in tower-circle-sectors/ui_tools/Tower Coverage Tools.tbx
- The source of the tool is set to point_angle_range_to_polygon.py and must be imported before the .tbx file is distrubted.

The tool takes parameters of a point file and three fields that specify the direction, centeral angle and radius of the resulting circle sector coverage area polygon.
The 3 fields are:
- azimuth: Angle of center line of the resulting cirlce sector. Angle must be in degrees.
- range: Radius of the resulting circle sector. Must be in meters.
- beamwidth: Total degrees covered by the central angle of the resulting circle sector. Must be in degrees.
