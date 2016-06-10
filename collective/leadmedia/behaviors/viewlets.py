# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import ViewletBase
from plone.app.layout.nextprevious.view import NextPreviousViewlet
from Products.mediaObject.object import ObjectView 
from Products.CMFCore.utils import getToolByName

class SlideshowViewlet(NextPreviousViewlet, ViewletBase, ObjectView):
    """ A simple viewlet which renders slideshow """

    def slideshow(self, context, parent):
        """
        Creates a slideshow with the media from parent
        """

        parentURL = ""
        slideshow_type = "regular"

        if parent != None:
            parentURL = parent.absolute_url()
        else:
            if context.portal_type == 'Collection':
                slideshow_type = "collection"
                brains = context.queryCatalog(batch=False, sort_on=context.sort_on)
                if len(brains) > 0:
                    lead_brain = brains[0]
                    lead_image = context.portal_catalog(UID=lead_brain.leadMedia)
                    if len(lead_image) > 0:
                        absolute_url = lead_image[0].getObject().absolute_url()
                    
                        scale = "large"

                        structure = """<div class="slick-slideshow %s">
                            <div><div class="inner-bg"><img src="%s/@@images/image/%s"/></div></div>
                            </div>""" % (slideshow_type, absolute_url, scale)
                        return structure

            elif context.portal_type == 'Folder':
                slideshow_type = "collection"
                catalog = getToolByName(context, 'portal_catalog')
                folder_path = '/'.join(context.getPhysicalPath())
                results = catalog(path={'query': folder_path, 'depth': 1}, sort_on='getObjPositionInParent')

                if len(results) > 0:
                    lead_brain = results[0]
                    lead_image = context.portal_catalog(UID=lead_brain.leadMedia)

                    if len(lead_image) > 0:
                        absolute_url = lead_image[0].getObject().absolute_url()
                        
                        scale = "large"

                        structure = """<div class="slick-slideshow %s">
                         <div><div class="inner-bg"><img src="%s/@@images/image/%s"/></div></div>
                        </div>""" % (slideshow_type, absolute_url, scale)
                        return structure
      

        if context.portal_type == "Object":
            slideshow_type = ""
            
        structure = """
            <div class="slick-slideshow %s" data-audio='' data-audio-duration=''>
            <a href="%s?recursive=true" id='slide-get-content'></a>    
            </div>
            """%(slideshow_type, parentURL)

        return structure

    def slideshowInContext(self, parent, request):
        inContext = False

        if parent.portal_type == 'Collection' or parent.portal_type == 'Folder' and 'folder_contents' not in request:
            return True

        if 'folder_contents' in request:
            return inContext
        try:
            inContext = 'slideshow' in parent
            return inContext
        except:
            return inContext

    def update(self):
        self.available = True
