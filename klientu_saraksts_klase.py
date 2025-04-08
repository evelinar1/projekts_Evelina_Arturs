from datetime import datetime 
from datetime import timedelta
import random
class Klientu_saraksts():
    def __init__(self): #inicializē vārdnīcu klientu_saraksts
        self.klientu_saraksts={}
    def pierakstit(self): #pieraksta klientu abonementu sarakstam
        klients = input("Jaunā klienta vārds un uzvārds (Vārds Uzvārds): ")
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
        print(f"Jaunais klients {klients} ir pievienots, tā abonementa termiņs ir līdz {termins} un tā kods {kods}.")
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



termins = "02-04-2026"
formats = "%d-%m-%Y"

termins = datetime.strptime(termins, formats)
if termins <= datetime.now():
    print("Datums ir mazāks")
else:
    print("datums ir lielāks")


klientu_saraskts = Klientu_saraksts()
klientu_saraskts.panem_no()




#izveles sākums
while True:
    print("Lūdzu ievadiet savu izvēli (1-4):")
    print("1 - Pierakstīt jaunu klientu")
    print("2 - Pārbaudīt klienta abonementa statusu")
    print("3 - atjaunot klienta abonementa statusu")
    print("4 - atcelt abonementa statusu")
    izvele=input()
    if izvele >=1 and izvele <=4:
        pass
    else:
        print("Izvele ir starp 1-4")
        continue
    if izvele == 1:
        klientu_saraskts.pierakstit()
        klientu_saraskts.saglabat_faila()
    if izvele == 2:
        kods=input("Ievadiet klienta 5 ciparu kodu:")
        if kods not in klientu_saraskts.klientu_saraksts:
            print("Klients nav abonements.")
            while True:
                j_vai_n = input("Vai klients vēlās pierakstīties(J/N):")
                if j_vai_n == "J":
                    pass



