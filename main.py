import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("=== Wargames ver 1.0 ===")
        print("Simulates fights between AI and uses a genetic algorithm to learn them to fight")
        print("Usage : ")
        print("\t-display to display the result")
        print("\t-simulate to launch simulation")
    else:
        if sys.argv[1] == "-simulate":
            from simulation import DarwinSelection

            sel = DarwinSelection()
            sel.run()

        elif sys.argv[1] == "-display":
            from display import Display
            if len(sys.argv) < 3:
                print("Please specify file !")
                quit()
            dis = Display(sys.argv[2])
            dis.run()
        else:
            print("Usage : ")
            print("\t-display to display the result")
            print("\t-simulate to launch simulation")
