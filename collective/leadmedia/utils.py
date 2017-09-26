# # # # # # # 
# U T I L S #
# # # # # # #

from zope.annotation.interfaces import IAnnotations
from plone.app.imagecropping import PAI_STORAGE_KEY

# AUTO CROPPING
def addCropToTranslation(original, translated):
    # Add crops if original has crops
    if hasCropsTranslation(original):
        fieldname = 'image'
        scale = 'mini'
        view = original.restrictedTraverse('@@crop-image')

        box = view._storage['{0:s}_{1:s}'.format(fieldname, scale)]

        # Create new crops
        translated_view = translated.restrictedTraverse('@@crop-image')
        translated_view._crop(fieldname, scale, box)

        # Re-index current crops
        view._crop(fieldname, scale, box)

def hasCropsTranslation(obj):
    #
    # Check if object has crops defined
    #
    annotations = IAnnotations(obj).get(PAI_STORAGE_KEY)
    if annotations != None:
        if 'image_mini' not in annotations.keys():
            return True
        else:
            return False
    else:
        return False
        
def hasCrops(ob):
    return False
    #
    # Check if object has crops defined
    #
    annotations = IAnnotations(ob).get(PAI_STORAGE_KEY)
    if annotations != None:
        if 'image_mini' not in annotations.keys():
            return False
        else:
            return False
    else:
        return False

def autoCropImage(ob):
    if not hasCrops(ob):
        view = ob.restrictedTraverse('@@crop-image')
        w, h = ob.image.getImageSize()

        #
        # Make crop centered
        #

        # 3:2 aspect ratio
        aspect_ratio = 1.5

        width = min(w, h*aspect_ratio)
        height = min(w/aspect_ratio, h)
        left = (w - width)/2
        top = (h - height)/2
        box = (int(left),int(top),int(left+width),int(top+height))

        # Square

        view._crop(fieldname='image', scale="mini", box=box)
        
        if w > h:
            delta = w - h
            left = int(delta/2)
            upper = 0
            right = h + left
            lower = h
        else:
            delta = h - w
            left = 0
            upper = int(delta/2)
            right = w
            lower = w + upper

        box = (left, upper, right, lower)

        view._crop(fieldname='image', scale="preview", box=box)

        ob.reindexObject()

def imageObjectCreated(ob, event):
    #print "Crop - Image object created!!"
    if ob.portal_type == "Image":
        if ob.image != None:
            autoCropImage(ob)
    
