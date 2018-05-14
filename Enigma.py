# Fuente para modelar las Ruedas (Wheel)
# enigma.louisedade.co.uk/howitworks.html
# Fuente para modelar el reflector B
# http://mat.uab.cat/~rcamps/cripto/docs/detalles_tecnicos_enigma.pdf

# Convertir cadena a lista (trivial)
def convert(str):
    a=[]
    for i in str:
        a.append(i)
    return a
# plugboard Enigma
class plugBoard:
    def __init__(self,rollo):
        self.abecedario=[]
        self.cifrado=[]
        self.abecedario=self.fill()
        self.cifrado=rollo
        return
    # llenar arreglo en orden
    def fill(self):
        a=[]
        for i in range(65,91):
            a.append(chr(i))
        return a
    
    def rota(self,static, n):
        if not static:
            #Llenado cifrado    
            temp=self.cifrado
            j=1 
            nuevo1=[]   
            for i in range(0,26):
                nuevo1.append(temp[j%26])
                j+=1
            self.cifrado= nuevo1

# Rueda enigma
class wheel:
    def __init__(self,static,roll=None):
        self.rotaciones=0
        self.pb = plugBoard(roll)
        if(static):
            self.static=True
        else:
            self.static=False  
    # rotar caracteres
    def rota(self):
        self.pb.rota(self.static,1)
        self.rotaciones=(self.rotaciones+1)%26

#Conectores para reflector B
class conector:
    def __init__(self,a,b):
        self.a=a
        self.b=b
    def check(self,character):
        #Devuelve la pareja de los caracteres- simulando una conección 
        # Si el caracter no se reconoce regresa None
        if character==self.a:
            return self.b
        elif character==self.b:
            return self.a
        else:
            return None

#Reflector B
class reflector:
    def __init__(self,letter):
        self.a=letter.upper()
        self.conectors=[]
        self.conectors.append( conector('A','Y') )
        self.conectors.append( conector('B','R') )
        self.conectors.append( conector('C','U') )
        self.conectors.append( conector('D','H') )
        self.conectors.append( conector('E','Q') )
        self.conectors.append( conector('F','S') )
        self.conectors.append( conector('G','L') )
        self.conectors.append( conector('I','P') )
        self.conectors.append( conector('J','X') )
        self.conectors.append( conector('K','N') )
        self.conectors.append( conector('M','O') )
        self.conectors.append( conector('T','Z') )
        self.conectors.append( conector('V','W') )
        self.conectors.append( conector(' ',' ') )

    def reflect(self):
        for conection in self.conectors:
            if conection.check(self.a)!=None:
                return conection.check(self.a)

class Enigma:
    def __init__(self,rolls,config):
        self.wheels=[]
        self.config=config
        #PB Estatico
        self.wheels.append(wheel(True,convert(rolls[0])))
        # Los demas giran (static=false)
        self.wheels.append(wheel(False,convert(rolls[1])))
        self.wheels.append(wheel(False,convert(rolls[2])))
        #Configurar
        for i,position in enumerate(self.config):
            for j in range(position):
                self.wheels[i].rota()
        
    def Run(self,text):
        text=text.upper()
        encrypted=""
        for char in text:
            # Primera letra que sale
            firstIndex=self.wheels[2].pb.abecedario.index(char)
            firstOut=self.wheels[2].pb.cifrado[firstIndex] 
            # Obtener índice de la letra que salio
            letterIndex=self.wheels[1].pb.abecedario.index(firstOut)
            # Segunda letra que sale
            SecondOut=self.wheels[1].pb.cifrado[letterIndex]
            # Obtener indice de la segunda letra que salio
            nextLetterIndex=self.wheels[0].pb.abecedario.index(SecondOut)
            # Obtener tercera letra que sale
            ThirdOut=self.wheels[0].pb.cifrado[nextLetterIndex]
            #Reflector
            ReflectedLetter=reflector(ThirdOut).reflect()
            # First Trackback
            tbIndex=self.wheels[0].pb.cifrado.index(ReflectedLetter)
            tbFirst=self.wheels[0].pb.abecedario[tbIndex]
            # Second Trackback
            SecondtbIndex=self.wheels[1].pb.cifrado.index(tbFirst)
            tbSecond=self.wheels[1].pb.abecedario[SecondtbIndex]
            # Third Trackback
            ThirdtbIndex=self.wheels[2].pb.cifrado.index(tbSecond)
            OfficialOut=self.wheels[2].pb.abecedario[ThirdtbIndex]
            #Rotate 
            
            self.wheels[2].rota()
            if self.wheels[2].rotaciones>=26: 
                self.wheels[1].rota()
                self.wheels[2].rotaciones=0
            if self.wheels[1].rotaciones>=26:
                self.wheels[1].rotaciones=0
                self.wheels[2].rotaciones=0
            
            encrypted+=OfficialOut
            
        return encrypted
    def Restart(self):
        for i,conf in enumerate(self.config):
            while self.wheels[i].rotaciones!=conf:
                self.wheels[i].rota()


rolls=["EKMFLGDQVZNTOWYHXUSPAIBRCJ","AJDKSIRUXBLHWTMCQGZNPYFVOE","BDFHJLCPRTXVZNYEIWGAKMUSQO"]
config=[0,0,0]

e=Enigma(rolls,config)

Text=input("Inserte texto a cifrar: ").replace(' ','')
Cipher=e.Run(Text)
#Imprime encriptado
print("Texto encriptado:", Cipher)
#Reinicia la configuración
e.Restart()
#Imprime desencriptado
print("Texto Desencriptado:",e.Run(Cipher))




