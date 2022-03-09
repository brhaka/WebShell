# WebShell

## To Start
`npm run serve` on web-shell-vue starts the npm server for Vue, on localhost, port 8080

`source venv/bin/activate` for the virtual environment
`python(3) containerizer.py` starts the Python server on localhost, port 8000

Interface available on **localhost:8080**

Internal: python server available on **localhost:8000**

## Information
Commands (except for *exit*, *clear* and *search*) are sent to an Ubuntu Docker container that is created when the page loads.
This container will stay active as long as there's at least one interaction every 10 minutes.