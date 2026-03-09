import secrets
import time

class Ja1pr750:
    def __init__(self, key1, key2, key3, abeceda, supress="abcdefghijklmnop"):
        self.key1 = key1
        self.key2 = key2
        self.key3 = key3
        self.abeceda = abeceda
        self.supress = supress

    def _remove2(self ,vec):
        return vec.replace("2", "")
    def _randomsalt(self ,szn, lenght):
        a = ""
        for i in range(lenght):
            a = a + secrets.choice(szn)
        return a
    def _mix_szn(self ,szn):
        pocet = len(szn)
        for i in range(pocet):
            a = secrets.choice(szn)
            szn.remove(a)
            szn.insert(secrets.randbelow(len(szn)), a)
        print(len(szn))
        return szn
    def _rotate(self ,list, n):
        while not list[0] == n:
            a = list.pop()
            list.insert(0, a)
        return list
    def _rotate_back(self ,list, n):
        while not list[0] == n:
            a = list.pop(0)
            list.append(a)
        return list


    def sifrovat(self, data):
        time1 = time.time() #Time measuring
        datalen = len(data)
        # < >Vigenere< >
        a,b,c = 0, 0, 0 # Three variables for keys
        vysledekl = []   #Final output from vigenere

        #Adding salt
        keey1elenght = min(len(self.key1) * len(self.key2) * len(self.key3), 100)  #Ensuring the salt will be one repeating sequence of keys, if too long it jumps to 100
        self.abeceda = list(self.abeceda)                                   #Makes lists of characters that salt can contain
        data = self._randomsalt(self.abeceda, keey1elenght) + data            #Calls randomsalt function which creates the salt using secrets library and then adds salt to data


        #Utf-8 coding
        utf = data.encode("utf-8")     #Code into numbers from 0 to 256

        #Amplifing the avalanche effect
        data = list(utf)
        for i in range(1, len(data)):
            data[i] = data[i] ^ data[i - 1]

        textl = []
        for i in data:                       #Translates back to characters from extended ascii
            textl.append(self.abeceda[i])       #This way is it ensured that messages can use any characters from utf-8 (including emoji´s and special characters)
        text = "".join(textl)               #Using .append and .join, as it is faster than +


        lista = list(self.abeceda)       #Creates list for mixing
        for i in range(len(text)):  #Goes through every character of text

            #Rotating and mixing
            pozice = lista.index(text[i])                                               # Position of character before mixing
            posun1 = int((lista.index(self.key1[a])) % len(self.abeceda))                         # Gets first number for mixing from self.key1
            lista = self._rotate(lista, self.key1[a])                                              # Rotates mixing list
            posun2 = int((lista.index(self.key2[b]) ^ lista.index(self.key3[c])) % len(self.abeceda))  # Gets second number for mixing from self.key2 xor self.key3
            lista[posun1], lista[posun2] = lista[posun2], lista[posun1]                 # Swaps two characters in mixing list posun1 and posun2
            lista = self._rotate(lista, self.abeceda[posun2])                                      # Rotates mixing list once more
            #lista = rotate(lista, self.key2[b])                                             #\
            #lista = rotate_back(lista,self.key3[c])                                         #/ Some more unnesseary rotations

            vysledekl.append(lista[pozice])                                  #Gets ciphered character

            a = (a + 1) % len(self.key1)     #\
            b = (b + 1) % len(self.key2)     # |> Moving to the next character
            c = (c + 1) % len(self.key3)     #/
        vysledek = "".join(vysledekl) #Using .append and .join, as it is faster than +
        # </>Vigenere< >

        # < >Base16< >
        base162 = []   #Variable for data in normal state
        sifr = self.abeceda #Creates map for base16

        # Translate to binary
        base161 = [format(sifr.index(i),"08b") for i in vysledekl] # Translates number to binary
        base161 = "".join(base161)
        # Translating back to characters
        for b in range(0, len(base161), 4): # Goes through every character of binary data
            g = int(base161[b:b+4], 2)   # Decodes binary to number (4 bits to one number between 0-16)
            base162.append(self.supress[g])         #Adds character from self.supress with index of the decoded binary to result
        base162 = "".join(base162)
        # </>Base16<>
        print("Ciphered data:")
        print("Completed! Time", time.time()-time1, "s, average time for character :", (time.time()-time1)/datalen, "s")
        return base162  # Returns result


    def odsifrovat(self, data):
        time1 = time.time() # Time measuring
        datalen = len(data)

        # < >Base16< >
        base161, base162  = [], [""]
        sifr = self.abeceda # Gets map

        for i in data:
            a = self.supress.index(i)        # Gets number for coding
            base161.append(format(a,"04b"))  # Codes number into half bytes
        base161 = "".join(base161) # Again uses .append because it is faster etc.

        for b in range(0, len(base161), 8): # Goes through every eight character of base161
            g =  int(base161[b:b+8],2)      #  Translates binary into decimal
            base162.append(sifr[g])
        base162 = "".join(base162)  # Once more
        # </>Base16<>

        # < >Vigenere < >
        a, b ,c = 0, 0, 0
        keey1elenght = min(len(self.key1) * len(self.key2) * len(self.key3), 100)

        vysledekl = []
        lista = list(self.abeceda) #Dynamic alphabet
        lista2 = list(self.abeceda) # Alphabet backup
        for i in range(len(base162)): #For every character

            posun1 = int((lista.index(self.key1[a])) % len(self.abeceda))                     # Gets first number for deciphering from self.key1
            lista = self._rotate(lista, self.key1[a])                                          # Rotates dynamic list
            posun2 = (lista.index(self.key2[b]) ^ lista.index(self.key3[c])) % len(self.abeceda)   # Gets second number for deciphering from self.key2 xor self.key3
            lista[posun1], lista[posun2] = lista[posun2], lista[posun1]             # Swaps two characters in dynamic list posun1 and posun2
            lista = self._rotate(lista, self.abeceda[posun2])                                  # Rotates dynamic list once more
            # lista = rotate(lista, self.key2[b])
            # lista = rotate_back(lista, self.key3[c])

            pozice = lista.index(base162[i]) #  Position of character after mixing
            vysledekl.append(lista2[pozice]) #  Gets of character from backup list
            lista2 = list(lista)        # Saving alphabet state for next character (to decode avalanche effect)

            a = (a + 1) % len(self.key1)     #\
            b = (b + 1) % len(self.key2)     # |> Moving to the next character
            c = (c + 1) % len(self.key3)     #/

        data = [self.abeceda.index(i) for i in vysledekl] #Translating into numbers for de-avalanche

        # De-avalanching
        for i in range(len(data) - 1, 0, -1):
            data[i] = data[i] ^ data[i - 1]

        # Using try because of possible errors in transmitting
        try:
            vysledek = bytes(data).decode("utf-8") # Decodes in utf
        except: # Means utf-8 coding was unsuccesfull
            print(" ")                                                # Informing user
            print("Critic error, data were damaged or manipulated!")
            print("Returning without utf-8 coding!")
            print("!Warning! Data aren´t valid!")
            etext = [self.abeceda[i] for i in data]  # Emergency translating data into ASCII extended
            vysledek="".join(etext)
        vysledek = vysledek[keey1elenght:]
        print("Completed! Time", time.time() - time1, "s, average time for character :",
              (time.time() - time1) / datalen, "s") # Calculate used time
        print("Deciphered data:")
        return vysledek # Retrurns deciphered data
        # </>Vigenere < > 