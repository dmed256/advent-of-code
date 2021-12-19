from repo_utils import *

def run(problem):
    # --------------------------------------------------#
    # Step 0: Assembly                                  #
    # --------------------------------------------------#
    # #ip 2
    # seti 123 0 3      // 0
    # bani 3 456 3      // 1
    # eqri 3 72 3       // 2
    # addr 3 2 2        // 3
    # seti 0 0 2        // 4
    # seti 0 4 3        // 5
    # bori 3 65536 4    // 6
    # seti 1107552 3 3  // 7
    # bani 4 255 5      // 8
    # addr 3 5 3        // 9
    # bani 3 16777215 3 // 10
    # muli 3 65899 3    // 11
    # bani 3 16777215 3 // 12
    # gtir 256 4 5      // 13
    # addr 5 2 2        // 14
    # addi 2 1 2        // 15
    # seti 27 0 2       // 16
    # seti 0 2 5        // 17
    # addi 5 1 1        // 18
    # muli 1 256 1      // 19
    # gtrr 1 4 1        // 20
    # addr 1 2 2        // 21
    # addi 2 1 2        // 22
    # seti 25 3 2       // 23
    # addi 5 1 5        // 24
    # seti 17 3 2       // 25
    # setr 5 3 4        // 26
    # seti 7 4 2        // 27
    # eqrr 3 0 5        // 28
    # addr 5 2 2        // 29
    # seti 5 8 2        // 30

    # --------------------------------------------------#
    # Step 1: Replaced registers                        #
    # --------------------------------------------------#
    # r[3] = 123             // 0
    # r[3] = r[3] & 456      // 1
    # r[3] = r[3] == 72      // 2
    # IP = r[3] + IP         // 3
    # IP = 0                 // 4
    # r[3] = 0               // 5
    # r[4] = r[3] | 65536    // 6
    # r[3] = 1107552         // 7
    # r[5] = r[4] & 255      // 8
    # r[3] = r[3] + r[5]     // 9
    # r[3] = r[3] & 16777215 // 10
    # r[3] = r[3] * 65899    // 11
    # r[3] = r[3] & 16777215 // 12
    # r[5] = 256 > r[4]      // 13
    # IP = r[5] + IP         // 14
    # IP = IP + 1            // 15
    # IP = 27                // 16
    # r[5] = 0               // 17
    # r[1] = r[5] + 1        // 18
    # r[1] = r[1] * 256      // 19
    # r[1] = r[1] > r[4]     // 20
    # IP = r[1] + IP         // 21
    # IP = IP + 1            // 22
    # IP = 25                // 23
    # r[5] = r[5] + 1        // 24
    # IP = 17                // 25
    # r[4] = r[5]            // 26
    # IP = 7                 // 27
    # r[5] = r[3] == r[0]    // 28
    # IP = r[5] + IP         // 29
    # IP = 5                 // 30

    # --------------------------------------------------#
    # Step 2: Replace IP                                #
    # --------------------------------------------------#
    # C = 123       // 0 <--[ ? ]
    # C &= 456      // 1
    # C = C == 72   // 2
    # IP += C       // 3 ---[ 1 ]-->
    # IP = 0        // 4 ---[ ? ]-->
    # C = 0         // 5 <--[ 1 ]
    # D = C | 65536 // 6 <--[ B ]
    # C = 1107552   // 7 <--[ 5 ]
    # E = D & 255   // 8 <--[ A ]
    # C += E        // 9
    # C &= 16777215 // 10
    # C *= 65899    // 11
    # C &= 16777215 // 12
    # E = 256 > D   // 13
    # IP += E       // 14 ---[ 2 ]-->
    # IP += 1       // 15 ---[ 6 ]-->
    # IP = 27       // 16 <--[ 2 ]
    # E = 0         // 17 <--[ 6 ]
    # B = E + 1     // 18 <--[ 9 ]
    # B *= 256      // 19
    # B = B > D     // 20
    # IP += B       // 21 ---[ 3 ]-->
    # IP += 1       // 22 ---[ 7 ]-->
    # IP = 25       // 23 <--[ 3 ] [ 4 ]-->
    # E += 1        // 24 <--[ 8 ]
    # IP = 17       // 25 ---[ 9 ]-->
    # D = E         // 26 <--[ 4 ]
    # IP = 7        // 27 ---[ A ]-->
    # E = C == A    // 28
    # IP += E       // 29 END!!
    # IP = 5        // 30 ---[ B ]-->
    #
    # |----------+--------------------------|
    # |      dec |                      bin |
    # |----------+--------------------------|
    # |        4 |                      100 |
    # |        5 |                      101 |
    # |        7 |                      111 |
    # |       17 |                    10001 |
    # |       25 |                    11001 |
    # |       27 |                    11011 |
    # |       72 |                  1001000 |
    # |      123 |                  1111011 |
    # |      255 |                 11111111 |
    # |      256 |                100000000 |
    # |      456 |                111001000 |
    # |    65536 |        10000000000000000 |
    # |    65899 |        10000000101101011 |
    # |  1107552 |    100001110011001100000 |
    # | 16777215 | 111111111111111111111111 |
    # |----------+--------------------------|

    # --------------------------------------------------#
    # Step 3: Replace with binary                       #
    # --------------------------------------------------#
    # // Test
    # C = 123       // 0 <--[ 0 ]
    # C &= 456      // 1
    # C = C == 72   // 2
    # IP += C       // 3 ---[ 1 ]--> MAIN
    # IP = 0        // 4 ---[ 0 ]-->
    #
    # // MAIN()
    # C = 0                                    // 5
    # D = C | 65536 (10000000000000000)        // 6  <--[ I ]
    # C = 1107552 (100001110011001100000)      // 7
    # E = D & 255 (11111111)                   // 8  <--[ H ]
    # C += E                                   // 9
    # C &= 16777215 (111111111111111111111111) // 10
    # C *= 1107552 (10000000101101011)         // 11
    # C &= 16777215 (111111111111111111111111) // 12
    # E = 256 > D                              // 13
    # IP += E                                  // 14 ---[ A ]-->
    # IP += 1                                  // 15 ---[ B ]--> <--[ A[F] ]
    # IP = 27                                  // 16 ---[ C ]--> <--[ A[T] ]
    # E = 0                                    // 17 <--[ B ]
    # B = E + 1                                // 18 <--[ G ]
    # B *= 256 (100000000)                     // 19
    # B = B > D                                // 20
    # IP += B                                  // 21 ---[ D ]-->
    # IP += 1                                  // 22 ---[ E ]--> <--[ D[F] ]
    # IP = 25 (11001)                          // 23 ---[ F ]--> <--[ D[T] ]
    # E += 1                                   // 24
    # IP = 17 (10001)                          // 25 ---[ G ]-->
    # D = E                                    // 26
    # IP = 7 (111)                             // 27 ---[ H ]-->
    # E = C == A                               // 28 <--[ C ]
    # IP += E                                  // 29 END
    # IP = 5 (101)                             // 30 ---[ I ]-->

    # --------------------------------------------------#
    # Step 4: JS-formatted                              #
    # --------------------------------------------------#
    # do {
    #   D = C | 65536 (10000000000000000)
    #   C = 1107552 (100001110011001100000)
    #   do {
    #     E = D & 255 (11111111)
    #
    #     C += E
    #     C &= 16777215 (111111111111111111111111)
    #     C *= 1107552 (10000000101101011)
    #     C &= 16777215 (111111111111111111111111)
    #
    #     if (256 > D) {
    #       if (C == A) {
    #         return
    #       }
    #       goto 0
    #     }
    #
    #     for E in range(1, 10000000) {
    #       if ((256 * E) > D) {
    #         break
    #       }
    #     }
    #     D = E
    #   } while (true)
    # } while (true)

    # --------------------------------------------------#
    # Step 5: Python-formatted                          #
    # --------------------------------------------------#
    last_solution = None
    cache = set()

    C = 1107552
    D = 65536
    while True:
        C += D & 255
        C &= 16777215
        C *= 65899
        C &= 16777215

        if D >= 256:
            D >>= 8
            continue

        # Star 1: Find first solution
        if problem == 1:
            return C

        # Star 2: Find last solution
        #      -> Stop before a repeat to avoid an infinite loop
        if C in cache:
            return last_solution

        cache.add(C)

        last_solution = C

        D = C | 65536
        C = 1107552

run(1) | debug('Star 1') | eq(16134795)

run(2) | debug('Star 2') | eq(14254292)
