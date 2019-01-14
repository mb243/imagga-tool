# imagga-tool

`imagga-tool` is a Python script that makes use of the [Imagga image tagging service](https://imagga.com). 

This script, in combination with an Imagga API key, will allow you to easily submit images to Imagga and apply the resulting tags as IPTC keywords. This script only supports one image at a time. If you want to do a batch of images, simply set up a `for` loop to iterate over each one. 

Options are shown using `imagga-tool.py -h`. 

Error-free operation is not guaranteed, and behavior may change in future versions. Back up your stuff first!

Configuration is done in the very top of the file. Excerpt below:

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

This requires that `exiftool` be available on your path, as it calls `exiftool` to update the IPTC tags. 

Example run and output below:

```
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
```
$ exiftool -keywords IMG_3312.JPG
Keywords                        : tree, woody plant, forest, autumn, trees, vascular plant, landscape, park, fall, leaves, road, southern beech, woods, foliage, path, leaf, scenic, scenery, plant, grass, season, outdoors, peaceful, yellow, rural, wood, scene, outdoor, countryside
```
