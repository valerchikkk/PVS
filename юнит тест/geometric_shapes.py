class GeometricFigure():
    def area(self):
        pass

class Triangle(GeometricFigure):
    def area(self, a, b, c):
        p = (a + b + c) // 2
        ploshad = (p * (p-a) * (p-b) * (p-c))**0.5
        return ploshad

class Rectangle(GeometricFigure):
    def area(self, a, b):
        return a * b
