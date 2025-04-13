import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1","click me!",["ul","ol"],{"href": "https://www.google.com"})
        node2 = HTMLNode("h1","click me!",["ul","ol"],{"href": "https://www.google.com"})
        self.assertEqual(node, node2)
    def test_neq(self):
        node = HTMLNode("h1","click me!",[],{"href": "https://www.google.com"})
        node2 = HTMLNode("h1","click me!",["ul","ol"],{"href": "https://www.google.com"})
        self.assertNotEqual(node, node2)

    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_p(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_leaf_to_html_nt(self):
        node = LeafNode(None, "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "Click me!")
    
    ## use assertRaises() to check for errors
    def test_leaf_to_html_ve(self):
        node = LeafNode("a", None, {"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    ###stress test from boots
    def test_complex_structure(self):
        # Leaf nodes
        leaf1 = LeafNode("b", "bold", {"class": "bold"})
        leaf2 = LeafNode(None, "normal")
        leaf3 = LeafNode("i", "italic")
    
        # Nested parent
        inner_parent = ParentNode("div", [leaf1, leaf2], {"id": "inner"})
        
        # Top parent with a mix of leaf and parent children
        outer_parent = ParentNode("section", [
            inner_parent,
            leaf3,
            ParentNode("p", [LeafNode("span", "Nested")], {"class": "para"})
        ], {"id": "outer"})
        
        expected = (
            '<section id="outer">'
            '<div id="inner"><b class="bold">Bold</b>Plain</div>'
            '<i>Italic</i>'
            '<p class="para"><span>Nested</span></p>'
            '</section>'
        )


if __name__ == "__main__":
    unittest.main()