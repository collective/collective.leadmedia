# Handling Events
from zope.annotation.interfaces import IAnnotations
from plone.multilingual.interfaces import ILanguage

def reindexMedia(object, event):
    """
        Reindexes leadmedia catalog indexes
    """

    if object.id != "whatson" and object.id != 'slideshow':
        #print "Reindexing %s"%object.id
        object.reindexObject()
        object.reindexObject(idxs=["hasMedia"])
        object.reindexObject(idxs=["leadMedia"])

        if hasattr(object.getParentNode(), "meta_type"):
            if object.getParentNode().meta_type == "Dexterity Container" and object.getParentNode().portal_type != "Folder":
                reindexMedia(object.getParentNode(), event)
    
    elif object.id == 'slideshow':
        if hasattr(object.getParentNode(), "meta_type"):
            if object.getParentNode().meta_type == "Dexterity Container" and object.getParentNode().portal_type != "Folder":
                reindexMedia(object.getParentNode(), event)

def objectAddedEvent(object, event):
    
    newparent_lang = ILanguage(event.newParent).get_language()

    if object.portal_type != "Folder":
        if 'slideshow' not in object.objectIds():
            print "Add slideshow folder."

            object.invokeFactory(
                type_name="Folder",
                id=u'slideshow',
                title='slideshow',
            )

            folder = object['slideshow']

            ILanguage(folder).set_language(newparent_lang)

            try:
              folder.portal_workflow.doActionFor(folder, "publish", comment="Slideshow content automatically published")
              object.reindexObject()
            except:
              pass
    