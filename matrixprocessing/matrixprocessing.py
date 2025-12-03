# 1. Розмір матриці
def read_matrix_size(prompt="Enter matrix size: "):
    while True:
        try:
            data = input(prompt).strip().split()
            if len(data) != 2:
                raise ValueError
            n, m = int(data[0]), int(data[1])
            if n <= 0 or m <= 0:
                raise ValueError
            return n, m
        except ValueError:
            print("Incorrect size. Try again.")

# 2. Зчитування матриці
def read_matrix(n, m, prompt="Enter matrix:"):
    print(prompt)
    matrix = []
    for _ in range(n):
        while True:
            try:
                row = input("> ").strip().split()
                if len(row) != m:
                    raise ValueError
                new_row = []
                for x in row:
                    if "." in x or "e" in x.lower():
                        new_row.append(float(x))
                    else:
                        new_row.append(int(x))
                matrix.append(new_row)
                break
            except ValueError:
                print("Incorrect row. Try again.")
    return matrix

# 3. Вивід матриці
def print_matrix(mat, prefix="The result is:"):
    print(prefix)
    for row in mat:
        row_to_print = []
        for x in row:
            if isinstance(x, float) and x.is_integer():
                row_to_print.append(int(x))
            else:
                row_to_print.append(round(x, 2))
        print(*row_to_print)

# 4. Операції з матрицями
def add_matrices(A, B):
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return None
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def multiply_by_constant(A, c):
    return [[A[i][j] * c for j in range(len(A[0]))] for i in range(len(A))]


def multiply_matrices(A, B):
    if len(A[0]) != len(B):
        return None
    n, m, p = len(A), len(A[0]), len(B[0])
    result = [[0 for _ in range(p)] for _ in range(n)]
    for i in range(n):
        for j in range(p):
            for k in range(m):
                result[i][j] += A[i][k] * B[k][j]
    return result

# 5. Транспонування
def transpose_main_diagonal(A):
    n, m = len(A), len(A[0])
    return [[A[j][i] for j in range(n)] for i in range(m)]


def transpose_side_diagonal(A):
    n, m = len(A), len(A[0])
    result = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(n):
        for j in range(m):
            result[m - 1 - j][n - 1 - i] = A[i][j]
    return result


def transpose_vertical(A):
    return [row[::-1] for row in A]


def transpose_horizontal(A):
    return A[::-1]

# 6. Детермінант
def determinant(A):
    n = len(A)
    if n != len(A[0]):
        raise ValueError("Determinant can only be calculated for square matrices")
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0]*A[1][1] - A[0][1]*A[1][0]
    det = 0
    for c in range(n):
        minor = [row[:c] + row[c+1:] for row in A[1:]]
        det += ((-1)**c) * A[0][c] * determinant(minor)
    return det

# 7. Зворотна матриця
def inverse_matrix(A):
    n = len(A)
    if n != len(A[0]):
        raise ValueError("Inverse can only be calculated for square matrices")
    det = determinant(A)
    if det == 0:
        return None

    cofactors = []
    for i in range(n):
        row = []
        for j in range(n):
            minor = [A[r][:j] + A[r][j+1:] for r in range(n) if r != i]
            cofactor = ((-1) ** (i + j)) * determinant(minor)
            row.append(cofactor)
        cofactors.append(row)

    adj = transpose_main_diagonal(cofactors)
    inverse = [[adj[i][j]/det for j in range(n)] for i in range(n)]
    return inverse

# 8. Головне меню
while True:
    print("""
1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit
""")
    choice = input("Your choice: > ").strip()
    if not choice.isdigit():
        print("Incorrect option.")
        continue
    choice = int(choice)

    if choice == 0:
        break

    elif choice == 1:
        n1, m1 = read_matrix_size("Enter size of first matrix: > ")
        A = read_matrix(n1, m1, "Enter first matrix:")
        n2, m2 = read_matrix_size("Enter size of second matrix: > ")
        B = read_matrix(n2, m2, "Enter second matrix:")
        result = add_matrices(A, B)
        if result is None:
            print("The operation cannot be performed.")
        else:
            print_matrix(result)

    elif choice == 2:
        n, m = read_matrix_size("Enter size of matrix: > ")
        A = read_matrix(n, m, "Enter matrix:")
        while True:
            try:
                c = input("Enter constant: > ").strip()
                c = float(c) if "." in c or "e" in c.lower() else int(c)
                break
            except ValueError:
                print("Incorrect constant. Try again.")
        result = multiply_by_constant(A, c)
        print_matrix(result)

    elif choice == 3:
        n1, m1 = read_matrix_size("Enter size of first matrix: > ")
        A = read_matrix(n1, m1, "Enter first matrix:")
        n2, m2 = read_matrix_size("Enter size of second matrix: > ")
        B = read_matrix(n2, m2, "Enter second matrix:")
        result = multiply_matrices(A, B)
        if result is None:
            print("The operation cannot be performed.")
        else:
            print_matrix(result)

    elif choice == 4:
        print("""
1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line
""")
        option = input("Your choice: > ").strip()
        if not option.isdigit() or not (1 <= int(option) <= 4):
            print("Incorrect option.")
            continue
        option = int(option)
        n, m = read_matrix_size("Enter matrix size: > ")
        A = read_matrix(n, m, "Enter matrix:")
        if option == 1:
            result = transpose_main_diagonal(A)
        elif option == 2:
            result = transpose_side_diagonal(A)
        elif option == 3:
            result = transpose_vertical(A)
        else:
            result = transpose_horizontal(A)
        print_matrix(result)

    elif choice == 5:
        n, m = read_matrix_size("Enter matrix size: > ")
        if n != m:
            print("The operation cannot be performed.")
            continue
        A = read_matrix(n, m, "Enter matrix:")
        print("The result is:")
        print(determinant(A))

    elif choice == 6:
        n, m = read_matrix_size("Enter matrix size: > ")
        if n != m:
            print("This matrix doesn't have an inverse.")
            continue
        A = read_matrix(n, m, "Enter matrix:")
        result = inverse_matrix(A)
        if result is None:
            print("This matrix doesn't have an inverse.")
        else:
            print_matrix(result)

    else:
        print("Incorrect option.")
