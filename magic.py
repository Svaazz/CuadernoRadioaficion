import datetime
import re
from docx import Document
import os

def print_table(data_list):
    print("{:<15} {:<11} {:<10} {:<10} {:<10} {:<11} {:<8} {:<15} {:<15} {:<15}".format(
        "UBICACIÓN", "FRECUENCIA", "HORA", "FECHA", "MODO", "INTENSIDAD", "SQUELCH", "R-DCS", "R-CTCS", "T-CTCS"))
    print("=" * 125)
    for data in data_list:
        location, frequency, time, date, mode, intensity, squelch, r_dcs, r_ctcs, t_ctcs = data
        formatted_data = "{:<15} {:<11.3f} {:<10} {:<10} {:<10} {:<11} {:<8} {:<15} {:<15} {:<15}".format(
            location, float(frequency), time, date, mode, int(intensity), int(squelch), r_dcs, r_ctcs, t_ctcs)
        print(formatted_data)

def print_table_to_docx(doc, data_list):
    table = doc.add_table(rows=1, cols=10)
    table.style = 'Table Grid'

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'UBICACIÓN'
    hdr_cells[1].text = 'FRECUENCIA'
    hdr_cells[2].text = 'HORA'
    hdr_cells[3].text = 'FECHA'
    hdr_cells[4].text = 'MODO'
    hdr_cells[5].text = 'INTENSIDAD'
    hdr_cells[6].text = 'SQUELCH'
    hdr_cells[7].text = 'R-DCS'
    hdr_cells[8].text = 'R-CTCS'
    hdr_cells[9].text = 'T-CTCS'

    for data in data_list:
        row_cells = table.add_row().cells
        row_cells[0].text = data[0]
        row_cells[1].text = f'{data[1]:.3f}'
        row_cells[2].text = data[2]
        row_cells[3].text = data[3]
        row_cells[4].text = data[4]
        row_cells[5].text = str(data[5])
        row_cells[6].text = str(data[6])
        row_cells[7].text = data[7]
        row_cells[8].text = data[8]
        row_cells[9].text = data[9]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_unique_frequencies(data_list):
    unique_frequencies = {}
    for data in data_list:
        frequency = data[1]
        if frequency not in unique_frequencies:
            unique_frequencies[frequency] = data
    return list(unique_frequencies.values())

def get_valid_frequency():
    while True:
        try:
            frequency_input = input("FRECUENCIA: ")
            if is_valid_frequency_input(frequency_input):
                frequency = float(frequency_input)
                if (136 <= frequency <= 174) or (400 <= frequency <= 520):
                    return frequency
                else:
                    print("Frecuencia fuera de rango. Introduce una frecuencia válida.")
            else:
                print("Formato de frecuencia incorrecto. Introduce una frecuencia con el formato adecuado (Ej: 142.300).")
        except ValueError:
            print("Entrada no válida. Introduce un número válido.")

def get_valid_location():
    location = input("UBICACIÓN (Dejar en blanco para NO DEFINIDA): ")
    return "NO DEFINIDA" if location == "" else location

def get_valid_time():
    while True:
        try:
            time_str = input("HORA (HH:MM): ")
            if time_str == "":
                return datetime.datetime.now().strftime("%H:%M")
            else:
                datetime.datetime.strptime(time_str, "%H:%M")
                return time_str
        except ValueError:
            print("Formato de hora incorrecto. Usa HH:MM o deja en blanco para usar la hora actual.")

def get_valid_date():
    while True:
        try:
            date_str = input("FECHA (YYYY-MM-DD): ")
            if date_str == "":
                return datetime.datetime.now().strftime("%Y-%m-%d")
            else:
                datetime.datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
        except ValueError:
            print("Formato de fecha incorrecto. Usa YYYY-MM-DD o deja en blanco para usar la fecha actual.")

def get_valid_intensity():
    while True:
        try:
            intensity = int(input("INTENSIDAD (0-4): "))
            if 0 <= intensity <= 4:
                return intensity
            else:
                print("Intensidad fuera de rango. Introduce un valor entre 0 y 4.")
        except ValueError:
            print("Entrada no válida. Introduce un número válido.")

def get_valid_squelch():
    squelch = None
    while True:
        try:
            squelch = int(input("SQUELCH (0-10): "))
            if 0 <= squelch <= 10:
                return squelch
            else:
                print("Squelch fuera de rango. Introduce un valor entre 0 y 10.")
        except ValueError:
            print("Entrada no válida. Introduce un número válido.")


def save_data(location, frequency, time, date, mode, intensity, squelch, r_dcs, r_ctcs, t_ctcs):
    with open("data.txt", "a") as file:
        file.write(f"{location}\t{frequency}\t{time}\t{date}\t{mode}\t{intensity}\t{squelch}\t{r_dcs}\t{r_ctcs}\t{t_ctcs}\n")

def is_valid_frequency_input(input_str):
    return re.match(r'^\d+\.\d{3}$', input_str)

def export_data_to_docx(data_list, filename):
    doc = Document()
    doc.add_heading('Primeros Contactos', level=1)
    unique_frequencies = get_unique_frequencies(data_list)
    print_table_to_docx(doc, unique_frequencies)

    doc.add_page_break()
    doc.add_heading('Todos los Datos', level=1)
    print_table_to_docx(doc, data_list)

    doc.save(filename)
    print(f"Archivo {filename} exportado exitosamente.")

def load_data_from_file():
    data_list = []
    with open("data.txt", "r") as file:
        for line in file:
            data = line.strip().split("\t")
            while len(data) < 10:
                data.append("0")  # Sustituir valores no definidos por ceros
            data_list.append((data[0], float(data[1]), data[2], data[3], data[4], int(data[5]), int(data[6]), data[7], data[8], data[9]))
    return data_list

def main():
    data_list = load_data_from_file()

    while True:
        print("\nCUADERNO DE RADIOAFICIONADO.")
        print("1. Ingresar una frecuencia")
        print("2. Ver los datos en pantalla")
        print("3. Exportar a DOCX")
        print("4. Salir")

        choice = input("Selecciona una opción (1/2/3/4): ")

        if choice == '1' or is_valid_frequency_input(choice):
            location = get_valid_location()
            if choice == '1':
                frequency = get_valid_frequency()
            else:
                frequency = choice
            time = get_valid_time()
            date = get_valid_date()
            mode = input("MODO (FM por defecto): ") or "FM"
            intensity = get_valid_intensity()
            squelch = get_valid_squelch()
            subtones = input("¿Deseas introducir subtonos? (Sí: S, No: N): ")
            if subtones.lower() == "s":
                r_dcs = input("R-DCS: ")
                r_ctcs = input("R-CTCS: ")
                t_ctcs = input("T-CTCS: ")
                data = (location, frequency, time, date, mode, intensity, squelch, r_dcs, r_ctcs, t_ctcs)
                data_list.append(data)
                save_data(location, frequency, time, date, mode, intensity, squelch, r_dcs, r_ctcs, t_ctcs)
                print("Datos almacenados exitosamente.")
            elif subtones.lower() == "n":
                data = (location, frequency, time, date, mode, intensity, squelch, "0", "0", "0")
                data_list.append(data)
                save_data(location, frequency, time, date, mode, intensity, squelch, "0", "0", "0")
                print("Datos almacenados exitosamente.")
            else:
                print("Opción no válida. Los datos no se almacenarán.")

        elif choice == '2':
            if len(data_list) == 0:
                print("No hay datos para mostrar.")
            else:
                while True:
                    clear_screen()
                    print("1. Ver todas las frecuencias")
                    print("2. Ver primeros contactos")
                    print("3. Volver atrás")
                    sub_choice = input("Selecciona una opción (1/2/3): ")

                    if sub_choice == '1':
                        print_table(data_list)
                        input("Presiona Enter para continuar...")
                        break
                    elif sub_choice == '2':
                        unique_frequencies = get_unique_frequencies(data_list)
                        print_table(unique_frequencies)
                        input("Presiona Enter para continuar...")
                        break
                    elif sub_choice == '3':
                        break
                    else:
                        print("Opción no válida. Por favor, selecciona una opción válida.")

        elif choice == '3':
            data_list = load_data_from_file()
            if len(data_list) == 0:
                print("No hay datos para exportar.")
            else:
                filename = input("Introduce el nombre del archivo (sin extensión .docx): ")
                filename += '.docx'
                export_data_to_docx(data_list, filename)
        elif choice == '4':
            return

if __name__ == "__main__":
    main()
