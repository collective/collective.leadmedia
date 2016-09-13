# Adapters

from zope.interface import implements
from collective.leadmedia.interfaces import ICanContainMedia
from Products.CMFCore.utils import getToolByName

class MediaHandling(object):
    implements(ICanContainMedia)

    def __init__(self, context):
        self.context = context

    def getMedia(self):
        """
        Get media 
        """
        item = self.context
        result = []

        if item.portal_type == "Collection":
            try:
                brains = item.queryCatalog()
                for brain in brains:
                    print brain.meta_type
                    if hasattr(brain, 'meta_type'):
                        if brain.meta_type == "Dexterity Container":
                            item = brain.getObject()
                            result.append(ICanContainMedia(item).getLeadMedia())
                            return result
            except:
                return result
        else:
            if 'slideshow' in item.objectIds():
                #print "slideshow in ids"
                slideshow = item['slideshow']
                #print str(slideshow.objectIds())
                for content in slideshow.objectIds():
                    content_obj = slideshow[content]

                    if content_obj.portal_type == "Image":
                        if content_obj.image != None:
                            result.append(content_obj)
                            return result

                    # If folderish content inside slideshow folder
                    elif hasattr(content_obj, 'meta_type'):
                        if content_obj.meta_type == "Dexterity Container" and content_obj.portal_type != "Folder":
                            if hasattr(content_obj, 'hasMedia'):
                                if content_obj.hasMedia:
                                    result.append(ICanContainMedia(content_obj).getLeadMedia())
                                    return result
                        
                        elif content_obj.meta_type == "Dexterity Container" and content_obj.portal_type == "Folder":
                            result.append(ICanContainMedia(content_obj).getLeadMedia())
                            return result

                return result

        # No slideshow
        brains = item.objectIds()

        for brain in brains:
            brain_obj = item[brain]

            if brain_obj.portal_type == "Image":
                result.append(brain_obj)
                return result

            # if folderish item inside item folder
            elif brain_obj.meta_type == "Dexterity Container" and brain_obj.portal_type == "Folder":
                result.append(ICanContainMedia(brain_obj).getLeadMedia())
                return result

            elif brain_obj.meta_type == "Dexterity Container" and brain_obj.portal_type != "Folder":
                result.append(ICanContainMedia(brain_obj).getLeadMedia())
                return result

            elif brain_obj.portal_type == "Collection":
                result.append(ICanContainMedia(brain_obj).getLeadMedia())
                return result

        return result

    def hasMedia(self):
        """
        Check if item has media 
        """
        
        media = self.getMedia()

        if len(media) > 0:
            return True
        else:
            return False

    def getLeadMedia(self):
        """
        Get the lead media
        """

        media = self.getMedia()
        if len(media) > 0:
            return media[0]
        else:
            return None
