# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import ViewletBase
from .slideshow import ISlideshow

class SlideshowViewlet(ViewletBase):
    """ A simple viewlet which renders slideshow """

    def slideshow(self, parent):
        """
        Creates a slideshow with the media from parent
        """
        try:
            inContext = 'slideshow' in parent
        except:
            inContext = False
            parent = self.context
            pass

        if inContext:
            parentURL = parent['slideshow'].absolute_url()
        else:
            parentURL = parent.absolute_url()
        
        structure = """
            <div class="slick-slideshow" data-audio='' data-audio-duration=''>
            <a href="%s?recursive=true" id='slide-get-content'></a>    
            </div>
            """%parentURL

        return structure

    def slideshowInContext(self, parent, request):
        inContext = False
        if 'folder_contents' in request:
            return inContext
        try:
            if ISlideshow.providedBy(parent):
                return True

            inContext = 'slideshow' in parent
            return inContext
        except:
            return inContext

    def update(self):
        self.available = True
