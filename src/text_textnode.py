import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_none(self):
        node = TextNode( "text", "regular" , None)
        node2 = TextNode( "text","regular" , None)
        self.assertEqual(node, node2)

     def test_dif(self):
        node = TextNode( "text", "regular" , None)
        node2 = TextNode( "different text","italics" , None)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
