class Vehiculo:

    def __init__(self, color, ruedas):
        self.color = color
        self.ruedas = ruedas

    def __str__(self):
        return "Color {0:}, {1:} ruedas".format(self.color, self.ruedas)d


class Coche(Vehiculo):

    def __init__(self, color, ruedas, velocidad, cilindrada):
        # Vehiculo.__init__(self, color, ruedas)
        # Con super se accede a los miembros de la clase Padre, no se usa el self
        super().__init__(color, ruedas)
        self.velocidad = velocidad
        self.cilindrada = cilindrada

    def __str__(self)
        z = "Color {0:}, {1:} ruedas, {2:} km/h, {3:} cilindrada"
        return  z.format(self.color, self.ruedas, self.velocidad, self.cilindrada)


x = Vehiculo("Rojo", 4)
print(x)

y = Coche("Verde", 4, 120, 1500)
print(y)
