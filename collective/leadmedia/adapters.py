# Adapters

from zope.interface import implements
from collective.leadmedia.interfaces import ICanContainMedia
from Products.CMFCore.utils import getToolByName
from plone.app.uuid.utils import uuidToCatalogBrain
from plone.app.contenttypes.behaviors.collection import ICollection

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

<<<<<<< HEAD
        if item.portal_type == "Collection":
            brains = item.queryCatalog()
            for brain in brains:
                if hasattr(brain, 'meta_type'):
                    if brain.meta_type == "Dexterity Container":
                        item = brain.getObject()
                        result.append(ICanContainMedia(item).getLeadMedia())
                        return result
=======
        if item.portal_type in ["Collection", "Person"]:

            try:
                if item.portal_type == "Collection":
                    brains = item.queryCatalog()
                else:
                    brains = ICollection(item).results(limit=1, batch=False)
            
                for brain in brains:
                    if hasattr(brain, 'meta_type'):
                        if brain.meta_type == "Dexterity Container":
                            item = brain.getObject()
                            result.append(ICanContainMedia(item).getLeadMedia())
                            return result
                return result
            except:
                return []
>>>>>>> plone5
        else:
            if 'slideshow' in item.objectIds():
                #print "slideshow in ids"
                slideshow = item['slideshow']
<<<<<<< HEAD
=======
                try:
                    if uuidToCatalogBrain(slideshow.UID()).review_state != "published":
                        return []
                except:
                    return []

>>>>>>> plone5
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
<<<<<<< HEAD
=======
                            return result

            if 'archive' in item.objectIds():
                #print "slideshow in ids"
                slideshow = item['archive']
                try:
                    if uuidToCatalogBrain(slideshow.UID()).review_state != "published":
                        return []
                except:
                    return []

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
>>>>>>> plone5
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

<<<<<<< HEAD
=======
            elif brain_obj.portal_type == "Collection":
                result.append(ICanContainMedia(brain_obj).getLeadMedia())
                return result
>>>>>>> plone5

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
