import os
import json
import csv
import urllib2
import httplib


def ensure_dir(dir_name):
    if not os.path.exists(os.path.join(os.pardir, dir_name)):
        os.makedirs(os.path.join(os.pardir, dir_name))


def load_json(filename, in_dir):
    with open(os.path.join(os.pardir, in_dir, filename)) as json_data:
        data = json.load(json_data)
    return data


def load_tsv(tsv, in_dir):
    lines = []
    with open(os.path.join(os.pardir, in_dir, tsv), 'rb') as tsv_in:
        tsv_in = csv.reader(tsv_in, delimiter='\t')
        for row in tsv_in:
            lines.append(row)

    return lines


def open_inf(url):
    for i in range(10):
        try:
            # page = urllib2.urlopen('http://'+url)
            page = urllib2.urlopen(url, timeout=1)
            return page
        except (IOError, httplib.HTTPException):
            print "[open_inf] httplib error:"
        except:  # urllib2.URLError:
            print "[open_inf] error error:"
    return -1
