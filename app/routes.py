from __future__ import absolute_import

from flask import Response, render_template, request

from app import app

from .utils import create_cifs_share


@app.route("/")
@app.route("/index")
def index():
    """Route to ACME's landing page"""
    return render_template("index.j2")


@app.route("/create", methods=["POST"])
def create_share():
    """API Endpoint for creating a share"""
    snapmirror_enable = False
    sm_checked = request.form.get("snapmirror_enable")
    if sm_checked is not None:
        snapmirror_enable = True
    share_name = request.form.get("smb_name")
    size = request.form.get("smb_size")
    permission = request.form.get("smb_permission")
    # calling share create
    result = create_cifs_share(share_name, size, permission, snapmirror_enable)
    if result:
        return Response(status=200)
    else:
        return Response(status=400)
