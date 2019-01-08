import json


class OtherUtils:

    @classmethod
    def decorateToJson(cls, layerList):
        for firstDir in layerList:
            for otherDir in layerList:
                for i in range(len(firstDir['children'])):
                    if firstDir['children'][i] == otherDir['name']:
                        firstDir['children'][i] = otherDir
        return json.dumps(layerList[0],ensure_ascii=False)