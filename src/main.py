from html_node import HTMLNode
from text_node import TextNode, TextType


def main():
    node = TextNode("This is a text node", TextType.BOLD_TEXT, "https://boot.dev")
    print(node)

    p = HTMLNode(tag="p", value="Hello, world!")

    a = HTMLNode(tag="a", value="Boot.dev", props={"href": "https://www.boot.dev"})

    img = HTMLNode(
        tag="img",
        props={
            "src": "https://i.imgur.com/zgbZwup.jpeg",
            "alt": "profile picture",
            "class": "profile-img",
        },
    )

    print(p)
    print(a)
    print(img)


if __name__ == "__main__":
    main()
