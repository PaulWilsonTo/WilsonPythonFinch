'''
  © Paul Wilson 2021
    Published under the Simple Public License:
    https://opensource.org/licenses/Simple-2.0
  For controlling BirdBrain Technologies Finch 2.0
    with Java and Python in online IDE like ReplIt
    see https://www.birdbraintechnologies.com/
'''
from flask import Flask, render_template, request
from wilson.internal.common import debug
from wilson.internal.message import Message
from wilson.internal.status import Status
from wilson.internal.worker import Worker
import logging
import os
import uuid

app = Flask(__name__, static_url_path="")
#app.config["SECRET_KEY"] = "FINCH"

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

@app.route("/")
def homePage():
  debug("WEBAPP homePage")
  fileList = [
    ".".join(fileName.split(".")[:-1])
    for fileName in os.listdir(".")
    if os.path.isfile(os.path.join(".", fileName))
      and fileName.endswith(".py")
    ]
  return render_template("index.html", fileList = fileList)

@app.route("/finch", defaults={"runModule": "main"})
@app.route("/finch/<runModule>")
def finchPage(runModule):
  uniqueId = uuid.uuid4()
  debug("WEBAPP finchPage", uniqueId, runModule)
  return render_template("finch.html", uniqueId = uniqueId, runModule = runModule)

@app.post("/startModule/<runModule>")
def startModule(runModule):
  sourceId = request.get_json()
  debug("WEBAPP startModule", sourceId, runModule)

  worker = Worker(sourceId, runModule)
  command = worker.getCommand()

  if command is None:
    response = "{}"
    status = 204
  else:
    response = command.toJson()
    status = 200

  return app.response_class(
    response=response,
    status=status,
    mimetype="application/json"
  )

@app.post("/nextCommand")
def nextCommand():
  sourceId = request.get_json()
  debug("WEBAPP nextCommand", sourceId)

  worker = Worker.getById(sourceId)
  command = worker.getCommand()

  if command is None:
    response = "{}"
    status = 204
  else:
    response = command.toJson()
    status = 200

  return app.response_class(
    response=response,
    status=status,
    mimetype="application/json"
  )

@app.post("/replyMessage")
def replyMessage():
  message = Message(request.get_json())
  debug("WEBAPP replyMessage", message.toString())

  worker = Worker.getById(message.sourceId)
  worker.popCommand(message)

  return app.response_class(
    response="{}",
    status=200,
    mimetype="application/json"
  )

@app.post("/updateStatus")
def updateStatus():
  status = Status(request.get_json())
  debug("WEBAPP updateStatus", status.toString())

  worker = Worker.getById(status.sourceId)
  worker.updateStatus(status.target, status.status)
  
  return app.response_class(
    response="{}",
    status=200,
    mimetype="application/json"
  )

debug("WEBAPP startup")
app.run(host="0.0.0.0")
