
class A:
    def __init__(self):
        print("Soy la Clase A")

    def a(self):
        print("Este método lo heredo de la clase A")


class B:
    def __init__(self):
        print("Soy la clase B")

    def b(self):
        print("Este método lo heredo de la clase B")


class C(A, B):
    def __init__(self):
        print("Soy la clase C")


x = A()
y = B()
z = C()

z.a()
z.b()

# Revisa si C es una subclase de B
print(issubclass(C, B))

# Revisa si un objeto es instancia de una clase
print(isinstance(x, C))
