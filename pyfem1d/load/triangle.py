parameterValues = [25,0.008]
parameterNames = ['loading_per','magnitude']


def main(t):
    tper=parameterValues[0]
    magn=parameterValues[1]
    tloc=t
    while tloc>tper:
        tloc=tloc-tper
    qper=tper/4.
    if tloc <=qper:
        load = tloc
    elif tloc>qper and tloc<=2.*qper:
        load = qper - (tloc-qper)
    elif tloc>2.*qper and tloc<=3.*qper:
        load = -1.*(tloc-2.*qper)
    elif tloc>3.*qper and tloc<=tper:
        load = -1.*qper + (tloc - 3.*qper)
    return load*magn
