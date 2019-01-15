# imagga-tool

## Background

`imagga-tool` is a Python script that makes use of the [Imagga image tagging service](https://imagga.com/solutions/auto-tagging.html) to automatically update supported photos with [IPTC keywords](http://photometadata.org/META-Resources-Field-Guide-to-Metadata#Keywords).

IPTC tags are used by many different photo-management applications to automatically organize and catalog photos. Some photo-management applications identify your images and index them accordingly. However, the data is not saved in your images, nor are you able to export it. Having tags in your images will help ensure that your images are able to be easily organized now and in the future.

This script, in combination with an Imagga API key, will allow you to easily submit images to Imagga and apply the resulting tags as IPTC keywords. This script only supports one image at a time. If you want to do a batch of images, simply set up a `for` loop to iterate over each one. 

## Installing

Requirements:

- [Python3](https://www.python.org/download/releases/3.0/)
- [exiftool](https://www.sno.phy.queensu.ca/~phil/exiftool/)
- Python3 [requests](https://pypi.org/project/requests/) package

MacOS users with [Homebrew](https://brew.sh) installed can run the following to fulfill these requirements:

```
brew install python3 exiftool
pip3 install requests
```

## Configuration

Configuration is done in the top of the file. Excerpt and links below:

```python
class ImaggaAPI:
    def __init__(self):
        self.api_key = ''
        self.api_secret = ''
        # https://docs.imagga.com/?python#tags
        self.threshold = 20
        self.language = "en"
```

## Use

Options are shown using `imagga-tool.py -h`:

```
usage: imagga-tool.py [-h] [--overwrite-file] [--append-tags]
                      [--skip-if-tagged]
                      file

positional arguments:
  file              Input file

optional arguments:
  -h, --help        show this help message and exit
  --overwrite-file  Overwrite images in-place when calling exiftool
  --append-tags     Append (add) keywords instead of replacing
  --skip-if-tagged  Skip file if it has any existing tags
```

Process a single image:

```
$ ~/bin/imagga-tool.py IMG_1439.jpeg 
Checking for existing tags: has tags
Posting file: IMG_1439.jpeg ... success: (image ID)
Getting tags for upload file ... 29 tags retrieved.
Deleting uploaded image ... success
Writing new file tags ... success
```

Verify tags were applied using `exiftool`:

```
$ exiftool -keywords IMG_1439.jpeg
Keywords                        : typewriter keyboard, keyboard, device, computer, key, technology, button, computer keyboard, type, close, buttons, office, keypad, equipment, communication, laptop, business, typing, keys, enter, letter, work, data input device, closeup, information, peripheral, alphabet, remote control, data
```

# Disclaimer

Error-free operation is not guaranteed, and behavior may change in future versions. Back up your stuff first!
