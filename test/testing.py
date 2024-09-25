import sys


# ejecuta el pipeline del testing
def test(scenario):
    pass

if __name__ == "__main__":

    scenario = 0
    try:
        scenario = sys.argv[1]
    except IndexError:
        print("ERROR: Ingrese un escenario --> python3 testing.py <escenario>")
        exit()

    test(scenario)
    