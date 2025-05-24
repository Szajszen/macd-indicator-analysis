import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Wczytanie danych z pliku CSV
dane = pd.read_csv('Dane_RGLD.csv')

print(dane.dtypes)

# Obliczenie MACD
# Obliczenie średniej ruchomej szybkiej (EMA12) i wolnej (EMA26)
ema12 = dane['Ostatnio'].rolling(window=12).mean()
ema26 = dane['Ostatnio'].rolling(window=26).mean()
macd = ema12 - ema26
signal = macd.rolling(window=9).mean()
dane['MACD'] = macd
dane['Signal'] = signal

# Narysowanie wykresu MACD i sygnału MACD z etykietami osi x
plt.plot(dane['Data'], dane['Signal'], label='Signal')
plt.plot(dane['Data'], dane['MACD'], label='MACD')
plt.legend()
plt.title('WSKAŹNIK MACD')
x_labels = [1, 1000] + list(range(250, len(dane), 250))
x_ticks = [0] + [i for i in range(1, len(dane)) if i in x_labels]
plt.xticks(x_labels, x_ticks)
plt.savefig('wykresMACD.png')
plt.show()

# Stworzenie wykresu liniowego
plt.plot(dane['Data'], dane['Ostatnio'])
plt.title('WYKRES WARTOŚCI AKCJI RGLD DLA OSTATNICH 1000 DNI')
plt.xlabel('Liczba Dni')
plt.ylabel('Wartość Akcji')
x_labels = [1, 1000] + list(range(250, len(dane), 250))
x_ticks = [0] + [i for i in range(1, len(dane)) if i in x_labels]
plt.xticks(x_labels, x_ticks)

# Wyświetlenie i zapis wykresu
plt.savefig('wykres.png')
plt.show()


kapital = 1000
pozycja = 0

# Inicjalizacja wartości trailing stop loss
tsl = 0
# Określenie procentowej wartości, o jaką będzie malał trailing stop loss
tsl_pct = 0.05

# Iteracja po każdym dniu w danych wejściowych
for i in range(len(dane)):

    # Aktualizacja wartości trailing stop loss, jeśli pozycja jest otwarta
    if pozycja > 0:
        obecna_cena= dane['Ostatnio'][i]
        nowe_tsl = max(obecna_cena * (1 - tsl_pct), tsl)
        tsl = nowe_tsl

    # Sprawdzenie czy MACD przekroczył sygnał w górę, Jeśli tak, kupujemy akcje za cały dostępny kapitał
    if dane['MACD'][i] > dane['Signal'][i] and pozycja == 0:
        pozycja = kapital / dane['Ostatnio'][i]
        kapital = 0
        tsl = dane['Ostatnio'][i] * (1 - tsl_pct)
        print("Kupiono akcje dnia", dane['Data'][i], "za cenę", dane['Ostatnio'][i])

    # Sprawdzenie czy cena przekroczyła wartość trailing stop loss, jeśli tak, sprzedajemy wszystkie posiadane akcje
    elif dane['Ostatnio'][i] < tsl and pozycja > 0:
        kapital = pozycja * tsl
        pozycja = 0
        tsl = 0
        print("Sprzedano akcje dnia", dane['Data'][i], "za cenę", tsl)

    # Sprawdzenie czy MACD przekroczył sygnał  w dół, Jeśli tak, sprzedajemy wszystkie posiadane akcje
    elif dane['MACD'][i] < dane['Signal'][i] and pozycja > 0:
        kapital = pozycja * dane['Ostatnio'][i]
        pozycja = 0
        tsl = 0
        print("Sprzedano akcje dnia", dane['Data'][i], "za cenę", dane['Ostatnio'][i])

# Sprawdzenie końcowego stanu pozycji i kapitału
if pozycja > 0:
    kapital = pozycja * dane['Ostatnio'][len(dane)-1]
    print("Uzyskano końcowy kapitał:", kapital)


"""
##MACD BEZ MODYFIKACJI
# Inicjalizacja kapitału początkowego i liczby akcji
capital = 1000
shares = 0

# Iteracja po kolejnych punktach czasowych
for i in range(1, len(dane)):
    # Jeśli wartość MACD przekracza wartość sygnału MACD, kupujemy akcje
    if macd[i] > signal[i] and macd[i-1] <= signal[i-1]:
        shares_to_buy = int(capital / dane['Ostatnio'][i])
        shares += shares_to_buy
        capital -= shares_to_buy * dane['Ostatnio'][i]
        print("Kupiono akcje dnia", dane['Data'][i], "za cenę", dane['Ostatnio'][i])

    # Jeśli wartość sygnału MACD przekracza wartość MACD, sprzedajemy akcje
    elif macd[i] < signal[i] and macd[i-1] >= signal[i-1]:
        capital += shares * dane['Ostatnio'][i]
        shares = 0
        print("Sprzedano akcje dnia", dane['Data'][i], "za cenę", dane['Ostatnio'][i])


# Obliczenie końcowego kapitału (uwzględniając wartość posiadanych akcji)
final_capital = capital + shares * dane['Ostatnio'][len(dane)-1]
print('Końcowy kapitał:', final_capital)
"""