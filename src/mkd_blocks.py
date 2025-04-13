from enum import Enum
import re

from htmlnode import *
from textnode import *
from nodesplit import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    doc = markdown.split("\n\n")
    result = []
    for element in doc:
        if element != "":
            result.append(element.strip())
    return result

def block_to_block_type(text):
    if bool(re.match(r"#{1,6} ",text.split("\n")[0])) :
        return BlockType.HEADING
    elif text.split("\n")[0] == "```" and text.split("\n")[-1] == "```" :
        return BlockType.CODE
    else:
        splitlines = text.split("\n")
        if all(map(lambda x: x.startswith(">"),splitlines)):
            return BlockType.QUOTE
        elif all(map(lambda x: x.startswith("- "),splitlines)):
            return BlockType.UNORDERED_LIST
        elif all(line.startswith(f"{i + 1}. ") for i, line in enumerate(splitlines)):
            return BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH
        
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

    # if blocktype == BlockType.QUOTE:
    #     output = block.split("\n")
    #     n_output = []
    #     for element in output:
    #         if element.lstrip(">") != "":
    #             n_output.append(element.lstrip(">"))
    #         else:
    #             continue
    #     return f"<blockquote>{" ".join(n_output)}</blockquote>"      

    # if blocktype == BlockType.UNORDERED_LIST:
    #     output = block.split("\n")
    #     n_output = []
    #     for element in output:
    #         n_output.append(f"<li>{element.lstrip("- ")}</li>")
    #     return f"<ul>{"".join(n_output)}</ul>"

    # if blocktype == BlockType.ORDERED_LIST:
    #     output = block.split("\n")
    #     n_output = []
    #     for i, element in enumerate(output,start = 1):
    #         n_output.append(f"<li>{element[len(f"{i}. ")::]}</li>")
    #     return f"<ol>{"".join(n_output)}</ol>"
        
    # if blocktype == BlockType.CODE:
    #     return f"<pre><code>{block.lstrip("```").rstrip("```")}</code></pre>"

    # if blocktype == BlockType.HEADING:
    #     return f"<h{block.split(" ",1)[0].count("#")}>{block.split(" ",1)[1]}</h{block.split(" ",1)[0].count("#")}>"

    # if blocktype == BlockType.PARAGRAPH:
    #     return f"<p>{block}</p>"

def extract_title(markdown):
    h1_lines = []
    for line in markdown.split("\n\n"):
        if line.startswith("# "):
            h1_lines.append(line[2:])
    if not h1_lines:
        raise Exception("No header1.")
    return h1_lines[0]