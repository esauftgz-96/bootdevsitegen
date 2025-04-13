class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children if children else []
        self.props = props if props else {}
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if not self.props:
            return ""
        output = []
        for element in self.props:
            output.append(f' {element}="{self.props[element]}"') 
        return "".join(output)
    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"
    def __eq__(self,HTMLNode2):
        if self.tag == HTMLNode2.tag and self.value == HTMLNode2.value and self.children == HTMLNode2.children and self.props == HTMLNode2.props:
            return True
        return False
    
class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag,value,children=[],props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf-value cannot be none.")
        if self.tag is None:
            return self.value
        if self.props:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        return f'<{self.tag}>{self.value}</{self.tag}>'
    
class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag,value=None,children=children,props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent-tag cannot be none.")
        if self.children is None:
            raise ValueError("Parent-children cannot be none.")
        
        output = f'<{self.tag}{self.props_to_html()}>'
        for child in self.children:
            output += child.to_html()
        output += f"</{self.tag}>"
        return output




        
        
        