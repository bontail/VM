import os.path
import random


def is_diagonally_dominant(A):
    n = len(A)
    for i in range(n):
        diag = abs(A[i][i])
        s = sum(abs(A[i][j]) for j in range(n)) - diag
        if diag < s:
            return False
    return True


def make_diagonally_dominant(A, b):
    n = len(A)

    used = [False] * n
    new_A = [None] * n
    new_b = [0] * n

    def backtrack(i):
        if i == n:
            return True

        for r in range(n):
            if not used[r]:
                diag = abs(A[r][i])
                s = sum(abs(A[r][j]) for j in range(n)) - diag

                if diag > s:
                    used[r] = True
                    new_A[i] = A[r]
                    new_b[i] = b[r]

                    if backtrack(i + 1):
                        return True

                    used[r] = False
        return False

    if backtrack(0):
        return new_A, new_b, True
    else:
        return A, b, False


def row_norm(A):
    return max(sum(abs(x) for x in row) for row in A)


def gauss_seidel(A, b, x, eps, M):
    n = len(A)

    for k in range(1, M + 1):
        delta_vec = [0] * n
        delta = 0

        for i in range(n):
            s = 0

            for j in range(i):
                s += A[i][j] * x[j]

            for j in range(i + 1, n):
                s += A[i][j] * x[j]

            x_new = (b[i] - s) / A[i][i]
            delta_vec[i] = abs(x_new - x[i])
            x[i] = x_new
            if delta_vec[i] > delta:
                delta = delta_vec[i]

        if delta < eps:
            return x, k, delta_vec

    return x, M, delta_vec


def input_console():
    n = int(input("Введите размерность n: "))

    print("Введите матрицу A:")
    A = [list(map(float, input().split())) for _ in range(n)]

    print("Введите вектор b:")
    b = list(map(float, input().split()))

    print("Введите начальное приближение x0:")
    x0 = list(map(float, input().split()))

    eps = float(input("Введите точность eps: "))
    M = int(input("Введите максимум итераций M: "))

    return A, b, x0, eps, M


def input_file(filename):
    with open(filename, "r") as f:
        n = int(f.readline())
        A = [list(map(float, f.readline().split())) for _ in range(n)]
        b = list(map(float, f.readline().split()))
        x0 = list(map(float, f.readline().split()))
        eps = float(f.readline())
        M = int(f.readline())

    return A, b, x0, eps, M


def input_generate():
    n = int(input("Введите n: "))
    A = []
    for l in range(n):
        line = []
        for column in range(n):
            line.append(random.randint(0, 10))
        line[l] = sum(line)
        A.append(line)
    b = [random.randint(0, 10) for _ in range(n)]
    x0 = [random.randint(0, 10) for _ in range(n)]
    eps = float(input("Введите точность eps: "))
    M = int(input("Введите максимум итераций M: "))
    return A, b, x0, eps, M


def main():
    print("1 — Ввод с клавиатуры")
    print("2 — Ввод из файла")
    print("3 — Генерация случайной матрицы")
    mode = input("Выбор: ")

    if mode == '1':
        A, b, x, eps, M = input_console()
    elif mode == '2':
        while True:
            filename = input("Введите имя файла: ")
            if os.path.exists(filename):
                if not os.access(filename, os.R_OK):
                    print("Нет доступа для чтения файла")
                    continue
                break
            print("Файла не существует")
        A, b, x, eps, M = input_file(filename)
    elif mode == '3':
        A, b, x, eps, M = input_generate()
    else:
        print("Неверное значение")
        return

    for row in A:
        if len(row) != len(A):
            print("Матрица должна быть квадратной")
            return

    if len(b) != len(A):
        print(f"Число неизвестных должно быть {len(A)}")
        return

    if len(x) != len(b):
        print(f"Число начальных значений должно быть {len(b)}")
        return

    if eps < 0:
        print("Точность должна быть положительной")
        return

    if M < 1:
        print("Количество итераций должно быть >= 1")
        return

    print("Проверка диагонального преобладания")

    if not is_diagonally_dominant(A):
        A, b, success = make_diagonally_dominant(A, b)

        if not success:
            print("Невозможно достичь диагонального преобладания")
            print(A)
            return
        else:
            print("Диагональное преобладание достигнуто перестановкой строк")
    else:
        print("Матрица обладает диагональным преобладанием")

    print("Норма матрицы:", row_norm(A))

    solution, iterations, errors = gauss_seidel(A, b, x, eps, M)

    print("Решение:")
    for i in range(len(solution)):
        print(f"x{i + 1} = {solution[i]:.6f}")

    print("Количество итераций:", iterations)

    print("Вектор погрешностей:")
    for i in range(len(errors)):
        print(f"|x{i}(k)-x{i}(k-1)| = {errors[i]:.6f}")


if __name__ == "__main__":
    main()
