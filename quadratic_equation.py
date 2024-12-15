def discriminant(a, b, c):
    """
    Функция для нахождения дискриминанта
    """
    # Ваш алгоритм
    return b ** 2 - 4*a*c


def quadratic_equation(a, b, c):
    """
    Функция для нахождения корней уравнения
    """
    d = discriminant(a, b, c)
    if d < 0:
        return None
    elif d == 0:
        x = (-b) / (2 * a)
        return x
    else:
        x = []
        x = [(-b + d**0.5) / (2 * a), (-b - d**0.5) / (2 * a)]
        # print(f'{x[0]} {x[1]}')
        return x


if __name__ == '__main__':
    print(quadratic_equation(1, 8, 15))
    print(quadratic_equation(1, -13, 12))
    print(quadratic_equation(-4, 28, -49))
    print(quadratic_equation(1, 1, 1))
