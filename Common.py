import os
import queue
from datetime import datetime
from glob import glob

import psutil
from api import XiGuaLiveApi
import json
import threading
from bypy import ByPy

_config_fp = open("config.json", "r", encoding="utf8")
config = json.load(_config_fp)
_config_fp.close()
bypy = ByPy()
doCleanTime = datetime.now()
_clean_flag = None

network = {
    "currentTime": datetime.now(),
    "out": {
        "currentByte": psutil.net_io_counters().bytes_sent,
    },
    "in": {
        "currentByte": psutil.net_io_counters().bytes_recv,
    }
}


def updateNetwork():
    global network
    network = {
        "currentTime": datetime.now(),
        "out": {
            "currentByte": psutil.net_io_counters().bytes_sent,
        },
        "in": {
            "currentByte": psutil.net_io_counters().bytes_recv,
        }
    }


def getTimeDelta(a, b):
    sec = (a - b).seconds
    ms  = (a - b).microseconds
    return sec+(ms/100000.0)


def _doClean(_force=False):
    global doCleanTime, _clean_flag
    _disk = psutil.disk_usage(".")
    if (_disk.percent > config["max"] and getTimeDelta(datetime.now(), doCleanTime) > 7200) or _force:
        doCleanTime = datetime.now()
        _list = sorted(glob("*.flv"), key=lambda x: datetime.utcfromtimestamp(os.path.getmtime(x)))
        for _i in _list:
            if not os.path.exists(_i):
                break
            doCleanTime = datetime.now()
            if (datetime.now() - datetime.utcfromtimestamp(os.path.getmtime(_i))).days >= config["exp"]:
                _clean_flag = True
                if config["dow"] == "bypy":
                    _res = bypy.upload(_i)
                    if _res == 0:
                        os.remove(_i)
                else:
                    os.system(config["dow"])
            else:
                break
            doCleanTime = datetime.now()
    _clean_flag = False


def doClean(_force=False):
    if _clean_flag:
        appendError("doClean request on cleaning, will ignore it")
        return
    p = threading.Thread(target=_doClean, args=(_force,))
    p.setDaemon(True)
    p.start()


def getCurrentStatus():
    _disk = psutil.disk_usage(".")
    _mem  = psutil.virtual_memory()
    _delta= getTimeDelta(datetime.now(),network["currentTime"])
    _net  = psutil.net_io_counters()
    if 60 > _delta > 0:
        _inSpeed = (_net.bytes_recv - network["in"]["currentByte"]) / _delta
        _outSpeed = (_net.bytes_sent - network["out"]["currentByte"]) / _delta
    else:
        _outSpeed = 0
        _inSpeed = 0
    updateNetwork()
    if getTimeDelta(datetime.now(), doCleanTime) > 3600:
        doClean()
    return {
        "memTotal": parseSize(_mem.total),
        "memUsed": parseSize(_mem.used),
        "memUsage": _mem.percent,
        "diskTotal": parseSize(_disk.total),
        "diskUsed": parseSize(_disk.used),
        "diskUsage": _disk.percent,
        "cpu": psutil.cpu_percent(),
        "outSpeed": parseSize(_outSpeed),
        "inSpeed": parseSize(_inSpeed),
        "doCleanTime": datetime.strftime(doCleanTime, dt_format),
        "fileExpire": config["exp"],
    }


def reloadConfig():
    global config, _config_fp
    _config_fp = open("config.json", "r", encoding="utf8")
    config = json.load(_config_fp)
    _config_fp.close()


dt_format = "%Y/%m/%d %H:%M:%S"

broadcaster = ""
streamUrl = ""
isBroadcasting = False
updateTime = ""

forceNotDownload = False
forceNotBroadcasting = False
forceNotUpload = False
forceNotEncode = False
forceStartEncodeThread = False
forceStartUploadThread = False

uploadQueue = queue.Queue()
encodeQueue = queue.Queue()

uploadStatus = []
downloadStatus = []
encodeStatus = []
errors = []
operations = []


def appendOperation(obj):
    global operations
    if isinstance(obj, dict):
        if "datetime" not in obj:
            obj["datetime"] = datetime.strftime(datetime.now(), dt_format)
        operations.append(obj)
    else:
        operations.append({
            "datetime": datetime.strftime(datetime.now(), dt_format),
            "message": str(obj)
        })
    operations = operations[-config["elc"]:]


def parseSize(size):
    K = size / 1024.0
    if K > 1000:
        M = K / 1024.0
        if M > 1000:
            return "{:.2f}GB".format(M / 1024.0)
        else:
            return "{:.2f}MB".format(M)
    else:
        return "{:.2f}KB".format(K)


def appendUploadStatus(obj):
    global uploadStatus
    if isinstance(obj, dict):
        if "datetime" not in obj:
            obj["datetime"] = datetime.strftime(datetime.now(), dt_format)
        uploadStatus.append(obj)
    else:
        uploadStatus.append({
            "datetime": datetime.strftime(datetime.now(), dt_format),
            "message": str(obj)
        })
    uploadStatus = uploadStatus[-config["l_c"]:]


def modifyLastUploadStatus(obj):
    global uploadStatus
    if isinstance(obj, dict):
        if "datetime" not in obj:
            obj["datetime"] = datetime.strftime(datetime.now(), dt_format)
        uploadStatus[-1] = obj
    else:
        uploadStatus[-1]["message"] = str(obj)
        uploadStatus[-1]["datetime"] = datetime.strftime(datetime.now(), dt_format)


def appendEncodeStatus(obj):
    global encodeStatus
    if isinstance(obj, dict):
        if "datetime" not in obj:
            obj["datetime"] = datetime.strftime(datetime.now(), dt_format)
        encodeStatus.append(obj)
    else:
        encodeStatus.append({
            "datetime": datetime.strftime(datetime.now(), dt_format),
            "message": str(obj)
        })
    encodeStatus = encodeStatus[-config["l_c"]:]


def modifyLastEncodeStatus(obj):
    global encodeStatus
    if isinstance(obj, dict):
        if "datetime" not in obj:
            obj["datetime"] = datetime.strftime(datetime.now(), dt_format)
        encodeStatus[-1] = obj
    else:
        encodeStatus[-1]["message"] = str(obj)
        encodeStatus[-1]["datetime"] = datetime.strftime(datetime.now(), dt_format)


def appendDownloadStatus(obj):
    global downloadStatus
    if isinstance(obj, dict):
        if "datetime" not in obj:
            obj["datetime"] = datetime.strftime(datetime.now(), dt_format)
        downloadStatus.append(obj)
    else:
        downloadStatus.append({
            "datetime": datetime.strftime(datetime.now(), dt_format),
            "message": str(obj)
        })
    downloadStatus = downloadStatus[-config["l_c"]:]


def modifyLastDownloadStatus(obj):
    global downloadStatus
    if isinstance(obj, dict):
        if "datetime" not in obj:
            obj["datetime"] = datetime.strftime(datetime.now(), dt_format)
        downloadStatus[-1] = obj
    else:
        downloadStatus[-1]["message"] = str(obj)
        downloadStatus[-1]["datetime"] = datetime.strftime(datetime.now(), dt_format)


def appendError(obj):
    global errors
    if isinstance(obj, dict):
        if "datetime" not in obj:
            obj["datetime"] = datetime.strftime(datetime.now(), dt_format)
        errors.append(obj)
    else:
        errors.append({
            "datetime": datetime.strftime(datetime.now(), dt_format),
            "message": str(obj)
        })
    errors = errors[-config["elc"]:]


class downloader(XiGuaLiveApi):
    playlist = None

    def updRoomInfo(self):
        global broadcaster, isBroadcasting, updateTime, forceNotBroadcasting, forceNotDownload
        super(downloader, self).updRoomInfo()
        updateTime = datetime.strftime(datetime.now(), dt_format)
        broadcaster = self.roomLiver
        isBroadcasting = self.isLive
        if self.isLive:
            self.updPlayList()
        else:
            forceNotDownload = False
            forceNotBroadcasting = False
            self.playlist = False

    def updPlayList(self):
        global streamUrl
        if self.isLive:
            if "stream_url" in self._rawRoomInfo:
                if self.playlist is None:
                    self.playlist = None
                else:
                    self.playlist = self._rawRoomInfo["stream_url"]["flv_pull_url"]
                    self.playlist = self.playlist.replace("_uhd", "").replace("_sd", "").replace("_ld", "")
                    streamUrl = self.playlist
        else:
            streamUrl = None
            self.playlist = None

    def onLike(self, user):
        pass

    def onAd(self, i):
        pass

    def onChat(self, chat):
        pass

    def onEnter(self, msg):
        pass

    def onJoin(self, user):
        pass

    def onLeave(self, json):
        self.updRoomInfo()

    def onMessage(self, msg):
        pass

    def onPresent(self, gift):
        pass

    def onPresentEnd(self, gift):
        pass

    def onSubscribe(self, user):
        pass


api = downloader(config["l_u"])


def refreshDownloader():
    global api
    api = downloader(config["l_u"])
