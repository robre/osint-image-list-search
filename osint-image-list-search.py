# robre 2019
import os
import urllib.request
import sys
tmpdir = "/tmp/osint_images/"
from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from msrest.authentication import CognitiveServicesCredentials
subscription_key = "ADD YOUR AZURE/BING SEARCH API KEY HERE"

def download_top_images(searchterm, n=4):
    assert(n>1)
    # Download the top n images for an image search on some search provider.
    # Returns a list of image urls

    # clean up search string (no special chars etc)
    searchterm = ''.join(c for c in searchterm if c.isalnum() or c == " ")
    try:
        client = ImageSearchAPI(CognitiveServicesCredentials(subscription_key))
        image_results = client.images.search(query=searchterm)
    except Exception as e:
        print("unknown Error retrieving {}".format(seachterm))
        print(e)
        return []
    if image_results.value:
        my_results = image_results.value[:n]
        res = []
        for r in my_results:
            res.append(r.content_url)
        return res
    else:
        print("No images found for {}".format(searchterm))
        return []

def combine_images(imagelist, filename):
    d = "/tmp/osint_images_temp/"
    try:
        os.mkdir(d)
    except FileExistsError:
        pass
    files = []
    # combines multiple image urls into a single image
    for n, result in enumerate(imagelist):
        n= str(n)
        filetype = result.split(".")[-1]
        try:
            urllib.request.urlretrieve(result, d + n + "." + filetype)
        except:
            continue
        files.append(d+n+"."+filetype)
    os.system("montage {} -geometry 400x400+2+2 {}".format(" ".join(files), filename))
    print("created {}".format(filename))


def create_image_from_searchterm(searchterm, filename, n=4):
    assert(n>1)
    top_images = download_top_images(searchterm, n=n)
    if len(top_images) == 0:
        return False
    if combine_images(top_images, filename):
        return True
    else:
        return False

def create_list_from_input_file(inputfile):
    return [line.strip() for line in open(inputfile, "r").readlines()]

def main():
    os.mkdir(tmpdir)

    if len(argv) < 2:
        print("Usage: $ python3 osint-image-list-search.py inputfile.txt\nWhere inputfile.txt is a file that contains one search term per line")
    inputfile = sys.argv[1]
    searchterms = create_list_from_input_file(inputfile)

    
    for count, searchterm in enumerate(searchterms):
        filename = tmpdir + str(count) + ".png"
        create_image_from_searchterm(searchterm, filename, n=4)
    
    with open(tmpdir + "index.txt", "w") as f:
        for c,s in enumerate(searchterms):
            f.write("{} : {}\n".format(c,s))
main()
