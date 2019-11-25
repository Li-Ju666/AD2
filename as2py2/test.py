def min_difference(u,r):
    A = [[None for i in range(len(r)+1)] for j in range(len(u)+1)]
    def min_dif(i, j):
        if A[i+1][j+1] is None:
            if i == 0 or j == 0:
                result = abs(i-j)
            else:
                result = min(
                    # min_dif(i-1, j)+R[u[i]]['-'],
                    # min_dif(i, j-1)+R['-'][r[j]],
                    # min_dif(i-1, j-1)+R[u[i]][r[j]]
                    min_dif(i - 1, j) + distance(u[i],'-'),
                    min_dif(i, j - 1) + distance('-', r[j]),
                    min_dif(i - 1, j - 1) + distance(u[i], r[j])
                )
            A[i+1][j+1] = result
        else: result = A[i+1][j+1]
        return result
    A[len(u)][len(r)] = min_dif(len(u)-1, len(r)-1)
    return A[len(u)][len(r)]

def distance(i, j):
    if i == j:
        result = 0
    else: result = 1
    return result

print(min_difference('dinamck','dynamic'))