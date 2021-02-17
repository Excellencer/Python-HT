################################################################################################################
# CT60A0202 Ohjelmoinnin ja data-analytiikan perusteet
# Tekijä: Kalle Liljeström
# Opiskelijanumero: 
# Päivämäärä: 19.11.2018
# Yhteistyö ja lähteet, nimi ja yhteistyön muoto: Python ohjelmointiopas ja luentomateriaali
# HUOM! KAIKKI KURSSIN TEHTÄVÄT OVAT HENKILÖKOHTAISIA!
################################################################################################################
# HTLib.py on aliohjelmakirjasto program.py tiedoston sisältämälle pääohjelmalle.
# Sisältää aliohjelmat: valikko(), lue_sahkontuotantotiedot(), analysoi_paivatuotanto() ja
# tallenna_paivatuotanto().
################################################################################################################

import datetime
import sys

# tuotanto-luokka, jonka olioilla attribuutit päivämäärä ja aika sekä sähköntuotto.
class tuotanto:
    pvm = ""
    tuotto = 0
    
# valikko() aliohjelman tarkoituksena on luoda valikkopohjainen rakenne ohjelmalle: käyttäjä voi valita
# minkä toiminnon haluaa tehdä seuraavaksi syöttämällä toiminnon numeron, tai lopettaa ohjelman.
def valikko():
    print("Anna haluamasi toiminnon numero seuraavasta valikosta:")
    print("1) Lue sähköntuotantotiedot")
    print("2) Analysoi päivätuotanto")
    print("3) Tallenna päivätuotanto")
    print("0) Lopeta")
    try:
        valinta = int(input("Valintasi: "))
    except ValueError:
        print("Tapahtui virhe, lopetetaan.")
        sys.exit(0)
    return valinta

# lue_sahkontuotantotiedot() saa parametreinaan listan ja tallettaa siihen csv-tiedostossa olevan datan olioina. 
def lue_sahkontuotantotiedot(lista):    
    lista.clear()
    rivit = 0  
    analysoitavat_rivit = 0

    # Kysytään käyttäjältä syötteenä csv-tiedoston nimeä ja analysoitavaa vuotta.
    tiedosto_luku = input("Anna luettavan tiedoston nimi: ")
    vuosi = input("Anna analysoitava vuosi: ")

    # Yritetään avata syötteenä annettu tiedoston nimi, jos ei onnistu, lopetetaan ohjelma.
    try:
        with open(tiedosto_luku, "r", encoding="utf-8") as csv_luku:
            csv_luku.readline()  # Hypätään tiedoston otsikkorivin yli.
            
            # Silmukka käy tiedoston rivit läpi yksi kerrallaan ja ottaa halutun vuoden ajalta olevien rivien
            # päivämäärän ja ajan sekä aurinkopaneelien yhteissähköntuotannon ylös listaan olioina.
            while True:
                tuotto = 0
                rivi = csv_luku.readline()
                
                if rivi == "":
                    break
                else:
                    rivi = rivi[:-2].split(";")  # Jaetaan rivi osiin.
                    paivays = datetime.datetime.strptime(rivi[0], "%Y-%m-%d %H:%M:%S")
                    rivit +=1
                    
                    if str(paivays.year) == vuosi:  # Tarkistetaan, että data halutulta vuodelta.
                        analysoitavat_rivit += 1
                        
                        for i in range(1,8):
                            tuotto = tuotto + float(rivi[i])  # Lasketaan aurinkopaneelien tuotot yhteen.
    
                        if tuotto < 0: 
                           tuotto = 0  # Negatiiviset tulokset muutetaan nolliksi.
                           
                        x = tuotanto()
                        x.pvm = paivays
                        x.tuotto = tuotto
                        lista.append(x)
                        
        # Tulostaa montako riviä tiedostossa oli, montako otettiin analysoitavaksi ja miltä aikaväliltä
        # dataa analysoitiin.
        print("Tiedosto '" + tiedosto_luku + "' luettu,", rivit + 1, "riviä,", \
            analysoitavat_rivit, "otettu analysoitavaksi.")
        print("Analysoidaan", datetime.datetime.strftime(lista[0].pvm, "%d.%m.%Y %H:%M"), "ja",\
            datetime.datetime.strftime(lista[-1].pvm, "%d.%m.%Y %H:%M"), "välistä dataa.\n")
        return lista
    
    except OSError:
        print("Tiedoston '" + tiedosto_luku + "' lukeminen epäonnistui, ei löydy, lopetetaan.")
        sys.exit(0)
    except:
        print("Tapahtui virhe, lopetetaan.")
        sys.exit(0)

# analysoi_paivatuotanto aliohjelma tekee annetun listan perusteella toisen listan, jossa sähköntuotanto on
# päivien välein.
def analysoi_paivatuotanto(lista):
    try:
        paivatuotanto = []
        paivays = lista[0].pvm  # Päivämäärä alussa.
        kokooja = 0

        # Käydään lista läpi summaten rivien sähköntuottoja, kunnes päivä vaihtuu -> talletetaan 
        # toiseen listaan ja nollataan kokooja.
        for x in lista: 
            if x.pvm.day == paivays.day:
                kokooja += x.tuotto
            
            else:
                y = tuotanto()
                y.pvm = paivays
                y.tuotto = kokooja
                paivatuotanto.append(y)
            
                paivays = x.pvm
                kokooja = 0
                kokooja += x.tuotto
                
        # Lisätään vielä viimeinen päivä, joka jää silmukan ulkopuolelle.
        y = tuotanto()        
        y.pvm = paivays
        y.tuotto = kokooja
        paivatuotanto.append(y)

        print("Päivätuotanto analysoitu.\n")
        
        return paivatuotanto
    
    except:
        print("Tapahtui virhe, lopetetaan.")
        sys.exit(0)

# tallenna_paivatuotanto aliohjelma tallettaa annetun listan csv-tiedostona ja tulostaa sekä päivittäisen
# että kumulatiivisen sähköntuotannon.
def tallenna_paivatuotanto(paivatuotanto):
    try:
        vuosi = str(paivatuotanto[0].pvm.year)  # Selvittää listan ensimmäisestä alkiosta vuoden.
        yht = 0
        tiedosto_kirjoitus = "tulosPaiva" + vuosi + ".csv"  # Tiedoston nimi
        
        with open(tiedosto_kirjoitus, "w") as csv_kirjoitus:
            csv_kirjoitus.write("Päivittäinen sähköntuotanto:\n;"+ vuosi + "\n")  # Otsikko
            
            # Päivittäisen sähköntuotannon tulostus
            for y in paivatuotanto:
                csv_kirjoitus.write(datetime.datetime.strftime(y.pvm, "%d.%m.%Y") + ";" + str(int(y.tuotto)) + "\n")

            # Kumulatiivisen sähköntuotannon tulostus
            csv_kirjoitus.write("\n\nKumulatiivinen päivittäinen sähköntuotanto:\n;" + vuosi + "\n") # Otsikko
            for y in paivatuotanto:
                yht += y.tuotto
                csv_kirjoitus.write(datetime.datetime.strftime(y.pvm, "%d.%m.%Y") + ";" + str(int(yht)) + "\n")
            csv_kirjoitus.write("\n\n")
                    
        print("Päivätuotanto tallennettu tiedostoon '" + tiedosto_kirjoitus + "'.\n")
        
    except OSError:
        print("Tiedostoon '" + tiedosto_kirjoitus + "' kirjoitus epäonnistui, lopetetaan.")
        sys.exit(0)
    except:
        print("Tapahtui virhe, lopetetaan.")
        sys.exit(0)
        
######################################################################################################
#eof
