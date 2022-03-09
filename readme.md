# WebShell
Shell developed in Vue.js, Python and Docker.
##### by Brhaka

---

## Start
`npm run serve` on **web-shell-vue** starts the npm server for Vue, on localhost, port 8080.

`source venv/bin/activate` for the virtual environment (recommended).

`python3 containerizer.py` starts the Python server on localhost, port 8000.

Interface available on **localhost:8080**

Internal: python server available on **localhost:8000**

---

## Information
When an user opens the WebShell, it sends a GET request for the Python server, which will create a Docker container using **debian:latest** and returns its id.

Everything typed in is sent to the Docker container, except for local commands (see bellow).

There, the input is executed and Python returns the result of it.

Both successfull and unsucessfull executions are treated and displayed accordingly on the terminal.

---

## Container-specifics
Containers have a maximum lifetime, currently of 21 minutes.

Every time there's any kind of interaction from the user with the container, the lifetime counter restarts. After the container is killed, in case the user tries to interact with it, a message will be displayed informing the user that the container has expired. Currently, when a container is killed it is also completely deleted.

In case the Python script is killed, it'll first destroy all containers that were still running (if any).

---

## Cryptography
Previously I mentioned that the server returns the container id for future requests. In fact, only the server has access to the actual docker container id. What is used for requests and therefore is visible to users is a cryptographed version of the id.

The cryptography is entirely handled on the server.

An implementation of a symmetric authenticated cryptography algorithm is used.

---

## Local commands
| Command | Arguments | Use |
| - | - | - |
| google | One | Searches *google.com* for the argument and embedds the page on the terminal screen. |
| search | One | Searches *en.wikipedia.com* for the argument and embedds the page on the terminal screen. |
| exit | None | Reloads the page |
| clear | None | Clears the history (cookie) and reloads the page |
| reload | None | Reloads the page |
| reboot | None | Reloads the page |
| restart | None | Reloads the page |

## Error codes
### (internal)
| Code | Description |
| - | - |
| 0x001 | Missing ID |
| 0x002 | Expired or invalid VM. reload, reboot or restart to continue |
| 0x003 | VM connection error |
| 0x004 | Missing Command |
| 0x005 | command not found |
| 0x006 | this command requires at least 1 argument |

##### by Brhaka