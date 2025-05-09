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
        day = 365
        years = 1
        termins = datetime.now() #paņem tagadējo datumu
        termins = termins + timedelta(days=day*years) #pievieno datumam 1 gadu
        termins = termins.strftime("%d-%m-%Y") #pārveido datumu uz pareizo formātu
        self.klientu_saraksts.update({kods:[klients,termins]}) #pievieno kodu kā atslēgu un [klients,termins] ka vērtību
        print(f"{klients} ir pierakstīts abonementam\nkods: {kods}\ntermins līdz: {termins}")
        print("*******************************************************")
        return kods
    def saglabat(self): #saglabā failā
        with open('Klientu_saraksts.txt','w',encoding='utf8') as fails:
            for klients, vertiba in self.klientu_saraksts.items():
                fails.write(f'{klients}:{vertiba[0]},{vertiba[1]}\n')
    def panem_datus(self):#nolasa no faila
        try:#lai neizmet error ja nav faila
            with open('Klientu_saraksts.txt','r',encoding='utf8') as fails:
                for rinda in fails: #katru faila rindu split ar :
                    kods,vertiba = rinda.strip().split(':') #iegūst kodu kā key un vērtību kas satur klientu vārdu uzvārdu un termiņu
                    klients,termins = vertiba.strip().split(',')#split ar , un sadala klienta vārdu un uzvārdu un termiņu
                    self.klientu_saraksts[kods]=[klients,termins] #ieliek vārdnīcā
        except FileNotFoundError:
            pass
        
# Klase "Parbaude", kas manto no klases "Klientu_saraksts"
class Parbaude(Klientu_saraksts):
    def __init__(self,klientu_saraksts):
        self.klientu_saraksts=klientu_saraksts
# FUNKCIJA PARBAUDIT - Pārbauda klienta abonementa statusu, ja abonements beidzies ir iespēja to pagarināt, vai pierakstīt klientu
    def parbaudit(self):
        while True:
                try:
                    for i in range(0,2): #atļauj ievadīt vēlreiz ja nav sarakstā, ja piem. ievada nepareizi
                        kods = input("Ievadiet klienta 5 ciparu kodu: ")
                        num = int(kods)
                        if not len(kods) == 5:#koda garuma pārbaude
                            print("Ievadiet 5 ciparu garu kodu!")
                            continue
                        if kods not in self.klientu_saraksts:# Pārbauda vai klients eksistē
                            print("Kods netika atrasts abonementu sarakstā ievadiet vēlreiz")
                            continue
                        elif kods in self.klientu_saraksts:
                            break
                    if kods not in self.klientu_saraksts: # pajautā vai Gundega ir pārliecināta ka ievada kodu pareizi
                        J_N = input(f"Koda nav sarakstā vai esat pārliecināts, ka šis:{kods} kods ir pareizais: ")
                        if J_N == 'J':
                            pass
                        elif J_N =="N":
                            print("Lūdzu ievadiet vēlreiz uzmanīgāk")
                            continue
                    if kods not in self.klientu_saraksts: 
                        print('Klients nav pierakstīts.')
                        while True: #ļauj izveidot jaunu klientu izmantojot pierakstit() un tad saglabā failā
                            turpinat = input("Vai klients vēlās pierakstīties? (J/N): ") 
                            if turpinat == 'J': # Ja neeksistējošs klients vēlas iegūt abonementu:
                                self.pierakstit()
                                self.saglabat()
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
                        termins = datetime.strptime(termins, formats) #pārveido termiņu uz datetime objektu
                        if termins <= datetime.now(): #pārbauda termiņu
                                # Paziņo, ka abonements beidzies, dod opciju pagarināt to
                            atjaunot = input(f"{self.klientu_saraksts[kods][0]} abonements ir beidzies.\nVai vēlaties atjaunot abonementu? (J/N):")
                            if atjaunot == 'J': # Abonementa pagarināšana
                                day = 365
                                years = 1
                                termins = datetime.now() #paņem tagadējo datumu
                                termins = termins + timedelta(days=day*years) #pievieno datumam 1 gadu
                                termins = termins.strftime("%d-%m-%Y") #pārveido datumu uz pareizo formātu
                                self.klientu_saraksts.update({kods:[self.klientu_saraksts[kods][0],termins]}) #update dict ar jauno terminu
                                self.saglabat()
                                print(f"Klienta {self.klientu_saraksts[kods][0]} abonements tika pagarināts līdz {self.klientu_saraksts[kods][1]}.")
                                print("*******************************************************")
                                break
                            elif atjaunot == 'N': # Abonements netiek pagarināts 
                                break
                        else:
                            print("Lietotājam ir abonements.")
                            print("*******************************************************")
                            break
                except ValueError: # Kļūdu pārbaude
                    print("Ievadiet atbilstošu vērtību!")
                    continue

#FUNKCIJA ATJAUNOT - atjauno eksitējoša klienta abonementu, ja klients neeksiste, dod iespēju pievienot
    def atjaunot(self):
        while True:
            for i in range(0,2):
                kods = input("Ievadiet klienta 5 ciparu kodu: ")
                if not len(kods) == 5:# Pievienot koda garuma pārbaudi
                    print("Ievadiet 5 ciparu garu kodu!")
                    continue
                if kods not in self.klientu_saraksts:# Pārbauda vai klients eksistē
                    print("Kods netika atrasts abonementu sarakstā ievadiet vēlreiz")
                    continue
                elif kods in self.klientu_saraksts:
                    break
            if kods not in self.klientu_saraksts:
                J_N = input(f"Koda nav sarakstā vai esat pārliecināts, ka šis:{kods} kods ir pareizais: ")
                if J_N == 'J':
                    pass
                elif J_N =="N":
                    print("Lūdzu ievadiet vēlreiz uzmanīgāk")
                    continue
            if kods not in self.klientu_saraksts: #ļauj pierakstī klientu
                turpinat = input("Klientam nav abonements.\nVai klients vēlās pierakstīties? (J/N): ") # Ja klientam nav abonements, dod iespēju to iegūr 
                if turpinat == 'J':
                    kods = self.pierakstit()
                    self.saglabat()
                    break
                elif turpinat == 'N': # Abonements netiek izveidots
                    break
            else: 
                day = 365
                years = 1
                termins = datetime.now() #paņem tagadējo datumu
                termins = termins + timedelta(days=day*years) #pievieno datumam 1 gadu
                termins = termins.strftime("%d-%m-%Y") #pārveido datumu uz pareizo formātu
                self.klientu_saraksts.update({kods:[self.klientu_saraksts[kods][0],termins]}) #pievieno kodu kā atslēgu un [klients,termins] ka vērtību
                self.saglabat()
                print(f"Klienta {self.klientu_saraksts[kods][0]} abonements ir atjaunots, derīguma termiņš: {self.klientu_saraksts[kods][1]}.") # Pagarina klienta abonementu
                print("*******************************************************")
                break

#FUNKCIJA ATCELT - atceļ eksistējoša klienta abonementu
    def atcelt(self):
        while True:
            try:
                for i in range(0,2):
                    kods = input("Ievadiet klienta 5 ciparu kodu: ")
                    num = int(kods)
                    if not len(kods) == 5:
                        print("Ievadiet 5 ciparu garu kodu!")
                        continue
                    if kods not in self.klientu_saraksts:
                        print("Kods netika atrasts abonementu sarakstā ievadiet vēlreiz")
                        continue
                    elif kods in self.klientu_saraksts:
                        break
                if kods not in self.klientu_saraksts:
                    J_N = input(f"Koda nav sarakstā vai esat pārliecināts, ka šis:{kods} kods ir pareizais: ")
                    if J_N == 'J':
                        pass
                    elif J_N =="N":
                        print("Lūdzu ievadiet vēlreiz uzmanīgāk")
                        continue
                if kods not in self.klientu_saraksts: #ja klientam nav abonements
                    print("Klientam nav abonements.")
                    print("*******************************************************")
                    break
                elif kods in self.klientu_saraksts: #izdzēš klientu izmantojot pop()
                    klients = self.klientu_saraksts[kods][0]
                    self.klientu_saraksts.pop(kods)
                    self.saglabat()
                    print(f"Klienta {klients} abonements ir atcelts.") # Ja klients eksistē, pēc koda ievadīšanas tiek atcelts abonemetnts
                    print("*******************************************************")
                    break
            except ValueError:
                print("Ievadiet atbilstošu vērtību!")
                continue

while True: #izvelne kur lietotājs izvēlās savas darbības
    klientu_saraksts = Klientu_saraksts() #izveido objektu
    klientu_saraksts.panem_datus()#nolasa no faila katru reizi sāk no jauna, lai būtu jaunākā informācija
    darbibas = Parbaude(klientu_saraksts.klientu_saraksts) #izveido objektu darbibas
    print("Lūdzu ievadiet savu izvēli (1-4):")
    print("1 - Pierakstīt jaunu klientu")
    print("2 - Pārbaudīt klienta abonementa statusu")
    print("3 - atjaunot klienta abonementa statusu")
    print("4 - atcelt abonementa statusu")
    print("stop - beigt programmu")
    izvele=input()
    if izvele == "stop":
        print("Programma beidzas")
        exit()
    elif int(izvele) >=1 and int(izvele) <=4:
        pass
    else:
        print("Izvele ir starp 1-4")
        continue
    if izvele == "1":
        klientu_saraksts.pierakstit()
        klientu_saraksts.saglabat()
    if izvele == "2":
        darbibas.parbaudit()
    if izvele == "3":
        darbibas.atjaunot()
    if izvele == "4":
        darbibas.atcelt()