def levenshtein(seq1, seq2, verbose=False):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = [[0 for col in range(size_y)] for row in range(size_x)]
    for x in range(size_x):
        matrix [x][0] = x
    for y in range(size_y):
        matrix [0][y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if verbose:
                print(seq1[x-1], seq2[y-1])
            if seq1[x-1] == seq2[y-1]:
                matrix [x][y] = min(
                    matrix[x-1][y] + 1,
                    matrix[x-1][y-1],
                    matrix[x][y-1] + 1
                )
            else:
                matrix [x][y] = min(
                    matrix[x-1][y] + 1,
                    matrix[x-1][y-1] + 1,
                    matrix[x][y-1] + 1
                )
    if verbose:
        display(matrix)
    return (matrix[size_x - 1][size_y - 1]), matrix

def display(mat):
    for row in mat:
        print(row)

def get_steps(seq1, seq2, output_file="affected_words.txt", verbose=False):
    val, mat = levenshtein(seq1, seq2)
    rows = len(mat) 
    cols = len(mat[0]) 
    r = rows - 1
    c = cols - 1

    substitutions = 0
    deletions = 0
    insertions = 0
    correct = 0
    with open(output_file, "a") as f:
        while r > 0 and c > 0:
            diag = mat[r-1][c-1]
            left = mat[r][c-1]
            up = mat[r-1][c]
            val = mat[r][c]
            
            if diag == min(left, min(up, diag)):
                if (seq1[r-1]) == (seq2[c-1]):
                    if verbose:
                        print("good", seq1[r-1], seq2[c-1])
                    f.write(" ".join(["good", seq1[r-1], seq2[c-1]]) + '\n')
                    correct += 1
                else:
                    if verbose:
                        print("swap", seq1[r-1], seq2[c-1])
                    f.write(" ".join(["swap", seq1[r-1], seq2[c-1]]) + '\n')
                    substitutions += 1
                r -= 1
                c -= 1  
            elif left == min(left, min(up, diag)):
                if verbose:
                    print("insert", seq2[c-1])
                f.write(" ".join(["insert", seq2[c-1]]) + '\n')
                insertions += 1
                c -= 1
            elif up == min(left, min(up, diag)):
                if verbose:
                    print("delete", seq1[r-1])
                f.write(" ".join(["delete", seq1[r-1]]) + '\n')
                deletions += 1
                r -= 1  
        while c > 0:
            c = c - 1
            if verbose:
                print("insert", seq2[c])
            f.write(" ".join(["insert", seq2[c]]) + '\n')
            insertions += 1
        while r > 0:
            r = r - 1
            if verbose:
                print("delete", seq1[r])
            f.write(" ".join(["delete", seq1[r]]) + '\n')
            deletions += 1
    return (substitutions, deletions, insertions, correct) 

def wer(S, D, I, C):
    N = S + D + C
    return (S + D + I) / N

#val, mat = levenshtein("text", "test")
#val, mat = levenshtein("text", "tekst")
"""val, mat = levenshtein(["text", "bla", "a", "b", "c"], ["tekst", "", "a", "x", "d", "c"])
display(mat)
print(get_steps(["text", "bla", "a", "b", "c"], ["tekst", "nj", "a", "x", "d", "c"], verbose=True))
"""
"""
val, mat = levenshtein(["a", "b", "c"], ["a"])
display(mat)
print(get_steps(["a", "b", "c"], ["a"], verbose=True))
"""
"""
s1 = "kina je razmjestila sedamsto ≈°est raketa na svojoj jugoistoƒНnoj obali"
s2 = "kine razmislila 706 raketa na svojoj jugoistoƒНnoj obali"
print(get_steps(s1.split(" "), s2.split(" "), verbose=True))
"""
