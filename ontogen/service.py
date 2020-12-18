from collections import OrderedDict
from flask import abort, Flask, request, render_template, redirect, session
from flask_cors import CORS
from flask_socketio import SocketIO

import json
import os

app = Flask(__name__)

CORS(app)

socketio = SocketIO(app)


@app.route("/ontogen/api/generate", methods=["GET"])
def api_generate():
    if "otmr" not in request.args:
        return "Parameter 'otmr' required", 403

    log = "log" in request.form and request.form["log"].lower() == "true"
    dc = "dc" in request.form and request.form["dc"].lower() == "true"
    dmp = "dmp" in request.form and request.form["dmp"].lower() == "true"
    return_one_result = "oneresult" in request.form and request.form["oneresult"].lower() == "true"
    is_robot = "isrobot" in request.form and request.form["isrobot"].lower() == "true"

    rargs = "rargs" in request.form and request.form["rargs"].lower() == "true"
    rargs_root_agent = request.form["rargs-root-agent"] if "rargs-root-agent" in request.form else ""
    rargs_root_beneficiary = request.form["rargs-root-beneficiary"] if "rargs-root-beneficiary" in request.form else ""
    rargs_frame_prefix = request.form["rargs-prefix"] if "rargs-prefix" in request.form else ""
    rargs_frame_delim = request.form["rargs-delim"] if "rargs-delim" in request.form else ""
    rargs_concept_prefix = request.form["ont-space"] if "ont-space" in request.form else ""

    robot_args = {
        "root-agent": rargs_root_agent,
        "root-beneficiary": rargs_root_beneficiary,
        "frame-prefix": rargs_frame_prefix,
        "frame-delim": rargs_frame_delim,
        "concept-prefix": "@" + rargs_concept_prefix + ".",
    } if rargs else {}

    try:
        tmr = request.args["otmr"]
        tmr = dict_to_tmr(tmr)
        entry = OntoGenRunner.run(tmr, debug=False)

        return json.dumps(entry)
    except Exception:
        return "Could not generate from the input oTMR. Is if formatted correctly?", 404
