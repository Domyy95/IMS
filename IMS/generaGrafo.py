import random
import sys

if __name__ == '__main__':
    N = sys.argv[1]
    L = sys.argv[2]
    min_const = int (sys.argv[3])
    max_const = int (sys.argv[4])
    nome = sys.argv[5]

    const = []

    file = open(nome+'.txt', "w")
    file.write(N + ' ' + L + '\n')
    for i in range(0, int(L)):
        f = True
        ite = 0
        while f is True and ite < 10:
            l1 = random.randint(0, int(N) - 2)
            l2 = random.randint(l1 + 1, int(N) - 1)
            if((l1,l2) not in const):
                f = False
                const.append((l1,l2))
            ite = ite + 1

        r1 = random.randint(min_const, max_const)
        r2 = random.randint(min_const, max_const)
        r3 = random.randint(min_const, max_const)
        r4 = random.randint(min_const, max_const)

        file.write(str(l1) + '-' + str(l2) + ' ' + str(r1) + ' ' + str(r2) + ' ' + str(r3) + ' ' + str(r4) + '\n')

    file.close()
    print('file ' + nome + ' created')
