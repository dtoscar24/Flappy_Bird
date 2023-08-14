import pygame # Per a crear el joc
import neat # Bàsicament per a evolucionar i crear xarxes neuronals
import os # Per a buscar les rutes de les nostres imatges i el fitxer de configuració
import random # Per a crear nombres aleatoris

pygame.font.init() # Inicialitzem la font
FONT = pygame.font.SysFont('comicsans', 25) # Establim la font i la mida de la lletra
blanc = (255, 255, 255) # Creem un color blanc en RGB i ho guardem a la variable blanc
                              
FINESTRA_AMPLADA = 450 # Amplada de la finestra (en píxels)
FINESTRA_ALTURA = 600 # Alçada de la finestra (en píxels)

# Creem la finestra del joc passant-li les seves mides
FINESTRA = pygame.display.set_mode((FINESTRA_AMPLADA, FINESTRA_ALTURA)) 
pygame.display.set_caption("Flappy Bird") # Posem un nom a la finestra

'''# Bucle while que s'executarà sempre quan sigui True
while True: 

    FINESTRA # Mostrem la finestra acabem de crear

    # Obtenim cada acció (event) feta per l'usuari, o sigui, nosaltres
    for event in pygame.event.get():
        # Mirem si el tipus d'acció que hem fet és igual que la de sortir, 
        # és a dir, si hem clicat el botó de tancar (a dalt a la dreta)
        if event.type == pygame.QUIT:
         # En el cas que sigui cert, es tancarà la finestra
         pygame.quit()
         quit()'''

# Carreguem i redimensionem les imatges de l'ocell i les fiquem a la llista imatges_ocells 
imatges_ocells = [pygame.transform.scale2x(pygame.image.load(os.path.join("imatges", "ocell1.png"))),
                  pygame.transform.scale2x(pygame.image.load(os.path.join("imatges", "ocell2.png"))), 
                  pygame.transform.scale2x(pygame.image.load(os.path.join("imatges", "ocell3.png")))]

# Fem la mateixa cosa, però aquesta vegada amb la foto de la columna, de la base i del fons 
imatge_columna = pygame.transform.scale(pygame.image.load(os.path.join("imatges", "columna.png")), (78, 480))
imatge_base = pygame.transform.scale(pygame.image.load(os.path.join("imatges", "base.png")), (504, 168)) 
imatge_fons = pygame.transform.scale(pygame.image.load(os.path.join("imatges", "fons.png")), (450, 600))

# Constant que ens ajudarà a saber el nombre de generacions que portem
GEN = 0

# Creem la classe Ocell
class Ocell:  
    # Establim que la llista imatges_ocells sigui igual a OCELL   
    OCELL = imatges_ocells  
    MAX_ROTATION = 25 # Màxima rotació que pot fer l'ocell
    ROTATION_VELOCITAT = 20 # Velocitat de rotació
    ANIMATION_TEMPS = 5 # Temps d'intercanvi entre les imatges

    # Creem el mètode __init__() i rebrà x i y com a paràmetres
    def __init__(self, x, y):
        self.x = x # Posició X inicial de l'ocell
        self.y = y # Posició Y inicial de l'ocell
        self.inclinació = 0 # Inclinació inicial de l'ocell
        self.velocitat = 0 # Velocitat inicial de l'ocell
        self.altura = self.y # Altura inicial de l'ocell, la qual serà igual 
        # que l'atribut self.y
        self.comptador_física = 0 # Comptador que ens servirà per a fer les 
        # físiques de l'ocell
        self.comptador_imatge = 0 # Comptador que ens ajudarà a saber quan 
        # intercanviar les diferents fotos de l'ocell entre si
        self.imatge = self.OCELL[0] # La imatge que es mostrarà a l'inici(ocell1.png)

    # Creem el mètode saltar() per al salt de l'ocell 
    def saltar(self):
        self.velocitat = -10.5 # Velocitat cap a a dalt de l'ocell quan salta
        self.comptador_física = 0 # Comptador que serveix per a saber el 
        # temps transcorregut en cada salt que fa l'ocell
        self.altura = self.y # L'altura original de l'ocell abans del salt 

    # Creem el mètode moviment() el qual ens servirà per a fer el moviment vertical de l'ocell
    def moviment(self):
        # Per cada frame li sumarem +1 a self.comptador_física
        self.comptador_física += 1 # self.comptador_física = self.comptador_física + 1

        # Calculem el desplaçament (en píxels) cap a dalt o cap avall que farà l'ocell en un frame determinat
        desplaçament = (self.velocitat * self.comptador_física) + (1.5 * (self.comptador_física ** 2))
        # Exemples quan self.comptador_física té diferents valors:
        # Quan és 1: desplaçament = (-10.5 · 1) + (1.5 · (1^2)) = -10.5 + 1.5 = -9 (va cap a dalt)
        # Quan és 4: desplaçament = (-10.5 · 4) + (1.5 · (4^2)) = -42 + 24 = -18 (va cap a dalt)
        # Quan és 6: desplaçament = (-10.5 · 6) + (1.5 · (6^2)) = -63 + 54 = -9 (va cap a dalt)
        # Quan és 9: desplaçament = (-10.5 · 9) + (1.5 · (9^2)) = -94.5 + 121.5 = 27 (va cap avall)
        # Els càlculs que hem fet voldrà dir que l'ocell es mourà 9, 18 i 9 píxels cap a dalt i 27 píxels 
        # cap avall en aquell frame. El valor de self.comptador_física tornarà a ser 0 quan l'ocell
        # salti una altra vegada i, com a resultat, faríem de nou les operacions.

        # Fem dues condicions if per a limitar el moviment de l'ocell
        # Mirem si el seu desplaçament cap avall és major o igual que 16 píxels:
        if desplaçament >= 16:
            desplaçament = 16 # En el cas que sigui cert, serà igual que 16, és a dir, 
            # que només es podrà moure 16 píxels cap avall 

        # Mirem si el desplaçament és cap a dalt, per tant, el seu valor serà negatiu:
        if desplaçament < 0: 
            desplaçament -= 2 # En el cas que sigui vertader, farem que l'ocell pugi 
            # 2 píxels més. Exemple del càlcul que s'estaria fent quan el desplaçament
            # inicial sigui -18 --> desplaçament = -18 -2 = -20 píxels cap a dalt

        # Actualitzem la posició nova de l'ocell en funció del desplaçament calculat
        self.y = self.y + desplaçament

        # Veiem si el desplaçament és cap a dalt o que l'altura actual de l'ocell és 
        # menor que la seva posició anterior
        if desplaçament < 0 or self.y < self.altura:
            # En el cas que això sigui cert, mirem si la inclinació actual de l'ocell
            # és menor que la constant MAX_ROTATION(25)
            if self.inclinació < self.MAX_ROTATION:
                # En el cas que sigui vertader, li assignarem el valor de MAX_ROTATION
                self.inclinació = self.MAX_ROTATION

        # En el cas que l'anterior sigui fals, és a dir, que el desplaçament és cap 
        # avall, farem una altra cosa:
        else:

            # Mirem si la inclinació actual de l'ocell és major que -90 graus
            if self.inclinació > -90:
                
                # En el cas que sigui cert, li restarem la constant ROTATION_VELOCITAT
                # de manera que simularem que l'ocell està anant cap avall
                self.inclinació -= self.ROTATION_VELOCITAT 

    # Creem el mètode dibuixar() per a dibuixar les imatges de l'ocell en diferents 
    # posicions, el qual rebrà l'atribut finestra com a paràmetre
    def dibuixar(self, finestra):
        self.comptador_imatge += 1 # Li sumem +1 a l'atribut comptador_imatge

        # Condicions que ens ajuda a canviar les fotos de l'ocell
        # Primera condició: 
        # Mirem si el valor de comptador_imatge és menor o igual que la constant ANIMATION_TEMPS(5)
        if self.comptador_imatge <= self.ANIMATION_TEMPS:
            # En el cas que sigui cert, mostrarem la primera imatge(ocell1.png) de la llista OCELL.
            # Aquesta foto ho guardarem a l'atribut imatge, el qual ho emprarem més tard per a 
            # dibuixar l'ocell 
            self.imatge = self.OCELL[0] 

        # Segona condició:
        # En el cas que la primera condició sigui fals, veurem si es compleix la segona, és a dir, 
        # mirem si és menor o igual que ANIMATION_TEMPS però aquesta vegada multiplicat per 2 (5·2=10)
        elif self.comptador_imatge <= self.ANIMATION_TEMPS*2:
            # En el cas que sigui vertader, ensenyarem la segona imatge(ocell2.png)
            self.imatge = self.OCELL[1] 

        # Tercera condició:
        # En el cas que la segona condició també sigui fals, comprovarem si es compleix que és menor o 
        # igual que ANIMATION_TEMPS multiplicat per 3 (5·3=15)
        elif self.comptador_imatge <= self.ANIMATION_TEMPS*3:
            # En el cas que això sigui cert, mostrarem la tercera imatge(ocell3.png) 
            self.imatge = self.OCELL[2] 

        # Quarta condició:
        # En el cas que la tercera condició encara sigui fals, mirem si es compleix que és menor o 
        # igual que ANIMATION_TEMPS multiplicat per 4 (5·4=20)
        elif self.comptador_imatge <= self.ANIMATION_TEMPS*4:
            # En el cas que això sigui vertader, mostrarem una altra vegada la segona imatge(ocell2.png) 
            self.imatge = self.OCELL[1] 
 
        # En el cas que tot l'anterior sigui fals farem una altra cosa:
        else:
            self.imatge = self.OCELL[0] # Ensenyarem la primera imatge de l'ocell (ocell1.png) 
            self.comptador_imatge = 0 # Reiniciem el valor de l'atribut comptador_imatge a 0 perquè 
            # torni a fer el moviment de l'ocell des de la primera condició i així contínuament

        # Creem una condició per a mirar si la inclinació actual de l'ocell és menor 
        # o igual que -80 graus
        if self.inclinació <= -80:
            # En el cas que sigui cert, establirem les següents coses:
            self.imatge = self.OCELL[1] # Fem que l'atribut imatge sigui igual que 
            # la segona foto de l'ocell 
            self.comptador_imatge = self.ANIMATION_TEMPS*2 # Fem que l'atribut 
            # comptador_imatge sigui igual que la constant ANIMATION_TEMPS per 2 perquè 
            # començi des de la segona condició d'abans. Fem això per a no saltar 
            # l'animació del moviment de l'ocell

        # Girem la imatge segons la inclinació de l'ocell i ho guardem a un atribut denominat imatge_girada
        imatge_girada = pygame.transform.rotate(self.imatge, self.inclinació)
        # Línia de codi que ens serveix per a obtenir el rectangle de la imatge girada a partir de la foto inicial
        nou_rectangle = imatge_girada.get_rect(center=self.imatge.get_rect(topleft = (self.x, self.y)).center)
        # Dibuixem la imatge girada donant-li la finestra i, a més, li concretem la coordenada X i Y on es 
        # mostrarà en funció de l'atribut topleft del nou_rectangle
        finestra.blit(imatge_girada, ((nou_rectangle.topleft)))

    # Definim el mètode obtenir_mask per tal d'obtenir 
    # la màscara de bits de l'ocell
    def obtenir_mask(self):
        return pygame.mask.from_surface(self.imatge) 

# Creem la classe Columna
class Columna:
    ESPAI = 200 # Establim l'espai que hi haurà entre la columna de dalt i la d'avall
    VELOCITAT = 20 # Velocitat la qual anirà les dues columnes

    # Creem el mètode __init__() i li passem l'atribut x com a paràmetre:
    def __init__(self, x): 
        self.x = x # Posició X inicial de les dues columnes 
        self.adalt = 0 # Posició Y inicial de la columna de dalt
        self.avall = 0 # Posició Y inicial de la columna d'avall
        self.altura = 0 # L'altura inicial de les columnes

        # Invertim la imatge de la columna que teníem inicialment respecte del seu 
        # eix Y (True) i no del seu eix X (False)
        self.COLUMNA_ADALT = pygame.transform.flip(imatge_columna, False, True) 
        self.COLUMNA_AVALL = imatge_columna # La columna d'avall serà igual que la 
        # imatge de la columna que teníem originalment

        self.passat = False # Establim que l'atribut passat serà False a l'inici, 
        # el qual ens servirà per a saber si l'ocell ha passat o no per les columnes
        self.establir_altura() # Generem l'altura de la columna de dalt i la d'avall 
        # amb el mètode establir_altura(), el qual ho crearem a continuació

    # Creem el mètode establir_altura() per a crear l'altura de la 
    # columna de dalt i la d'avall
    def establir_altura(self):

        # Creem un nombre enter que estigui en un rang d'entre 50 i 200
        self.altura = random.randrange(50, 200)

        # Calculem la coordenada Y de la columna de dalt
        self.adalt = self.altura - self.COLUMNA_ADALT.get_height() 
        # Calculem la posició Y de la columna d'avall
        self.avall = self.altura + self.ESPAI 

    # Definim el mètode moviment() per al moviment de les columnes
    def moviment(self):
        # Li restem la constant self.VELOCITAT(5) a la posició X de les columnes
        self.x -= self.VELOCITAT # self.x = self.x - self.VELOCITAT

    # Creem el mètode dibuixar() per a dibuixar la columna de dalt i d'avall
    def dibuixar(self, finestra):
        # Dibuixem la columna de dalt en funció de la seva posició X i Y
        finestra.blit(self.COLUMNA_ADALT, (self.x, self.adalt)) 
        # Dibuixem la columna d'avall segons la seva coordenada X i Y
        finestra.blit(self.COLUMNA_AVALL, (self.x, self.avall)) 

    # Creem el mètode col·lisió per a saber si l'ocell s'ha col·lidit o no 
    # amb les columnes i que rebrà com a paràmetre cada ocell d'una població
    def col·lisió(self, ocell):
        # Obtenim les màscares de bits de cada ocell a través de la funció 
        # obtenir_mask() que vàrem crear a la classe Ocell()
        ocell_mask = ocell.obtenir_mask()
        # Aconseguim la màscara de bits de la columna de dalt 
        columna_adalt_mask = pygame.mask.from_surface(self.COLUMNA_ADALT)
        # Fem el mateix amb la columna d'avall
        columna_avall_mask = pygame.mask.from_surface(self.COLUMNA_AVALL)

        # Calculem el desplaçament(offset) de l'ocell amb la columna de dalt
        ocell_columna_adalt_offset = (self.x - ocell.x, self.adalt - round(ocell.y)) 

        # Fem el mateix però aquesta vegada amb la columna d'avall
        ocell_columna_avall_offset = (self.x - ocell.x, self.avall - round(ocell.y))

        # Mirem si s'ha col·lidit o no la màscara de bits de l'ocell amb la de la columna de dalt 
        # fent servir l'offset (ocell_columna_adalt_offset) que hem calculat abans
        col·lisió_ocell_adalt = ocell_mask.overlap(columna_adalt_mask, ocell_columna_adalt_offset) 

        # Fent el mateix que abans però aquesta vegada amb la columna d'avall
        col·lisió_ocell_avall = ocell_mask.overlap(columna_avall_mask, ocell_columna_avall_offset) 

        # Mirem si els ocells s'han col·lidit o no amb les columnes:
        if col·lisió_ocell_adalt or col·lisió_ocell_avall:
            # En el cas que sigui cert, ens retornarà True 
            return True 
        # En el cas contrari, o sigui, no s'han xocat, ens retornarà False
        return False

# Creem la classe Base
class Base:
    VELOCITAT = 5 # Velocitat la qual anirà la primera i la segona base 
    AMPLADA = imatge_base.get_width() # Obtenim l'amplada de la imatge de 
    # la base que vam importar a l'inici de la part pràctica (imatge_base)

    # Creem el mètode __init__() i rebrà l'atribut y com a paràmetre
    def __init__(self, y):
        self.y = y # Posició Y de les dues bases, la qual serà la mateixa
        self.x1 = 0 # Posició X inicial de la primera base
        self.x2 = self.AMPLADA # Posició X inicial de la segona base, la 
        # qual estarà endarrere de la primera

    # Definim el mètode moviment() per al moviment de les dues bases
    def moviment(self):
        # Restem la constant VELOCITAT a la coordenada X de la primera base 
        self.x1 -= self.VELOCITAT # self.x1 = self.x1 - self.VELOCITAT

        # Fem la mateixa cosa però aquesta vegada amb la posició X de la segona 
        self.x2 -= self.VELOCITAT # self.x2 = self.x2 - self.VELOCITAT

        # Primera condició: 
        # Mirem si la posició X de la primera base més de la seva 
        # amplada(self.AMPLADA) és menor que 0
        if self.x1 + self.AMPLADA < 0:
            # En el cas que sigui cert, li sumem la coordenada X 
            # de la segona base més de la seva amplada de manera 
            # que aquesta estarà al seu darrere
            self.x1 = self.x2 + self.AMPLADA

        # Segona condició:
        # Fem el mateix que abans però aquesta vegada amb la segona 
        # base
        if self.x2 + self.AMPLADA < 0:
            # En el cas que aquesta condició sigui cert, li sumem la 
            # posició X de la primera base més de la seva amplada 
            self.x2 = self.x1 + self.AMPLADA

    # Creem el mètode dibuixar() per a dibuixar les dues bases i li donem 
    # el paràmetre finestra
    def dibuixar(self, finestra):
        # Dibuixem la primera base especificant la seva coordenada X i Y
        finestra.blit(imatge_base, (self.x1, self.y))
        # Dibuixem la segona base concretant la seva posició X i Y
        finestra.blit(imatge_base, (self.x2, self.y))

# Creem la funció dibuixar_elements() per a dibuixar les coses que volem mostrar
def dibuixar_elements(finestra, ocells, columnes, bases, puntuació, GEN):

    # Dibuixem la imatge del fons donant-li la finestra i la seva posició X i Y
    finestra.blit(imatge_fons, (0,0))

    # Aconseguim la columna de dalt i la d'avall dins de la llista columnes:
    for columna in columnes:
        columna.dibuixar(finestra) # Dibuixem la columna de dalt i 
        # la d'avall amb el mètode dibuixar() de la classe Columna

    # Obtenim cada ocell d'una població dins de la llista ocells:
    for ocell in ocells:
        ocell.dibuixar(finestra) # Dibuixem a cada ocell donant-li la 
        # finestra a través del mètode dibuixar() de la classe Ocell

    bases.dibuixar(finestra) # Dibuixem les dues bases a partir del mètode 
    # dibuixar() de la classe Base

    # Text de la puntuació
    puntuació_text = FONT.render('Puntuació: '+ str(puntuació), True, blanc)

    # Text de les generacions
    generació_text = FONT.render('Generació: '+ str(GEN), True, blanc)
    
    # Text dels supervivents
    supervivents_text = FONT.render('Supervivents: '+ str(len(ocells)), True, blanc)

    # Mostrem el text de la puntuació especificant-li la seva coordenada X i Y
    finestra.blit(puntuació_text, (FINESTRA_AMPLADA - puntuació_text.get_width() - 10, 10)) 

    # Fem el mateix amb el text de les generacions
    finestra.blit(generació_text, (10, 10))
    
    # Fem el mateix amb el text dels supervivents
    finestra.blit(supervivents_text, (10, 50))

    pygame.display.update() # Actualitzem els canvis

# Creem la funció main() i que rebrà com a paràmetres 
# els genomes i les seves respectives configuracions
def main(genomes, configuració):

    global GEN # Fem que GEN sigui una variable global
    GEN += 1 # Per cada evolució li sumarem +1 a la constant GEN
    finestra = FINESTRA # Fem que la variable finestra sigui igual que FINESTRA

    bases = Base(500) # Establim la posició Y de les dues bases
    columnes = [Columna(600)] # Especifiquem la coordenada X de 
    # la columna de dalt i la d'avall

    partida = True # Variable partida que servirà per a l'algoritme perquè sàpiga 
    # quan generar o no una nova generació
    clock = pygame.time.Clock() # Funció de Pygame per a controlar el FPS del joc
    puntuació = 0 # Puntuació inicial de cada genoma

    xarxes = [] # Llista on es guardarà la xarxa neuronal que controla al genoma
    ge = [] # Llista per a emmagatzemar els genomes d'una generació 
    ocells = [] # Llista per a guardar a cada ocell d'una població

    # Guardem l'índex de cada genoma a la variable _, mentre 
    # que el mateix genoma es guardarà al variable genoma
    for _, genoma in genomes:

        # Creem cada xarxa neuronal que controlarà a cada genoma
        xarxa = neat.nn.FeedForwardNetwork.create(genoma, configuració)

        xarxes.append(xarxa) # Afegim la xarxa creada a la llista xarxes

        # Per a cada genoma generem un ocell concretant-li la seva 
        # coordenada X i Y i, després, ho agreguem a la llista ocells
        ocells.append(Ocell(200, 250)) 

        genoma.fitness = 0 # Valor inicial del fitness de cada genoma 
        ge.append(genoma) # Afegim a cada genoma a la llista ge

    # Creem el bucle while, el qual s'executarà sempre quan partida sigui True
    while partida:

        # Establim els FPS del joc, o sigui, 30 fotos per segon
        clock.tick(30) 

        # Obtenim les accions que s'estan ocorrent a la finestra i ho 
        # guardem a la variable event
        for event in pygame.event.get():
            # Mirem si el tipus d'acció de event és igual que la de sortir
            if event.type == pygame.QUIT:
                # En el cas que sigui cert, tancarem la finestra
                pygame.quit() 
                quit()

        # Creem la variable columna_índex i tindrà un valor inicial de 0
        columna_índex = 0 

        # Mirem si queden ocells vius o no
        if len(ocells) > 0:

            # Veiem si els ocells ha passat o no per la primera columna
            if ocells[0].x > (columnes[0].x + columnes[0].COLUMNA_ADALT.get_width()):
                # En el cas que sigui cert, farem que columna_índex sigui 1 
                columna_índex = 1

        # En el cas que no hi quedin més ocell a la partida 
        # fem que la variable partida sigui False
        else: 
            partida = False 

        # Guardem l'índex de cada ocell al variable índex 
        # i els mateixos ocells al variable ocell
        for índex, ocell in enumerate(ocells):

            # Per cada frame, sumem +0.1 al fitness del genoma 
            # emprant l'índex de l'ocell que el representa
            ge[índex].fitness += 0.1 

            # Fem que cada ocell es mogui a partir del mètode moviment()
            ocell.moviment() 

            # Activem la xarxa neuronal especificant-li les dades d'entrada
            output = xarxes[índex].activate((ocell.y, 
                                        abs(ocell.y - columnes[columna_índex].altura),
                                        abs(ocell.y - columnes[columna_índex].avall)))   
            
            # Mirem si el primer element de la llista output és major que 0.5
            if output[0] > 0.5:
                ocell.saltar() # En el cas que es compleixi això, l'ocell 
                # saltarà a través del mètode saltar() 

        # Creem la llista eliminar_columnes per tal d'agregar 
        # aquelles columnes que s'hagin sortit de la finestra
        eliminar_columnes = [] 

        # Guardem les columnes a la variable columna
        for columna in columnes:

            # Emmagatzemem l'índex de cada ocell al variable 
            # índex i a cada un d'aquest al variable ocell
            for índex, ocell in enumerate(ocells):

                # Emprem el mètode col·lisió() de la classe Columna per 
                # a veure si els ocells s'han xocat o no amb les columnes
                if columna.col·lisió(ocell):

                    # En el cas que això sigui veritabler, restem 
                    # -1 al valor del fitness d'aquell genoma
                    ge[índex].fitness -= 1 

                    # Eliminem a l'ocell que s'ha xocat de la llista ocells
                    ocells.pop(índex) 

                    # Suprimim la xarxa neuronal que el controla de la 
                    # llista xarxes
                    xarxes.pop(índex)
                    
                    # Abolim al genoma que aquest ocell estava representant 
                    # de la llista ge
                    ge.pop(índex) 

                # Veiem si l'ocell ha passat o no per la columna en 
                # funció de la seva coordenada X i la de la columna
                if not columna.passat and (ocell.x > columna.x): 

                    # En el cas que es compleixi això, farem que l'atribut 
                    # self.passat d'aquesta columna sigui True
                    columna.passat = True

            # Mirem si la columna s'ha sortit o no de la finestra
            if columna.x + columna.COLUMNA_ADALT.get_width() < 0:
                # En el cas que sigui cert, agregarem aquesta 
                # columna a la llista eliminar_columnes
                eliminar_columnes.append(columna)
 
            # Fem que cada element de la llista columnes es mogui
            columna.moviment() 

        # Mirem si l'atribut self.passat de la columna que s'està 
        # veient és True o False
        if columna.passat: 

            # En el cas que sigui True, li sumarem +1 a la puntuació
            puntuació += 1 

            # Obtenim cada genoma de la llista ge i ho guardem a la 
            # variable genoma
            for genoma in ge:

                # Sumem +5 al valor del seu fitness
                genoma.fitness += 5 

            # Afegim una altra columna especificant-li la seva coordenada 
            # X a la classe Columna i ho agreguem a la llista columnes
            columnes.append(Columna(600))

        # Guardem cada element de la llista eliminar_columnes 
        # en la variable eliminar
        for eliminar in eliminar_columnes:

            # Suprimim aquest element de la llista columnes
            columnes.remove(eliminar) 

        # Guardem els índexs i els ocells als variables 
        # índex i ocell respectivament
        for índex, ocell in enumerate(ocells):

            # Mirem si cada ocell s'ha xocat o no amb les dues bases 
            # o si s'ha sortit per la part superior de la finestra
            if ocell.y + ocell.imatge.get_height() >= 500 or ocell.y < 0: 

                # En el cas que sigui cert, restem -1 al fitness 
                # d'aquell genoma 
                ge[índex].fitness -= 1 

                # Eliminem aquest ocell de la llista ocells
                ocells.pop(índex) 
                
                # Abolim la seva xarxa neuronal de la llista xarxes
                xarxes.pop(índex) 

                # Suprimim el genoma de la llista ge
                ge.pop(índex) 

        # Fem que les dues bases es moguin
        bases.moviment() 

        # Passem les coses que volem dibuixar a la funció dibuixar_elements
        dibuixar_elements(finestra, ocells, columnes, bases, puntuació, GEN) 

# Creem la funció importar() i rebrà la variable 
# configuració_ruta com a paràmetre
def importar(configuració_ruta):
   
    # Importem les '5 seccions' del fitxer de configuració i ho guardem a la variable 
    # configuració
    configuració = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                      neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                      configuració_ruta)

    # Obtenim el nombre d'individus d'una generació 
    # i ho guardem a la variable població
    població = neat.Population(configuració)

    # Fem que en la consola ens surti informacions 
    # detallades de cada generació
    població.add_reporter(neat.StdOutReporter(True)) 

    # Establim que tindrem 50 generacions i que emprarem la
    # funció main() per als genomes d'una població
    població.run(main, 50) 

if __name__ == '__main__':

    # Obtenim la ruta actual on es troba el nostre codi
    local_ruta = os.path.dirname(__file__) 

    # Obtenim la ruta del fitxer de configuració
    configuració_ruta = os.path.join(local_ruta, "config.txt") 

    # Li donem la ruta del fitxer de 
    # configuració a la funció importar()
    importar(configuració_ruta) 
