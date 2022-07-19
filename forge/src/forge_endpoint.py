from forge_ctrl import ForgeCtrl
from time import time
from rmi.forge_pb2_grpc import ForgeServicer
from rmi.forge_pb2 import GemResponse, FusionResponse
import traceback


class ForgeEndpoint(ForgeServicer):

    def __init__(self, ctrl: ForgeCtrl):
        self.ctrl = ctrl

    def gem(self, request, context):
        print(f"{context.peer()}: gem({str(request).strip()})")
        uid, username = self.ctrl.auth(request.token)
        if not uid:
            return GemResponse(error="AuthError")
        print(f"{context.peer()}: checking quota for {username}...")
        ok, wait = self.ctrl.check_quota(uid)
        if not ok:
            return GemResponse(error="QuotaExceeded", wait=wait)
        print(f"{context.peer()}: choosing gem...")
        gem = self.ctrl.choose_gem(username)
        self.ctrl.set_quota(uid)
        return GemResponse(gem=gem)
    
    def fuse(self, request, context):
        print(f"{context.peer()}: fuse({str(request).strip()})")
        uid, username = self.ctrl.auth(request.token)
        if not uid:
            return FusionResponse(error="AuthError")
        print(f"{context.peer()}: attempting fusion...")
        peerid, gems = request.peerid, [g for g in request.gems]
        try:
            self.ctrl.update_fusion_request(uid, peerid, uid, username, gems)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.ctrl.remove_fusion_request(uid, peerid)
            return FusionResponse(error="InvalidGems")
        t0, ok = time(), False
        print(f'{context.peer()}: waiting for peer...')
        try:
            while time() - t0 <= 60:
                req = self.ctrl.get_fusion_request(uid, peerid)
                if req.is_complete() and req.has_fusion_set():
                    print(f'{context.peer()}: peer connected')
                    ok = True
                    break
        except:
            pass
        if not ok:
            print(f'{context.peer()}: timeout')
            return FusionResponse(error="Timeout")
        req = self.ctrl.get_fusion_request(uid, peerid)
        fused, others = req.fusion
        gems = [fused, *others[uid]] if fused else others[uid]
        self.ctrl.remove_fusion_request(uid, peerid, uid)
        return FusionResponse(gems=gems)
        
