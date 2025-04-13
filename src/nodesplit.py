from textnode import *
from regex import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        blocks = old_node.text.split(delimiter)
        if len(blocks)%2 == 0:
            raise Exception("Delimiter not properly formatted")
        for i in range(len(blocks)):
            if blocks[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(blocks[i],TextType.TEXT))
            else:
                new_nodes.append(TextNode(blocks[i],text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        x = extract_markdown_images(old_node.text)
        if not x:
            new_nodes.append(old_node)
            continue
        else:
            rawtext = old_node.text
            for image1,link1 in x:
                sections = rawtext.split(f"![{image1}]({link1})",1)
                if len(sections) < 2:
                    continue
                elif sections[0] == "":
                    new_nodes.append(TextNode(image1,TextType.IMAGE,link1))
                    rawtext = sections[1]
                else:
                    new_nodes.append(TextNode(sections[0],TextType.TEXT))
                    new_nodes.append(TextNode(image1,TextType.IMAGE,link1))
                    rawtext = sections[1]
            if rawtext != "":
                new_nodes.append(TextNode(rawtext,TextType.TEXT))
            elif rawtext == "":
                continue             
    return new_nodes

                    
def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        x = extract_markdown_links(old_node.text)
        if not x:
            new_nodes.append(old_node)
            continue
        else:
            rawtext = old_node.text
            for hyper1,link1 in x:
                sections = rawtext.split(f"[{hyper1}]({link1})",1)
                if len(sections) < 2:
                    continue
                elif sections[0] == "":
                    new_nodes.append(TextNode(hyper1,TextType.LINK,link1))
                    rawtext = sections[1]
                else:
                    new_nodes.append(TextNode(sections[0],TextType.TEXT))
                    new_nodes.append(TextNode(hyper1,TextType.LINK,link1))
                    rawtext = sections[1]
            if rawtext != "":
                new_nodes.append(TextNode(rawtext,TextType.TEXT))
            elif rawtext == "":
                continue             
    return new_nodes

def text_to_textnodes(text):
    rawtext = [TextNode(text,TextType.TEXT)]
    delim_tt=(("**",TextType.BOLD),("_",TextType.ITALIC),("`",TextType.CODE))
    node = split_nodes_image(split_nodes_link(rawtext))
    for delim,tt in delim_tt:
        node = split_nodes_delimiter(node, delim, tt)
    return node