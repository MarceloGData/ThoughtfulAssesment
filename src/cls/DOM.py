from pattern import web

class DOM:
    def __init__(self, element=None, html=''):
        if(type(element) != type(None)):
            html = element.get_attribute('innerHTML')

        if(html == ''):
            raise Exception('DOM: Can\'t initialize DOM without html or element')

        self.__dom = web.Element(html)
    
    def get_tag_contents(self, tag):
        return [element.content for element in self.__dom.by_tag(tag)]

    def get_tags(self, tag):
        return [element for element in self.__dom.by_tag(tag)]