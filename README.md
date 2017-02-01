## docker-show_my_idevices
Docker recepie for tracking iDevices on Google MAp using iCloud API (find-my-iphone)

## TO BUILD a docker image
- $ INSTALL docker-engine
- $ git clone https://github.com/rajr0/docker-show_my_idevices
- $ cd docker-show_my_idevices
- $ docker build -t show_my_idevices .

### TO RUN
- $ export ITUNES_UNAME='your iTunes uuser-name'
- $ export ITUNES_PASSWD='your iTunes password'
- $ docker run --name show_my_idevices -itd  -p 8000:8000 -e ITUNES_UNAME -e ITUNES_PASSWD show_my_idevices

** OR you can pass all user-name/password as arguments
- $ docker run --name show_my_idevices -itd  -p 8000:8000 show_my_idevices ./show_my_idevices.py "your iTunes uuser-name" "your iTunes password"

### then point your browser to http://localhost:8000 to see all your iDevices as pins

## Inspirations
- https://wrightshq.com/playground/placing-multiple-markers-on-a-google-map-using-api-3/
- http://twistedmatrix.com/trac/
- https://github.com/picklepete/pyicloud
