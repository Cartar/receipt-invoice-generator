# receipt-invoice-generator

## This service is hosted on Google Run with the following setup instructions:
### Note
1. By default, flask maps to port 5000. This [can be changed](https://stackoverflow.com/questions/60452377/docker-flask-app-not-working-port-issues), but if it isn't, docker run will neeed to use port 5000.
2. Mounting the current directly allows changes outside of app.py to be reflected in testing. Since the app is spun up during image creation, app.py requires a full tear-down and restart to be reflected in the browser.

'''sh
docker build --tag python-docker .
docker run -dp 5000:5000 \
    -w /app -v "$(pwd):/app" \
    python-docker
'''

Use the Docker GUI to delete images when done.


### Appendix A: Docker logs
Watch logs with:

'''sh
docker ps
'''

to fetch the containerID, and use it like:

'''sh
docker logs -f <containerID>
'''

### Appendix B: setup without Docker

'''sh
conda create -n receipt-creator python=3.9
conda activate receipt-creator
brew install Caskroom/cask/wkhtmltopdf
pip install pdfkit
pip install flask
'''

### Appendix C: testing with Curl

'''sh
curl -o test.pdf http://localhost:5000/receipt \
   -H "subtotal: 300"
'''
