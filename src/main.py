from textnode import TextNode, TextType


def main():
    text_node = TextNode("This is a node", TextType.BOLD, "https//www.boot.dev")
    print(text_node)

if __name__ == "__main__":
    main()
