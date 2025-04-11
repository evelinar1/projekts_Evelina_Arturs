from datetime import datetime 
from datetime import timedelta
import random
class Klientu_saraksts():
    def __init__(self): #inicializē vārdnīcu klientu_saraksts
        self.klientu_saraksts={}
    def pierakstit(self): #pieraksta klientu abonementu sarakstam
        klients = input("Ievadiet klienta vārdu (Vārds Uzvārds): ")
        while True: #izmantotjot random izveido skaitli starp 10000 un 99999 un salīdzina vai tāds jau nav vārdnīcā
            kods = random.randint(10000,99999)
            if kods not in self.klientu_saraksts.items():
                break
            else:
                continue
        termins = datetime.now() #paņem tagadējo datumu
        termins = termins + timedelta(days=365) #pievieno datumam 1 gadu
        termins = termins.strftime("%d-%m-%Y") #pārveido datumu uz pareizo formātu
        self.klientu_saraksts.update({kods:[klients,termins]}) #pievieno klientu kā atslēgu un [kods,termins] ka vērtību
        print(f"{klients} ir pierakstīts abonementam\nkods: {kods}\ntermins līdz: {termins}")
        return kods
    def saglabat_faila(self): #saglabā failā
        with open('Klientu_saraksts.txt','w',encoding='utf8') as fails:
            for klients, vertiba in self.klientu_saraksts.items():
                fails.write(f'{klients}:{vertiba[0]},{vertiba[1]}\n')
    def panem_no(self):#nolasa no faila
        try:#lai neizmet error ja nav faila
            with open('Klientu_saraksts.txt','r',encoding='utf8') as fails:
                for rinda in fails:
                    kods,vertiba = rinda.strip().split(':')
                    klients,termins = vertiba.strip().split(',')
                    self.klientu_saraksts[kods]=[klients,termins]
        except FileNotFoundError:
            pass

# Klase "Parbaude", kas manto no klases "Klientu_saraksts"
class Parbaude(Klientu_saraksts):
    def __init__(self,klientu_saraksts):
        self.klientu_saraksts=klientu_saraksts
        

# FUNKCIJA PARBAUDIT - Pārbauda klienta abonementa statusu, ja abonements beidzies ir iespēja to pagarināt
    def parbaudit(self):
        
        while True:
                try:
                    kods = input("Ievadiet klienta 5 ciparu kodu: ")
                    num = int(kods)
                    if not len(kods) == 5:
                        print("Ievadiet 5 ciparu garu kodu!")
                        continue
                
                        # Pievienot koda garuma pārbaudi
                    if kods not in self.klientu_saraksts: # Pārbauda vai klients eksistē
                        print('Klients nav pierakstīts.')
                        while True:
                            turpinat = input("Vai vēlieties pierakstīt klientu? (J/N): ") 
                            if turpinat == 'J': # Ja neeksistējošs klients vēlas iegūt abonementu:
                                self.pierakstit()
                                self.saglabat_faila()
                                break
                            elif turpinat == 'N': # Nevēlas iegūt abonementu:
                                break
                            else:
                                print("Ievadiet atbilstošu vērtību!") # Ierakstīta neatbilstoša vērtība
                            continue
                        break
                                
                    else: # Ja klients ir sarakstā
                        termins = self.klientu_saraksts[kods][1]
                        formats = "%d-%m-%Y"
                        termins = datetime.strptime(termins, formats)
                        if termins <= datetime.now():
                                # Paziņo, ka abonements beidzies, dod opciju pagarināt to
                            atjaunot = input(f"{self.klientu_saraksts[kods][0]} abonements ir beidzies.\nVai vēlaties atjaunot abonementu? (J/N):")
                            if atjaunot == 'J': # Abonementa pagarināšana
                                    
                                print(f"Klienta {self.klientu_saraksts[kods][0]} abonements tika pagarināts līdz {self.klientu_saraksts[kods][1]}.")
                            elif atjaunot == 'N': # Abonements netiek pagarināts - programma beidzas
                                print("Programma Beidzas")
                                break
                        else:
                            print("Lietotājam ir abonements.")
                            break
                except ValueError: # Kļūdu pārbaude
                    print("Ievadiet atbilstošu vērtību!")
                    continue

#FUNKCIJA ATJAUNOT - atjauno eksitējoša klienta abonementu, ja klients neeksiste, dod iespēju pievienot un iedod jaunā klienta kodu
    def atjaunot(self):
        print(self.klientu_saraksts)
        while True:
            try:
                kods = input("Ievadiet klienta 5 ciparu kodu: ")
                if kods not in self.klientu_saraksts:
                    turpinat = input("Klientam nav amonements.\nVai vēlajties pierakstīties abonementam? (J/N): ") # Ja klientam nav abonements, dod iespēju to iegūr 
                    if turpinat == 'J':
                        kods = self.pierakstit()
                        self.saglabat_faila()
                        # Parāda, ka jaunais klients ir ieguvis abonementu, parāda tā derīguma termiņu un klienta kodu
                        print(f"Jaunais klients {self.klientu_saraksts[kods][0]} ir pievienots! Abonementa termiņš: {self.klientu_saraksts[kods][1]}, kods: {kods}")
                        break
                    elif turpinat == 'N': # Ja neturpina, programma beidzas
                        break
                else: 
                    termins = datetime.now() #paņem tagadējo datumu
                    termins = termins + timedelta(days=365) #pievieno datumam 1 gadu
                    termins = termins.strftime("%d-%m-%Y") #pārveido datumu uz pareizo formātu
                    self.klientu_saraksts.update({kods:[self.klientu_saraksts[kods][0],termins]}) #pievieno klientu kā atslēgu un [kods,termins] ka vērtību
                    self.saglabat_faila()
                    print(f"Klienta {self.klientu_saraksts[kods][0]} abonements ir atjaunots, derīguma termiņš: {self.klientu_saraksts[kods][1]}.") # Pagarina klienta abonementu
                    break
            except ValueError:
                print("Ievadiet atbilstošu vērtību!")
                continue

#FUNKCIJA ATCELT - atceļ eksistējoša klienta abonementu
    def atcelt(self):
        while True:
            try:
                kods = int(input("Ievadiet klienta 5 ciparu kodu: "))
                if kods not in self.klientu_saraksts:
                    print("Klients netika atrasts.") 
                elif kods in self.klientu_saraksts:
                    klients = self.klientu_saraksts[kods][0]
                    self.klientu_saraksts.pop(kods)
                    self.saglabat_faila()
                    print(f"Klienta {klients} abonements ir atcelts.") # Ja klients eksistē, pēc koda ievadīšanas tiek atcelts abonemetnts
                    break
            except ValueError:
                print("Ievadiet atbilstošu vērtību!")

klientu_saraksts = Klientu_saraksts()
klientu_saraksts.panem_no()
darbibas = Parbaude(klientu_saraksts.klientu_saraksts)

while True:
    print("Lūdzu ievadiet savu izvēli (1-4):")
    print("1 - Pierakstīt jaunu klientu")
    print("2 - Pārbaudīt klienta abonementa statusu")
    print("3 - atjaunot klienta abonementa statusu")
    print("4 - atcelt abonementa statusu")
    print("stop - beigt programmu")
    izvele=input()
    if izvele == "stop":
        exit()
    elif int(izvele) >=1 and int(izvele) <=4:
        pass
    else:
        print("Izvele ir starp 1-4")
        continue
    if izvele == "1":
        klientu_saraksts.pierakstit()
        klientu_saraksts.saglabat_faila()
    if izvele == "2":
        darbibas.parbaudit()
    if izvele == "3":
        darbibas.atjaunot()