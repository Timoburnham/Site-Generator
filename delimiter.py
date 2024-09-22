from htmlnodes import TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []
	for node in old_nodes:
		if node.text_type == "text":
			parts = node.content.split(delimiter)
			for index, part in enumerate(parts):
				if index % 2 == 1:
					new_nodes.append(TextNode(part, text_type))
				else:
					new_nodes.append(TextNode(part, "text"))

			if len(parts) % 2 == 0:
				raise Exception("Unmatched delimiter found in text node")

		else:
			new_nodes.append(node)

	return new_nodes


