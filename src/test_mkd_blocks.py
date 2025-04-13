import unittest

from mkd_blocks import *

class TestMKD_Blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_BT_heading(self):
        text = "# This is a heading"
        result = block_to_block_type(text)
        assert result == BlockType.HEADING, f"Expected BlockType.HEADING, got {result}"

    def test_bblock_to_BT_code(self):
        text = "```\nprint('hello world')\n```"
        result = block_to_block_type(text)
        assert result == BlockType.CODE, f"Expected BlockType.CODE, got {result}"

    def test_bblock_to_BT_quote(self):
        text = "> This is a quote\n> Another line of the quote"
        result = block_to_block_type(text)
        assert result == BlockType.QUOTE, f"Expected BlockType.QUOTE, got {result}"

    def test_bblock_to_BT_UL(self):
        text = "- Item 1\n- Item 2\n- Item 3"
        result = block_to_block_type(text)
        assert result == BlockType.UNORDERED_LIST, f"Expected BlockType.UNORDERED_LIST, got {result}"

    def test_bblock_to_BT_OL(self):
        text = "1. First item\n2. Second item\n3. Third item"
        result = block_to_block_type(text)
        assert result == BlockType.ORDERED_LIST, f"Expected BlockType.ORDERED_LIST, got {result}"

    def test_bblock_to_BT_PRG(self):
        text = "This is just a normal paragraph.\nIt spans multiple lines but has no other characteristics."
        result = block_to_block_type(text)
        assert result == BlockType.PARAGRAPH, f"Expected BlockType.PARAGRAPH, got {result}"

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

class TestExtractTitle(unittest.TestCase):
    # Test 1: Valid Markdown with a single H1
    def test_valid_h1(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    # Test 2: No H1 in Markdown
    def test_no_h1(self):
        markdown = "## Subheader\nSome content without an h1."
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No header1.")
        

if __name__ == "__main__":
    unittest.main()