import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        from simulation import DarwinSelection

        sel = DarwinSelection()
        sel.run()

    elif sys.argv[1] == "-display":
        from display import Display

        dis = Display()
        dis.run()
