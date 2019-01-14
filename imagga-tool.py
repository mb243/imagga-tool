#!/usr/bin/env python3

import requests
import argparse
import json
import subprocess

## https://docs.imagga.com/?python
api_key = ''
api_secret = ''
api_endpoint = 'https://api.imagga.com/v2'
api_endpoint_uploads = api_endpoint + '/uploads'
api_endpoint_tags = api_endpoint + '/tags'
api_endpoint_colors = api_endpoint + '/colors'
api_threshold = 20
api_language = "en"
##

def parse_arguments():
    """
    Parses arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--image", 
        help="Input file", 
        required=True
        )
    parser.add_argument(
        "-O", "--overwrite",
        help="Overwrite images in-place when calling exiftool",
        action="store_true"
    )
    args = parser.parse_args()
    return args

def get_result_upload_id(result):
    """
    Get the upload_id from the results json
    """
    return result["result"]["upload_id"]

def fix_json(j):
    """
    Workaround function to address Imagga sending back Json with single quotes
    """
    jd = json.dumps(j)
    jl = json.loads(jd)
    return jl
    
def post_image(image):
    """
    Post the image to Imagga
    """
    print("Posting image: {image}".format(
        image=image
    ))
    r = requests.post(api_endpoint_uploads,
        auth=(api_key, api_secret),
        files={'image': open(image, 'rb')}
        )
    result = r.json()
    return fix_json(result)

def delete_image(image_id):
    """
    Delete the image. Not really needed because Imagga deletes 
    everything you upload after 24 hours, but still a nice-to-do
    """
    print('- Deleting image_id: {image_id}'.format(
        image_id=image_id
    ))
    url = api_endpoint_uploads + '/' + image_id
    r = requests.delete(url,
        auth=(api_key, api_secret),
    )
    return r.status_code

def get_tags(image_id):
    url = api_endpoint_tags
    payload = {
        "image_upload_id" : image_id,
        "threshold" : api_threshold,
        "language"  : api_language
    }
    r = requests.get(url, params=payload, auth=(api_key, api_secret))
    result = r.json()
    return fix_json(result["result"]["tags"])

def count_tags(json_tags):
    l = len(json_tags)
    print("- Counted tags: {tags}".format(
        tags=l
    ))
    print("- Detected tags: ", end='')
    for i in range(l):
        print(json_tags[i]["tag"][api_language], end=', ')
    print()
    return l

def update_tags(image, tags, overwrite=False):
    """
    Updates the image, writing the tags to it. 
    NOTE: I haven't been able to find a stable, working python3 library to handle
    EXIF/IPTC keyword writing. For this reason, this uses 'exiftool' to handle keywords
    PRs are welcome to change this behavior.
    """
    t = ""
    print("Preparing to update tags for image: {}".format(
        image
    ))
    out = subprocess.getoutput("exiftool " + image + " -keywords")
    print("Existing keywords:")
    print(out)
    print("- Assembling new list of keywords... ", end='')
    for i in range(len(tags)):
        print(tags[i]["tag"][api_language], end=', ')
        t = t + " -keywords=\"" + tags[i]["tag"][api_language] + "\""
    print()
    print("- Writing new tags...")
    if overwrite:
        t = t + " -overwrite_original"
    out = subprocess.getoutput("exiftool " + image + t)
    print(out)
    
def main():
    args = parse_arguments()
    result = post_image(args.image)
    image_id = get_result_upload_id(result)
    print("- Uploaded image ID: {image_id}".format(
        image_id = image_id
    ))
    t = get_tags(image_id)
    count_tags(t)
    delete_image(image_id)
    update_tags(args.image, t, args.overwrite)

if __name__ == '__main__':
    main()
