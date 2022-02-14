import math

def getlength(products, **kwargs):
    try:
        rez = products.filter(**kwargs)
        try: return len(rez)
        except: return 1
    except Exception as e: return 0

def isfilterok(produs, filter, genuri, marimi) -> bool:
    if filter["stoc"]=="in" and produs.stoc<=0:
        return False
    if filter["stoc"]=="redus" and produs.pret.reducere<=0:
        return False
    if filter["pret_max"] is not None and produs.pret.pret_final>filter["pret_max"]:
        return False
    if produs.specificatii.spalaremasina==False and filter["ch_spalare"]==True:
        return False

    skip_gen = True
    _genuri = []
    for gen in genuri:
        skip_gen &= not gen[2]
        if gen[2]: _genuri.append(gen[0])
    if not skip_gen and produs.specificatii.gen not in _genuri:
        return False

    skip_marime = True
    _marimi = []
    for marime in marimi:
        skip_marime &= not marime[2]
        if marime[2]: _marimi.append(marime[0])
    if not skip_marime and produs.specificatii.marime not in _marimi:
        return False

    return True

def isLight(rgbColor=(0,128,255)):
    r, g, b, a = rgbColor
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
    if hsp>127.5 or a <= 0.3:
        return True
    return False


