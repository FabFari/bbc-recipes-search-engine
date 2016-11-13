import urllib2
import httplib
import os.path

from utils.utility_functions import open_inf

BASE_URL = "http://www.bbc.co.uk"
# file where are saved all recipe links
URLS_FILE = 'links_pythonIngredients.txt'
INPUT_DIR = "data"
OUTPUT_DIR = "recipes"


def get_list_from_file():
    """ from URLS_FILE file it reads this file and put in a list one line for each list's element
           :param Nothing(void)
           :return urls_list: list contents all links
    """
    print '-------- getListFromFile called -----------'
    in_file = open('..\\{}\\{}'.format(INPUT_DIR, URLS_FILE), "r")
    urls_list = []

    for line in in_file:
        # -1 because in the file there is a new line "\n" and we do not want to save in the list
        urls_list.append(BASE_URL + line[:len(line)-1])

    print '#size {} : {}'.format(URLS_FILE, len(urls_list))
    urls_list.sort()
    return urls_list


def save_local_copy(urls_list):
    """ from file where are saved all recipes' link we read one by one and it downloads
            one page at time
           :param Nothing(void)
           :return: all recipes' files saved and broke link find
    """
    print '-------- saveLocalCopy called -----------------'
    # we can find a link that point a expired page
    broke_links = []

    curr_num = 0
    for url in urls_list:
        # try to read the url
        page = open_inf(url)

        if page == -1:
            broke_links.append(url)
        else:
            # read the page's content
            page_content = page.read()
            name = url[len(BASE_URL + '/food/recipes/'):len(url)]
            print "recipe #{}: {}".format(curr_num, name)
            f = open("..\\{}\\{}.html".format(OUTPUT_DIR, name), 'w')
            # write the page in .html file
            f.write(page_content)
            f.close()

        curr_num += 1

    put_into_file(broke_links, 'broke_links')


def put_into_file(recipes_urls, name):
    """ put into the neme file the content of the list


                   :param name: file where to put the content
                   :param links_recipes: list of link
                   :return: Nothing(void)
     """
    recipes_set = set(recipes_urls)
    print '#size {} : {}'.format(name, len(recipes_set))

    # save into the file
    out_file = open(name+".txt", "w")
    for link in recipes_set:
        out_file.write(link + '\n')
    out_file.close()


if __name__ == '__main__':
    from utils.utility_functions import ensure_dir

    ensure_dir(INPUT_DIR)
    # get all links from URLS_FILE
    links = get_list_from_file()
    # for each link download the page and save it
    save_local_copy(links)
