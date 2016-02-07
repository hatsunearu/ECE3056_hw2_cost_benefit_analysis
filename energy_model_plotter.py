import matplotlib.pyplot as plt
import subprocess, math, sys

# hatsunearu
# Auxillary script for ECE 3056
# Assignment: compute the reconstruction error of a DCT'd image and the number of operations vs. neglected higher frequency terms

def normalized_discrete_derivative(x, y):
    out = []
    last_y = y[0]
    last_x = x[0]
    for x,y in zip(x[1:], y[1:]):
        dy = y - last_y
        dx = x - last_x
        out.append(dy / dx)

    return out

def main(filename):
    l = []
    for i in range(0, 255):
        p = subprocess.Popen(['./EnergyModel', filename, '/dev/null', str(i), '39'], stdout=subprocess.PIPE)
        s = p.stdout.read()
        l.append(map(float, s.split()))

    k = map(lambda x: x[0], l)
    error = map(lambda x: x[1], l)
    accuracy = map(lambda x: 100-x[1], l)
    energy = map(lambda x: x[2], l)

    fig, ax1 = plt.subplots()

    # ax1.plot(k, error)
    # ax1.set_xlabel('Neglected DCT terms')
    # ax1.set_ylabel('Reconstruction Error (%)')

    # ax2 = ax1.twinx()
    # ax2.plot(k, energy, 'r')
    # ax2.set_ylabel('Energy Used (fJ)')

    marginal_benefit = normalized_discrete_derivative(energy, accuracy)
    plt.plot(energy[0:-1], marginal_benefit)
    plt.xlabel("Energy used (fJ)")
    plt.ylabel("Marginal accuracy benefit (% per fJ)")

    best_energy = energy[marginal_benefit.index(min(marginal_benefit))]
    ind = energy.index(best_energy)
    print "Optimal Values:"
    print "K: %d" % (k[ind],)
    print "Accuracy: %.2f %%" % (accuracy[ind],)
    print "Energy: %d fJ" % (energy[ind],)

    plt.show()

if __name__ == "__main__":
    main(str(sys.argv[1]))
