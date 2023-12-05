import json
from os.path import isfile, getsize
from typing import TextIO

from django.test import TestCase
from django.conf import settings


def open_file(path: str, operation: str) -> str or TextIO:
    """open file acc. to need"""
    f = open(str(path), operation)
    if operation == "r":
        return f.read()
    elif operation == "wb":
        return f


def save_text_file(filename, filesize, file_data):
    """create a file and write content of uploaded file"""
    try:
        path = settings.STATICFILES_DIRS[0] + rf"\uploaded_file\{filename}"
        if isfile(path):  # check file
            if getsize(path) == filesize:
                # file is not exist and its size is same
                return "exist"
        # file is new
        f = open_file(path, operation="wb")
        f.write(file_data)
        f.close()
        return path
    except Exception as e:
        print("Saving Error:-", e)
        return False


def process_csv_file(path):
    """open uploaded file and perform computation"""
    candle = []
    result = []
    try:
        file_data = open_file(path, operation="r").split("\n")

        heading = file_data[0].split(",")  # splitting very first line of text line

        #  build a candle list data
        for num, data in enumerate(file_data[1:]):
            temp_data = data.split(",")
            candle.append({
                "id": num+1,
                # heading[0]: temp_data[0],
                heading[3]: temp_data[3],  # open
                heading[4]: temp_data[4],  # high
                heading[5]: temp_data[5],  # low
                heading[6]: temp_data[6],  # close
                heading[7]: temp_data[7],  # volume
                heading[1]: temp_data[1],  # date
                heading[2]: temp_data[2],  # time
            })

        print("data", len(candle))

        # compute the result for json file
        for i, d in enumerate(range(0, len(candle), 10)):
            temp = []
            for c in candle[d:d+10]:
                temp.append(list(c.values())[1:-2])
            res = compute_trade_data(temp)
            result.append({
                "id": i + 1,
                # heading[0]: temp_data[0],
                heading[3]: res[0],  # open
                heading[4]: res[1],  # high
                heading[5]: res[2],  # low
                heading[6]: res[3],  # close
                heading[7]: res[4],  # volume
                heading[1]: candle[d].get("DATE"),  # date
                heading[2]: candle[d].get("TIME"),  # time
            })
        print("result", len(result))
        return result
    except Exception as e:
        print("Processing File Error:-", e)
        return False


def compute_trade_data(trade_data: list):
    """this computes data"""
    trade_data = list(zip(*trade_data))
    _open_ = trade_data[0]
    _high_ = trade_data[1]
    _low_ = trade_data[2]
    _close_ = trade_data[3]
    _volume_ = trade_data[4]
    return _open_[0], max(_high_), min(_low_), _close_[-1], _volume_[-1]
