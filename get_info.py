def get_info() -> list:
    """secret_key, admin_password, port, host"""

    info = ["secret_key", "admin_password", 5000, "localhost"]
    

    print("Welcome!")
    print()

    while True:
        print("Do you want to follow the default startup (1), use a custom one (2) or host in your local network (3)?\n\t|", end="")
    
        x = input()

        if x == "1":
            with open("default settings/secret_key.txt", "r") as d:
                info[0] = d.read()

            with open("default settings/admin_password.txt", "r") as d:
                info[1] = d.read()

            with open("default settings/port.txt", "r") as d:
                info[2] = int(d.read())

            print()
            print("Now using default settings.")
            print("Press enter to continue:")

            input()
            break

        elif x == "2":

            print()

            while True:
                print("Please enter your own secret key:\n\t|", end="")
                x = input()
                if x != "\n":
                    info[0] = x
                    print("Now using your own secret key.")
                    break

            print()

            while True:
                print("Please enter your own admin password:\n\t|", end="")
                x = input()
                if x != "\n":
                    info[1] = x
                    print("Now using your own admin password.")
                    break

            print()

            while True:
                print("Please enter your own port:\n\t|", end="")
                x = input()
                if x != "\n":
                    info[2] = int(x)
                    print("Now using your own port.")
                    break

            print()

            while True:
                print("Please enter your own ip to host on:\n\t|", end="")
                x = input()
                if x != "\n":
                    info[3] = x
                    print("Now using your own ip.")
                    break

            print()
            print("Now using default settings.")
            print("Press enter to continue:")

            input()
            break

        elif x == "3":
            with open("default settings/secret_key.txt", "r") as d:
                info[0] = d.read()

            with open("default settings/admin_password.txt", "r") as d:
                info[1] = d.read()

            with open("default settings/port.txt", "r") as d:
                info[2] = int(d.read())

            import socket

            info[3] = socket.gethostbyname(socket.getfqdn())
            print(info[3])

            del socket

            print()
            print("Now using default settings.")
            print("Press enter to continue:")

            input()
            break

    print("Starting...")
    return info