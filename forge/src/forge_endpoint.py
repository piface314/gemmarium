from flask import Flask, request
from forge_ctrl import ForgeCtrl
from time import time
import base64
import traceback


class ForgeEndpoint:

    def __init__(self, ctrl: ForgeCtrl):
        self.ctrl = ctrl
        self.app = Flask(__name__)
        self.app.route("/gem", methods=["GET"])(self.gem)
        self.app.route("/fuse", methods=["POST"])(self.fuse)

    def gem(self):
        token = request.args.get('token')
        uid, username = self.ctrl.auth(base64.b64decode(token))
        if not uid:
            return dict(error="AuthError"), 401
        ok, wait = self.ctrl.check_quota(uid)
        if not ok:
            return dict(error="QuotaExceeded", wait=wait), 418
        gem = self.ctrl.choose_gem(username)
        self.ctrl.set_quota(uid)
        return dict(gem=base64.b64encode(gem).decode())
    
    def fuse(self):
        body = request.get_json()
        uid, username = self.ctrl.auth(base64.b64decode(body['token']))
        if not uid:
            return dict(error="AuthError"), 401
        peerid, gems = body['peerid'], [base64.b64decode(g) for g in body['gems']]
        try:
            self.ctrl.update_fusion_request(uid, peerid, uid, username, gems)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.ctrl.remove_fusion_request(uid, peerid)
            return dict(error="InvalidGems"), 400
        t0, ok = time(), False
        try:
            while time() - t0 <= 60:
                req = self.ctrl.get_fusion_request(uid, peerid)
                if req.is_complete() and req.has_fusion_set():
                    ok = True
                    break
        except:
            pass
        if not ok:
            return dict(error="Timeout"), 408
        req = self.ctrl.get_fusion_request(uid, peerid)
        fused, others = req.fusion
        gems = [fused, *others[uid]] if fused else others[uid]
        gems = [base64.b64encode(g).decode() for g in gems]
        self.ctrl.remove_fusion_request(uid, peerid, uid)
        return dict(gems=gems)
        
