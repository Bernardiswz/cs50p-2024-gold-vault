import os


def main() -> None:
    print(os.path.islink("mylink"))
    print(os.path.islink("link_chain"))
    print(os.path.isfile("hardlink"))
    print(os.path.isfile(os.readlink("mylink")))

    with open("mylink", "r") as s_link:
        print(s_link.read())

    with open("hardlink","r") as r_link:
        print(r_link.read())

    with open("link_chain", "a") as link_chain:
        link_chain.write("Testing\n")

    with open("link_chain", "r") as link_chain:
        print(link_chain.read())


if __name__ == "__main__":
    main()
