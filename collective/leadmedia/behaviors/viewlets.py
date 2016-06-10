# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import ViewletBase
from .slideshow import ISlideshow
from plone.app.uuid.utils import uuidToCatalogBrain

class SlideshowViewlet(ViewletBase):
    """ A simple viewlet which renders slideshow """

    def slideshow(self, parent):
        """
        Creates a slideshow with the media from parent
        """

        uuid = self.context.UID()
        brain = uuidToCatalogBrain(uuid)
        lead_media = getattr(brain, 'leadMedia', None)

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
        
        if not lead_media:
            structure = """
                <div class="slick-slideshow empty" data-audio='' data-audio-duration=''>
                    <a href="%s?recursive=true" id='slide-get-content'></a>    
                </div>
                """%parentURL
        else:
            structure = """
                <div class="slick-slideshow" data-audio='' data-audio-duration=''>
                    <a href="%s?recursive=true" id='slide-get-content'></a>    
                    <script>
                        $('body').addClass('not-empty-slideshow');
                    </script>
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
