#!/usr/bin/env python3

import requests
import argparse
import json
import subprocess
import shlex

## https://docs.imagga.com/?python

# api_endpoint_colors = api_endpoint + '/colors'

class ImaggaAPI:
    def __init__(self):
        self.api_key = ''
        self.api_secret = ''
        # https://docs.imagga.com/?python#tags
        self.threshold = 20
        self.language = "en"
        self.auth = (self.api_key, self.api_secret)

    def _fix_json(self, j):
        """
        Helper function to address Json with single quotes.
        json: an malformed json string

        returns a proper json object
        """
        j_dumped = json.dumps(j)
        j_loaded = json.loads(j_dumped)
        return j_loaded

    def getTags(self, imageId):
        """
        Get list of tags using the Imagga API

        imageId: image_upload_id that you want tags from

        returns: list of tags as a json object
        """
        url = "https://api.imagga.com/v2/tags"
        payload = {
            "image_upload_id" : imageId,
            "threshold" : self.threshold,
            "language"  : self.language
        }
        r = requests.get(url, params=payload, auth=self.auth)
        result = r.json()
        return self._fix_json(result["result"]["tags"])  

    def getColors(self, imageId):
        """
        Get list of identified colors using the Imagga API

        imageID: The image_upload_id

        returns: list of colors
        """
        url = "https://api.imagga.com/v2/colors"
        payload = {
            "image_upload_id" : imageId
        }
        r = requests.get(url, params=payload, auth=self.auth)
        result = r.json()
        return self._fix_json(result["result"]["colors"])  

    def postFile(self, file):
        """
        Post the image to Imagga

        file: file to post

        returns the entire json result as a json object
        """
        url = "https://api.imagga.com/v2/uploads"
        r = requests.post(url,
            auth=self.auth,
            files={'image': open(file, 'rb')}
            )
        result = r.json()
        return self._fix_json(result)

    def deleteImage(self, image_id):
        """
        Imagga deletes all uploads after 24 hours, so this is optional, but nice.

        image_id: The upload_image_id to delete

        returns: the status code
        """
        url = "https://api.imagga.com/v2/uploads/" + image_id
        r = requests.delete(url,
            auth=self.auth,
        )
        if r.status_code == 200:
            return "success"
        else:
            return "failed"

def parse_arguments():
    """
    Parses arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        help="Input file",
        )
    parser.add_argument(
        "--overwrite-file",
        help="Overwrite images in-place when calling exiftool",
        action="store_true"
    )
    parser.add_argument(
        "--append-tags",
        help="Append (add) keywords instead of replacing",
        action="store_true"
    )
    parser.add_argument(
        "--skip-if-tagged",
        dest="skipIfTagged",
        help="Skip file if it has any existing tags",
        action="store_true"
    )
    args = parser.parse_args()
    return args

def get_result_upload_id(result):
    """
    Helper function to get the upload_id from the results json
    """
    return result["result"]["upload_id"]

def CountJsonTags(json_tags):
    return len(json_tags)

def sh(command):
    return subprocess.getoutput(command)

def FileHasTags(file):
    o = sh("exiftool -keywords {}".format(shlex.quote(file)))
    if o:
        return True
    else:
        return False

# def WriteFileTags(file, tags, colors, language, append=False, overwriteFile=False):
def WriteFileTags(file, tags, language, append=False, overwriteFile=False):
    t = ""
    for i in range(len(tags)):
        if append:
            t = t + " -keywords+='" + tags[i]["tag"][language] + "'"
        else:
            t = t + " -keywords='" + tags[i]["tag"][language] + "'"
    # for z in ["foreground_colors", "image_colors", "background_colors"]:
    #     for l in range(len(colors[z])):
    #         if append:
    #             t = t + " -keywords+='" + colors[z][l]["closest_palette_color"] + "'"
    #         else:
    #             t = t + " -keywords='" + colors[z][l]["closest_palette_color"] + "'"
    if overwriteFile:
        t = t + " -overwrite_original"
    # use shlex to escape special characters
    c = "exiftool {tag} {file}".format(
        tag=t,
        file=shlex.quote(file),
    )
    return sh(c)

def main():
    i = ImaggaAPI()

    args = parse_arguments()
    file = args.file

    print("Checking for existing tags: ", end='')
    hasTags = FileHasTags(file)
    if hasTags:
        print("has tags")
    else:
        print("does not have tags")

    if not (hasTags and args.skipIfTagged):
        print("Posting file: {} ... ".format(file), end='')
        result = i.postFile(file)
        id = get_result_upload_id(result)
        print('{result}: {id}'.format(
            result=result["status"]["type"],
            id=id,
            ))

        print("Getting tags for uploaded file ... ", end="")
        tags = i.getTags(id)
        c = CountJsonTags(tags)
        print("{tags} tags retrieved.".format(
            tags=c
        ))

        # print("Getting colors for uploaded file ... ", end="")
        # colors = i.getColors(id)
        # c = len(colors["background_colors"]) + len(colors["image_colors"]) + len(colors["foreground_colors"])
        # print("{colors} colors retrieved.".format(
        #     colors = c
        # ))
        
        print("Deleting uploaded image ... ", end='')
        result = i.deleteImage(id)
        print(result)

        print("Writing new file tags ... ", end='')
        s = WriteFileTags(file, tags, i.language)
        #s = WriteFileTags(file, tags, colors, i.language)
        if s:
            print("success")
        else:
            print("failed")
    else:
        print("Skipping file as it has tags already.")

if __name__ == '__main__':
    main()
