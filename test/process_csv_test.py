# TEST: Correr este archivo con `python3 process_csv_test.py` y deberia dar successful para los 2 chequeos
import filecmp
import os

def process_csv(can_csv) -> None:
    # TOOD: Procesar can.csv y guardarlo en los archivos bms.csv and kelly.csv siguiendo las formulas de traduccion de
    # orion.OrionParse.on_message_received y kelly.parsed_message_kelly.
    # Por cada fila leida, se deberia guardar el estado completo del componente, reemplazando los datos
    # no procesados por el mensaje por N.
    pass

def check_file(filename):
    print("Checking "+filename+"...")
    if filecmp.cmp("extractor\\" + filename, "test\\" + "expected_"+filename):
        print("Test successful!")
    else:
        print("Test unsuccessful: "+filename+" and expected_"+filename+" are not the same")

if __name__ == "__main__":
    process_csv("can.csv")
    check_file("bms.csv")
    check_file("kelly.csv")
