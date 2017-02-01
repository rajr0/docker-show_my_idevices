#!/usr/bin/python
import os
import sys
from twisted.internet import reactor
from twisted.web.resource import Resource, NoResource
from twisted.web.server import Site
from pyicloud import PyiCloudService

html_page = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <!--
    Modified from the Debian original for Ubuntu
    Last updated: 2014-03-19
    See: https://launchpad.net/bugs/1288690
  -->
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>iDevices' Location</title>
  </head>
  <body>
    <style type="text/css" media="screen">
      #map_wrapper {{
          height: 400px;
      }}

      #map_canvas {{
          width: 100%;
          height: 100%;
      }}
    </style>
    <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
    <script>
    jQuery(function($) {{
        // Asynchronously Load the map API
        var script = document.createElement('script');
        script.src = "//maps.googleapis.com/maps/api/js?sensor=false&callback=initialize";
        document.body.appendChild(script);
    }});

    function initialize() {{
        var map;
        var bounds = new google.maps.LatLngBounds();
        var mapOptions = {{
            mapTypeId: 'roadmap'
        }};

        // Display a map on the page
        map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
        map.setTilt(45);

        // The below 'markers' is generated from the python code and passed to .format()
        {markers}

        // Display multiple markers on a map
        var marker, i;

        // Loop through our array of markers & place each one on the map
        for( i = 0; i < markers.length; i++ ) {{
            var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
            bounds.extend(position);
            marker = new google.maps.Marker({{
                position: position,
                map: map,
                title: markers[i][0]
            }});

            // Automatically center the map fitting all markers on the screen
            map.fitBounds(bounds);
            //map.setCenter(position);
        }}

        // Override our map zoom level once our fitBounds function runs (Make sure it only runs once)
        var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {{
            this.setZoom(11);
            google.maps.event.removeListener(boundsListener);
        }});

    }}
    </script>
  <div id="map_wrapper">
          <div id="map_canvas" class="mapping"></div>
  </div>
  </body>
</html>
"""

class iDevicesOnAMapPage(Resource):
  def __init__(self, username, password):
    Resource.__init__(self)
    #print username, password
    try:
      api = PyiCloudService(username, password)
    except:
      pass

    self.markers="        var markers = ["
    for i in api.devices:
      try:
        device="{}".format(i)
        device=device.replace("'", "")
        self.markers+="['{name}', {lon}, {lat}], ".format(name=device, lon=i.location()['latitude'], lat=i.location()['longitude'])
      except:
        pass
    self.markers+="        ];"

    #print self.markers

  def render_GET(self, request):
    return html_page.format(markers=self.markers)

class iDevicesOnAMap(Resource):
  def __init__(self, username='a', password='p'):
    Resource.__init__(self)
    self.username=username
    self.password=password

  def getChild(self, name, request):
    return iDevicesOnAMapPage(self.username, self.password)

def main(argv):
  root = iDevicesOnAMap(argv[0], argv[1])
  factory = Site(root)
  reactor.listenTCP(8000, factory)
  reactor.run()


if __name__ == "__main__":
  username=None
  password=None
  try:
    username=sys.argv[1]
  except:
    pass
  if username is None:
    username=os.environ['ITUNES_UNAME']
  try:
    password=sys.argv[2]
  except:
    pass
  if password is None:
    password=os.environ['ITUNES_PASSWD']
  if username is None or password is None:
    print ("usage: {prog_name} username password".format(prog_name=sys.argv[0]))
  else:
    main((username, password))
