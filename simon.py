

zaehlerzkeyscheduler = 0 #bracuhe ich im kesceduler habs als globale variable gemacht dass nichts schief gehen kann
def rotl16(x, n):
    return ((x << n) | (x >> (16 - n))) & 0xFFFF  #der vordere teil (x <<n) der funktion ist auch der erste teil des geschobenen bitstrings (er wird je nach position in der quaterround funktion weilter weschoben (deshalb n))
             ##bist werden um n nach vorne geschoben und fallen wegen dem & a, ende weg weil ich sage der "überlauf übre 16 bist soll weg                                       #der hintere teil ist der vordere teil der jetzt nach hinten rotiert wurde, durch das | werden die strings wieder zusammengemacht
                            #das sind die vorderen bist die ich hinten wieder anhängen muss, der string wird einfahc um die nagegebene menge nahc hinten verschoben und wenn ich z.b. mit 1 aufrufe bleibt nur der vorderste wert übrig (weil ich 16-n hab rotiere also um 15 nach hinten)
def rotl64(x, n):
    return ((x << n) | (x >> (64 - n))) & 0xFFFFFFFFFFFFFFFF


a = 0xF2A13937

def simonrundenfunktion32(block):

    links= block >> 16       #die bist wurden um 16 stellen also um 4 hex stellen nach rechts verschoben also sind nur noch die vorderen bytes da (linke hälfte)
    rechts = block - (links << 16)  #ich ziehe von dem block die linke hälfte im 4 nullen angehängt (wieder 16 weil 4 nullen hex im binär sytem sind 16) und ziehe das davon ab also recne ich 0xF2A13937 - 0xf2a10000


    links1 = rotl16(links,1)
    links8 = rotl16(links,8)
    links2 = rotl16(links,2)  #der ablauf der simon rundenfunktion
    links  = links1 & links8
    links = links ^ links2

    rechts = rechts << 16   ##ich hänge an rechts 16 nullen also 4 hex nullen weil rechts zu links wird und ich bei zusammenfügen quasi die jetzt hinzugefügten nullen durch den neu errechneten und teil ersetze durch ein | also oder
    block = rechts | links
    return block

def simoninnerefunktion128(block):  #()erklärungen sind für die 32 bit funktion weil ich die zum testenzu erst gemacht hab

    links= block >> 64#die bist wurden um 16 stellen also um 4 hex stellen nach rechts verschoben also sind nur noch die vorderen bytes da (linke hälfte)

    linksalt = links
    rechts = block - (links << 64)  #ich ziehe von dem block die linke hälfte im 4 nullen angehängt (wieder 16 weil 4 nullen hex im binär sytem sind 16) und ziehe das davon ab also recne ich 0xF2A13937 - 0xf2a10000


    links1 = rotl64(links,1)
    links8 = rotl64(links,8)
    links2 = rotl64(links,2)  #der ablauf der simon rundenfunktion
    links  = links1 & links8
    links = links ^ links2

    #rechts = rechts << 64   ##ich hänge an rechts 16 nullen also 4 hex nullen weil rechts zu links wird und ich bei zusammenfügen quasi die jetzt hinzugefügten nullen durch den neu errechneten und teil ersetze durch ein | also oder
    #block = rechts | links
    return links,rechts,linksalt
def simonrundenfunktion128(block,key):
    linksF,rechts,linksalt = simoninnerefunktion128(block)
    block = ((rechts^linksF^key)<<64) | (linksalt)
    return block
def keyscheduler(altkey,aktkey):
    aktkey = rotl64(aktkey, 64-3)  #muss eigentlich nach rechts rotieren hab aber kein  lust mir da ne funktion zu schreiben dasshalb so (3 nach rechts  = 61 nach links)
    aktkey = aktkey ^ rotl64(aktkey,63)
    c = 0xfffffffffffffffc
    z = [1,0,1,0,1,1,1,1,0,1,1,1,0,0,0,0,0,0,1,1,0,1,0,0,1,0,0,1,1,0,0,0,1,0,1,0,0,0,0,1,0,0,0,1,1,1,1,1,1,0,0,1,0,1,1,0,1,1,0,0,1,1]
    global zaehlerzkeyscheduler    #ich erhoehe meinen globalen zaehler so dass ich immer das richtige z vom key sceduler nehme
    zwert = z[zaehlerzkeyscheduler % 62]
    zaehlerzkeyscheduler += 1
    return altkey ^ aktkey ^ c ^ zwert


def simon(arrm, arrk,blockrunden):
    for i in range (len(arrm)):
        global zaehlerzkeyscheduler
        zaehlerzkeyscheduler = 0
        startkey = arrk[i]  #wenn ich mehrere nachrichtenblöcke verschluesseln will dann muss immer ein startkex mitgegeben weden
        startkeylinks = startkey >> 64
        startkeyrechts = startkey - (startkeylinks << 64)
        keyarr = [startkeyrechts, startkeylinks]  # der schluessel wird in ...
        for x in range(blockrunden):
            #die schluessel funktion (muss ich hier einbauen weil ich muss ja wenn ich den block verschlüssel wissen in welcher rund ich bin und das geht am einfachsten hier)
            try:
                arrm[i] = simonrundenfunktion128(arrm[i],keyarr[x])   #am anfang nimmt man einfach die schlüsselteile vom hauptschlüssel die mitgegeben werden, das ist der try teil danach nimmt man die rundenfunktion fuer den schluessel das macht er dann in dem except teil wenn das keyarr keine eintraege mehr hat

            except IndexError:
                keyarr.append(keyscheduler(keyarr[x-2],keyarr[x-1]))
                arrm[i] = simonrundenfunktion128(arrm[i], keyarr[x])

    return arrm






#----------------------------------------Aufgabe24---------------------------------------#k


m_array  = [0x11111111111111110102030405060708]
m_arrayverg = [0x11111111111111100102030405060708]
key= [0xFFEEDDCCBBAA99887766554433221100]   #ich hab jetzt schon den code fuer aufteilen der 128 bit bloeckte gschrieben und iwll ihn nicht aendern
auf24 = simon(m_array,key,2)
print(auf24)
auf242=simon(m_arrayverg,key,2)

for i in range(len(auf24)):
    print (hex(auf24[i]^auf242[i]))
    print("wert von 24:"+ str(auf24[i]))
    print("wert von 242: "+ str(auf242[i]))


#---------------------------------------Aufgabe25-----------------------------------------#
for x in range(2,40):
    print("----------------------------------Mit "+str(x)+" Runden-------------------------------")
    m_array  = [0x11111111111111110102030405060708]
    m_arrayverg = [0x11111111111111100102030405060708]
    key = [0xFFEEDDCCBBAA99887766554433221100]
    auf24 = simon(m_array,key,x)
    print(auf24)
    auf242=simon(m_arrayverg,key,x)

    for i in range(len(auf24)):
        print (hex(auf24[i]^auf242[i]))
        print("wert von 24: "+ str(auf24[i]))
        print("wert von 242:"+ str(auf242[i]))

    #unterschiedliche bits zaehlen
    binarr1 = format(auf24[0],'#1300b')
    binarr2 = format(auf242[0],'#1300b')

    bitsunterschied = 0
    for i in range(len(binarr1)):
        if binarr1[i] != binarr2[i]:
            bitsunterschied += 1

    print("der bitsunterschied betraegt: " + str(bitsunterschied))



key = [0x0f0e0d0c0b0a09080706050403020100]
klartext = [0x63736564207372656c6c657661727420]
geheimtext = simon(klartext, key, 68)
assert geheimtext[0] == 0x49681b1e1e54fe3f65aa832af84e0bbc
print("Testvektor Simon128/128 stimmt")

