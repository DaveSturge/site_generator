from textnode import TextNode, TextType

def main():

    text = "This is a test"
    type = TextType.BOLD
    
    text_node = TextNode(text, type)

    print(text_node)

main()