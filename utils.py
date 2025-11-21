# Funções

def gms_to_decimal(gms):
    """
    Função que transforma 410842N (41° 08' 42''N) em graus
    in: 410842N
    out: 41.145°

    """
    # Ex: "410842N"
    g = int(gms[0:2])     # graus
    m = int(gms[2:4])     # minutos
    s = int(gms[4:6])     # segundos
    hemi = gms[6]         # N, S, E, W

    decimal = g + m/60 + s/3600

    # hemisfério: S e W são negativos
    if hemi in ["S", "W"]:
        decimal = -decimal

    return decimal

# Listas

cod_rad = ["1387", "1111", "2661", 
           "3469A", "3194U", "4121", 
           "5402", "5973", "6325O", 
           "7178I", "9981A", "0201D"]
