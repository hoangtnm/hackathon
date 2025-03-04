import gmplot
from config import GeoLocations

location = GeoLocations()

latitude_list = [30.3358376, 30.307977, 30.3216419]
longitude_list = [77.8701919, 78.048457, 78.0413095]

gmap = gmplot.GoogleMapPlotter(location.latitude,
                               location.longitude,
                               location.zoom_level)

# gmap5.scatter(latitude_list, longitude_list, '# FF0000',
#               size=40, marker=False)
#
# # polygon method Draw a polygon with
# # the help of coordinates
# gmap5.polygon(latitude_list, longitude_list,
#               color='cornflowerblue')
gmap.draw('map.html')
