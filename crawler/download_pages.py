import urllib2
import httplib
import os.path

BASE_URL = "http://www.bbc.co.uk"
URLS_FILE = 'links_pythonIngredients.txt'
INPUT_DIR = "data"
OUTPUT_DIR = "recipes"


def get_list_from_file():
    print '-------- getListFromFile called -----------'
    in_file = open('..\\{}\\{}'.format(INPUT_DIR, URLS_FILE), "r")
    urls_list = []

    for line in in_file:
        # -1 perche nel file c'e' la new line(\n)
        urls_list.append(BASE_URL + line[:len(line)-1])

    print '#size {} : {}'.format(URLS_FILE, len(urls_list))
    urls_list.sort()
    return urls_list


def save_local_copy(urls_list):
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from utils.utility_functions import open_inf

    print '-------- saveLocalCopy called -----------------'
    broke_links = []

    curr_num = 0
    for url in urls_list:
        page = open_inf(url)

        if page == -1:
            broke_links.append(url)
        else:
            page_content = page.read()
            name = url[len(BASE_URL + '/food/recipes/'):len(url)]
            print "recipe #{}: {}".format(curr_num, name)
            f = open("..\\{}\\{}.html".format(OUTPUT_DIR, name), 'w')
            f.write(page_content)
            f.close()

        curr_num += 1

    put_into_file(broke_links, 'broke_links')


def put_into_file(recipes_urls, name):
    recipes_set = set(recipes_urls)
    print '#size {} : {}'.format(name, len(recipes_set))

    # save into the file
    out_file = open(name+".txt", "w")
    for link in recipes_set:
        out_file.write(link + '\n')
    out_file.close()


if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from utils.utility_functions import ensure_dir
    else:
        from ..utils.utility_functions import ensure_dir

    ensure_dir(INPUT_DIR)
    links = get_list_from_file()
    save_local_copy(links)
