import re
from slownik_mas import slownik_mas
import tkinter as tk


def sprawdz_znaki(sklad: str) -> bool:
    return bool(re.search(r'[^a-zA-Z\d\.()]', sklad))  #dopuszczalne znaki - wielkie i małe litery, kropki, nawiasy okragle


def podziel_sklad(sklad: str) -> list[str]:
    
    lista = re.findall(r'[A-Z][a-z]*|[\d.]+|[()]', sklad)  #dzieli na liste wielkie litery z malymi opcjonalnie, cyfry z kropkami, nawiasy)
    #print(lista)
    result = []
    poprzedni_alpha = False
    poprzedni_nawias_zamykajacy = False

    
    for el in lista:          
        if el.isalpha():
            if poprzedni_alpha or poprzedni_nawias_zamykajacy:
                result.append('1')
            result.append(el)
            poprzedni_alpha = True
            poprzedni_nawias_zamykajacy = False
        elif el == ')':
            if poprzedni_alpha or poprzedni_nawias_zamykajacy:
                result.append('1')
            result.append(el)
            poprzedni_alpha = False
            poprzedni_nawias_zamykajacy = True
        elif el == '(':
            if poprzedni_alpha or poprzedni_nawias_zamykajacy:
                result.append('1')
            result.append(el)
            poprzedni_alpha = False
            poprzedni_nawias_zamykajacy = False
        else:
            result.append(el)
            poprzedni_alpha = False
            poprzedni_nawias_zamykajacy = False
    
    if result[-1].isalpha() or result[-1] == ')':  #na koncu doda 1, jesli nie ma liczby
        result.append('1')  

    print(result)
    return result

def analiza_nawiasow(lista: list[str]) -> list[str]:
    wewnatrz_nawiasu = False
    result = []
    temp_list = []
    mnoznik=1

    i=0
    while i < len(lista):
        element = lista[i]

        if element =='(':
            if wewnatrz_nawiasu:
                return None
            wewnatrz_nawiasu = True
            i+=1
            continue
        elif element == ')':
            if not wewnatrz_nawiasu:
                return None
            wewnatrz_nawiasu = False
            mnoznik = float(lista[i+1])
            i+=1 #nie zapisujemy mnoznika
            for temp_el in temp_list:
                if not temp_el.isalpha():
                    result.append(str(float(temp_el) * mnoznik))
                else:
                    result.append(temp_el)
            temp_list = []
            i+=1

            continue
        elif wewnatrz_nawiasu:
            temp_list.append(element)
        else:
            result.append(element)
        i+=1

    if wewnatrz_nawiasu:
        #print('nawias')
        return None
    
    return result
                  



def czy_nie_pierwiastki(lista: list[str]) -> bool:
    for el in lista[::2]:
        if el not in slownik_mas:
            return True
    return False


def licz_mase(lista: list[str]) -> float:
    masa = 0
    for i in range(0, len(lista), 2):
        masa += slownik_mas[lista[i]] * float(lista[i + 1])
    return masa


class MMCalculator:
    def __init__(self):
        self.label1 = None
        self.label2 = None
        self.button = None
        self.button2 = None
        self.entry1 = None
        self.window = tk.Tk()
        self.window.title('Molar mass calculator')
        self.window.iconbitmap('./czasteczka.ico')
        self.window.geometry("300x200")

        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self):

        self.label1 = tk.Label(self.window, text="Enter the chemical formula\n e.g. Al(NO3)3", font=('Arial', 12))
        self.label1.grid(row=0, column=0, columnspan=2, pady=(10, 0))

        self.entry1 = tk.Entry(self.window, font=('Arial', 12))
        self.entry1.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

        self.button = tk.Button(text="CALCULATE", font=('Arial', 15))
        self.button.grid(row=2, column=0, padx=(10, 5), pady=10, sticky='ew')
        self.button.bind("<Button-1>", self.button_press)

        self.button2 = tk.Button(text="CLEAR", font=('Arial', 15))
        self.button2.grid(row=2, column=1, padx=(5, 10), pady=10, sticky='ew')
        self.button2.bind("<Button-1>", self.button2_press)

        self.label2 = tk.Label(self.window, text="", font=('Arial', 12))
        self.label2.grid(row=3, column=0, columnspan=2, pady=(0, 10))

   
    def nierozpoznana_formula(self):
        self.label2.config(text="unrecognisable sequence of characters", font=('Arial', 10), fg='red')

    def button_press(self, _):
        sklad = self.entry1.get()
        if sprawdz_znaki(sklad):
            self.nierozpoznana_formula()
            return
        lista_elementow_naw = podziel_sklad(sklad)
        lista_elementow = analiza_nawiasow(lista_elementow_naw)
        if lista_elementow == None:
            self.nierozpoznana_formula()
            return
        if czy_nie_pierwiastki(lista_elementow):
            self.nierozpoznana_formula()
            return
        self.label2.config(text=f" molar mass {licz_mase(lista_elementow):.3f} g/mol", font=('Arial', 12),
                           fg='black')

    def button2_press(self, _):
        self.entry1.delete(0, tk.END)
        self.label2.config(text="")


if __name__ == '__main__':
    MMCalculator()
