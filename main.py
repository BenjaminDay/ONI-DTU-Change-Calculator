from data.resource_reader import Elements, State
from data.stats import StatsBuilder
from dotenv import load_dotenv
import math
import logging

logger = logging.getLogger(__name__)

load_dotenv()

"""
Todo:

get formulas imported - done
Recreate the example tested - done
recursively calculate the values to generate a finite set of data - done
get results - done
$$$ - kaching!
"""

def get_k(mode, k1, k2):
    if mode == "k_lowest":
        return min(k1, k2)

    elif mode == "k_geom":
        return math.sqrt(k1 * k2)

    elif mode == "k_avg":
        return 0.5*(k1 + k2)

    elif mode == "k_mult":
        return 0.5*k1*k2

def get_q_DTU(mode_k, mat1, mat2):
    T_diff = mat1.T - mat2.T
    if T_diff < 1:
        return 0
    #print("mode_k: ", mode_k)
    q_max1a = (T_diff / 4) * mat1.m * mat1.c
    q_max1b = (T_diff / 4) * mat2.m * mat2.c
    #print("T_diff: ", round(T_diff,2)," qmax: ",round(q_max1a,2), round(q_max1b,2))
    q_upperlimit = min(q_max1a, q_max1b)
    q_real = T_diff * 0.2 * mode_k * 1000 * 25
    #print("q_real: ", q_real)
    return min(q_real, q_upperlimit)

def main():
    elements = Elements()
    stats = StatsBuilder(elements)

    count = 0
    # thermium     = stats.of('thermium', State.SOLID).withMass(100).at(20.0).build()
    # superCoolant = stats.of('super coolant', State.LIQUID).withMass(800).at(-20.0).build()
    # print("starting thermium temp: ", round(thermium.T, 1), " starting superCoolant temp: ", round(superCoolant.T, 1))
    
    print("lead gas")
    conductor  = stats.of("lead", State.GAS).withMass(2000).at(4000.0).build()
    logger.info(f"thermal conductivity: {conductor.k}")
    logger.info(f"SHC: {conductor.c}")
    abyssalite = stats.of("abyssalite", State.SOLID).withMass(500).at(0.0).build()
    logger.info(f"thermal conductivity abyss: {abyssalite.k}")
    logger.info(f"SHC abyss: {abyssalite.c}")

    print("starting conductor temp: ", round(conductor.T, 1), " starting abyssalite temp: ", round(abyssalite.T, 1))
    q_DTU = 1

    mode_k = get_k("k_geom", conductor.k, abyssalite.k)

    #for i in range(0,5):
    while q_DTU>0.1:
        count+=1
        q_DTU = get_q_DTU(mode_k, conductor, abyssalite)
        # conductor.T -= conductor.tempChange(q_DTU)
        abyssalite.T += abyssalite.tempChange(q_DTU)
        if abyssalite.T > 3421.9:
            break

        logger.info(f"\tq_DTU: {round(q_DTU,1)} \tconductor temp: {round(conductor.T, 1)} \tabyssalite temp: {abyssalite.T}")

    print("time passed: ", count/5/60/10, "cycles")
    print("final conductor temp: ", round(conductor.T, 1), "final abyssalite temp: ", abyssalite.T)
    input("Enter to exit")
    
main()   

