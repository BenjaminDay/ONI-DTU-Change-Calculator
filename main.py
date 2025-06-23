import math
"""
Todo:

get formulas imported - done
Recreate the example tested - done
recursively calculate the values to generate a finite set of data - done
get results - done
$$$ - kaching!
"""

class Stats:
    def __init__(self, TC, SHC, mass, temp):
        self.k = TC #Thermal Conductivity
        self.c = SHC #Specific Heat Capacity
        self.m = mass #(kg)
        self.T = temp #starting(C)

def get_k(mode, k1, k2):
    if mode == "k_lowest":
        return min(k1, k2)

    elif mode == "k_geom":
        return math.sqrt(k1 + k2)

    elif mode == "k_avg":
        return 0.5*(k1 + k2)

    elif mode == "k_mult":
        return 0.5*k1*k2

def get_q_DTU(mode, mat1, mat2):
    T_diff = mat1.T - mat2.T
    if T_diff < 1:
        pass
    mode_k = get_k(mode, mat1.k, mat2.k)
    q_max1a = (T_diff / 4) * mat1.m * mat1.c
    q_max1b = (T_diff / 4) * mat2.m * mat2.c
    #print("T_diff: ", round(T_diff,2)," qmax: ",round(q_max1a,2), round(q_max1b,2))
    q_upperlimit = min(q_max1a, q_max1b)
    q_real = T_diff * 0.2 * mode_k * 1000
    return min(q_real, q_upperlimit)

def get_tempChange(q_DTU, mat):
    return (q_DTU / mat.c) / mat.m

def main():
    count = 0
    thermium = Stats(220, 0.622, 100, 20.0)
    superCoolant = Stats(9.460, 8.440, 800, -20.0)
    print("starting thermium temp: ", round(thermium.T, 1), " starting superCoolant temp: ", round(superCoolant.T, 1))
    q_DTU = 2

    while q_DTU>0.1:
        count+=1
        q_DTU = get_q_DTU("k_geom", thermium, superCoolant)
        thermium.T -= get_tempChange(q_DTU, thermium)
        superCoolant.T += get_tempChange(q_DTU, superCoolant)

        print("q_DTU: ", round(q_DTU,1), " thermium temp: ", round(thermium.T, 1), "superCoolant temp: ", round(superCoolant.T, 1))

    print("time passed: ", count/5, "seconds")
    
main()   

