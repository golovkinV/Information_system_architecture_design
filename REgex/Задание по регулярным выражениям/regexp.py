def calculate(data, findall):
    matches = findall(r"([abc])([+-]?=)([abc])?([+-]?\d+)?")  # Если придумать хорошую регулярку, будет просто
    print(matches)
    for v1, s, v2, n in matches:  # Если кортеж такой структуры: var1, [sign]=, [var2], [[+-]number]
        if n == "":
            n = 0
        if s == "=":
            data[v1] = int(n) if v2 == "" else data[v2] + int(n)
        if s == "+=":
            data[v1] += int(n) if v2 == "" else data[v2] + int(n)
        if s == "-=":
            data[v1] -= int(n) if v2 == "" else data[v2] + int(n)
    return data
