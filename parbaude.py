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
        self.klientu_saraksts.update({klients:[kods,termins]}) #pievieno klientu kā atslēgu un [kods,termins] ka vērtību
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
                    klients,vertiba = rinda.strip().split(':')
                    kods,termins = vertiba.strip().split(',')
                    self.klientu_saraksts[klients]=[kods,termins]
        except FileNotFoundError:
            pass

# Klase "Parbaude", kas manto no klases "Klientu_saraksts"
class Parbaude(Klientu_saraksts):
    def __init__(self,klientu_saraksts):
        super().__init__(klientu_saraksts)
        

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
                except ValueError: # Kļūdu pārbaude
                    print("Ievadiet atbilstošu vērtību!")
                    continue

#FUNKCIJA ATJAUNOT - atjauno eksitējoša klienta abonementu, ja klients neeksiste, dod iespēju pievienot un iedod jaunā klienta kodu
    def atjaunot(self):
        while True:
            try:
                kods = int(input("Ievadiet klienta 5 ciparu kodu: "))
                if kods not in self.klientu_saraksts:
                    turpinat = input("Klientam nav amonements.\nVai vēlajties pierakstīties abonementam? (J/N): ") # Ja klientam nav abonements, dod iespēju to iegūr 
                    if turpinat == 'J':
                        kods = self.pierakstit()
                        # Parāda, ka jaunais klients ir ieguvis abonementu, parāda tā derīguma termiņu un klienta kodu
                        print(f"Jaunais klients {self.klientu_saraksts[kods][0]} ir pievienots! Abonementa termiņš: {self.klientu_saraksts[kods][1]}, kods: {kods}")
                    elif turpinat == 'N': # Ja neturpina, programma beidzas
                        break
                else: 
                    termins = datetime.now() #paņem tagadējo datumu
                    termins = termins + timedelta(days=365) #pievieno datumam 1 gadu
                    termins = termins.strftime("%d-%m-%Y") #pārveido datumu uz pareizo formātu
                    self.klientu_saraksts.update({self.klientu_saraksts[kods][0]:[kods,termins]}) #pievieno klientu kā atslēgu un [kods,termins] ka vērtību
                    print(f"Klienta {self.klientu_saraksts[kods][0]} abonements ir atjaunots, derīguma termiņš: {self.klientu_saraksts[kods][1]}.") # Pagarina klienta abonementu
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
                    print(f"Klienta {klients} abonements ir atcelts.") # Ja klients eksistē, pēc koda ievadīšanas tiek atcelts abonemetnts
                    break
            except ValueError:
                print("Ievadiet atbilstošu vērtību!")





klients = Parbaude(73343,'Rihards Krūmiņš','02-04-2026',)
klients.parbaudit()