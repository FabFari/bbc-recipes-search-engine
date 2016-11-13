import os
import json
import csv
import urllib2
import httplib


def ensure_dir(dir_name):
    """To test if a specific directory exists as sibling directory

        It's used to test if a specific directory exists in the parent
        directory of the directory hosting the calling python file.
        It's needed mainly to test the existence of input and output
        directory placed as sibling directory with respect to code ones.

        :param dir_name: The name of the directory to be tested
        :return: Nothing (void)
    """
    if not os.path.exists(os.path.join(os.pardir, dir_name)):
        os.makedirs(os.path.join(os.pardir, dir_name))


def load_json(filename, in_dir):
    """To read from a JSON file

        It's used to wrap the execution of json.load() method on
        an entire JSON file and in the end return all the data
        stored into the JSON file as a Python iterable object.

        :param filename: The name of the JSON file to be read
        :param in_dir: The sibling directory containing the JSON file
        :return: An iterable object containing the all the data read
    """
    with open(os.path.join(os.pardir, in_dir, filename)) as json_data:
        data = json.load(json_data)
    return data


def load_tsv(tsv, in_dir):
    """To read from a TSV file

        It's used to wrap the execution of csv.reader method on
        an entire TSV file and in the end return all the data
        stored into the TSV file as a Python iterable object.


        :param tsv: The name of the TSV file to be read
        :param in_dir: The sibling directory containing the TSV file
        :return: An iterable object containing the all the data read
    """
    lines = []
    with open(os.path.join(os.pardir, in_dir, tsv), 'rb') as tsv_in:
        tsv_in = csv.reader(tsv_in, delimiter='\t')
        for row in tsv_in:
            lines.append(row)

    return lines


def open_inf(url):
    """To open a web URL and returning the corresponding web page

        It's used to wrap the execution of urllib2.urlopen() method on
        a URL while managing the thrown exceptions.

        :param url: The URL to be opened
        :return: The received web page or -1 in case of errors
    """
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
