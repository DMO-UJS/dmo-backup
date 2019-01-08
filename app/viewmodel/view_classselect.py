from app.utils.OntoOperUtils import OntoOperUtils

class view_classselect():
    def translate(self,libraryName,className):
        result={'className':'',
                'iri':'',
                'annotations':'',
                'parents':'',
                'relationships':[],
                'comments':[]}
        iri=OntoOperUtils.searchOwlClassIri(libraryName,className)
        parent=OntoOperUtils.searchOwlParent(libraryName,className)
        annotations=OntoOperUtils.searchOwlAnnotations(libraryName,className)
        result['className'],result['iri'],result['parents'],result['annotations'] = className,iri,\
                                                          parent,annotations
        return result