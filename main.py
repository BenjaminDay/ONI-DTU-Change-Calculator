from data.resource_reader import Elements, State
from data.stats import StatsBuilder
from dotenv import load_dotenv
import math

load_dotenv()

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

    def tempChange(self, q_DTU):
        return(q_DTU / self.c) / self.m

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
        return 0
    mode_k = get_k(mode, mat1.k, mat2.k)
    q_max1a = (T_diff / 4) * mat1.m * mat1.c
    q_max1b = (T_diff / 4) * mat2.m * mat2.c
    #print("T_diff: ", round(T_diff,2)," qmax: ",round(q_max1a,2), round(q_max1b,2))
    q_upperlimit = min(q_max1a, q_max1b)
    q_real = T_diff * 0.2 * mode_k * 1000
    return min(q_real, q_upperlimit)

def main():
    elements = Elements()
    stats = StatsBuilder(elements)

    count = 0
    thermium     = stats.of('thermium', State.SOLID).withMass(100).at(20.0).build()
    superCoolant = stats.of('super coolant', State.LIQUID).withMass(800).at(-20.0).build()
    print("starting thermium temp: ", round(thermium.T, 1), " starting superCoolant temp: ", round(superCoolant.T, 1))
    q_DTU = 1

    while q_DTU>0.1:
        count+=1
        q_DTU = get_q_DTU("k_geom", thermium, superCoolant)
        thermium.T -= thermium.tempChange(q_DTU)
        superCoolant.T += superCoolant.tempChange(q_DTU)

        print("q_DTU: ", round(q_DTU,1), " thermium temp: ", round(thermium.T, 1), "superCoolant temp: ", round(superCoolant.T, 1))

    print("time passed: ", count/5, "seconds")
    
main()   

