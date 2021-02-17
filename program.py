######################################################################################################
# CT60A0202 Ohjelmoinnin ja data-analytiikan perusteet
# Tekijä: Kalle Liljeström
# Opiskelijanumero: 
# Päivämäärä: 19.11.2018
# Yhteistyö ja lähteet, nimi ja yhteistyön muoto: Python ohjelmointiopas ja luentomateriaali
# HUOM! KAIKKI KURSSIN TEHTÄVÄT OVAT HENKILÖKOHTAISIA!
######################################################################################################
# program.py ohjelman tarkoituksena on käsitellä dataa LUT:n aurinkopaneelien sähköntuotannosta ja
# tallettaa se csv-tiedostoon. Tulokset voidaan visualisoida Excelin avulla.
# Ohjelma vaatii toimiakseen "HTLib" aliohjelmakirjaston.
######################################################################################################

import datetime
import sys
try:
    import HTLib  # Aliohjelmakirjasto, lopetetaan, jos ei löydy.
except:
    print("Aliohjelmakirjastoa \"HTLib\" ei löytynyt, lopetetaan.")
    sys.exit(0)

def paaohjelma():
    lista = []
    paivatuotanto = []

    # Silmukka kysyy käyttäjältä, minkä toiminnon tämä haluaa ja kutsuu oikeaa aliohjelmaa valinnan
    # perusteella. Lopettaa arvolla 0.
    while True:
        valinta = HTLib.valikko()
        if valinta  == 1:
            lista = HTLib.lue_sahkontuotantotiedot(lista)
        elif valinta  == 2:
            paivatuotanto = HTLib.analysoi_paivatuotanto(lista)
        elif valinta  == 3:
            HTLib.tallenna_paivatuotanto(paivatuotanto)
        elif valinta  == 0:
            print("Kiitos ohjelman käytöstä.")
            break
        else:
            print("Syöte ei kelpaa!\n")

    lista.clear()
    paivatuotanto.clear()
    
######################################################################################################
paaohjelma()  # Pääohjelman ajo

######################################################################################################
#eof
