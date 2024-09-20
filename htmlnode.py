
class HTMLNode:
	def __init__(self, tag = None, value = None, children = None, props = None):
		self.tag = tag
                self.value = value
                self.children = children
                self.props = props

        def to_html(self):
                raise NotImplementedError()
	
	def props_to_html(self):
		if not self.props:
			return ""

	formatted_props = []
	for key, value in self.props.items():
		formatted_props += [f'{key}="{value}"']
	return " " + " ".join(formatted_props)

	def __repr__(self):
		attributes = []

		if self.tag is not None:
			attributes.append(f"tag='{self.tag}'")
		if self.value is not None:
			value = self.value if len(self.value) <= 20 else self.value[:20] + "..."
			attributes.append(f"value='{value}'")
		if self.children is not None:
			if len(self.children) > 2:
				children_repr = f"[{len(self.children)} items]"
			else:
				children_repr = repr(self.children)
			attributes.append(f"children={children_repr}")
		if self.props is not None:
			attributes.append(f"props='{self.props}'")
		return f"HTMLNode({', '.join(attributes)})"


class LeafNode(HTMLNode):
	def __init__(self, value, tag=None, props=None):
		super().__init__(tag=tag, value=value, children=None, props=props)

	def to_html(self):
		if self.value is None:
			raise ValueError("LeafNode must have a value")
		if self.tag is None:
			return self.value

		attrs = ""
		if self.props is not None:
			attrs = ' '.join([f'{key}="{value}"' for key, value in self.props.items()])
		return f"<{self.tag}{attrs}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
        def __init__(self, children, tag = None, props = None):
                super().__init__(children = children, tag=tag, props=props)

	def to_html(self):
		if self.tag is None:
			raise ValueError("ParentNode must have a tag")
		if len(self.children) == 0:
			raise ValueError("ParentNode must have children")

		children_html = ''.join(child.to_html() for child in self.children)

		return f"<{self.tag}>{children_html}</{self.tag}>"
