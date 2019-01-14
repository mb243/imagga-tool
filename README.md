# imagga-tool

## Background

`imagga-tool` is a Python script that makes use of the [Imagga image tagging service](https://imagga.com/solutions/auto-tagging.html). 

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
## https://docs.imagga.com/?python
api_key = '' 
api_secret = '' 
# https://docs.imagga.com/?python#api-endpoints
api_endpoint = 'https://api.imagga.com/v2'
api_endpoint_uploads = api_endpoint + '/uploads'
api_endpoint_tags = api_endpoint + '/tags'
api_endpoint_colors = api_endpoint + '/colors'
# https://docs.imagga.com/?python#tags
api_threshold = 20
api_language = "en"
```

## Use

Options are shown using `imagga-tool.py -h`. 

Process a single image:

```
$ imagga-tool.py -i IMG_3312.JPG
Posting image: IMG_3312.JPG
- Uploaded image ID: (omitted)
- Counted tags: 29
- Deleting image_id: (omitted)
Preparing to update tags for image: IMG_3312.JPG
Existing keywords:

- Assembling new list of keywords... tree, woody plant, forest, autumn, trees, vascular plant, landscape, park, fall, leaves, road, southern beech, woods, foliage, path, leaf, scenic, scenery, plant, grass, season, outdoors, peaceful, yellow, rural, wood, scene, outdoor, countryside, 
- Writing new tags...
    1 image files updated
```

Verify tags were applied using `exiftool`:

```
$ exiftool -keywords IMG_3312.JPG
Keywords                        : tree, woody plant, forest, autumn, trees, vascular plant, landscape, park, fall, leaves, road, southern beech, woods, foliage, path, leaf, scenic, scenery, plant, grass, season, outdoors, peaceful, yellow, rural, wood, scene, outdoor, countryside
```

# Disclaimer

Error-free operation is not guaranteed, and behavior may change in future versions. Back up your stuff first!
