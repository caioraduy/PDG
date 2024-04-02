from Abrupto import Abrupto
from Incremental import Incremental
from Recorrente import Recurring
from Gradual import Gradual

class Contexto:
    def __init__(self, p):
        self.p = p

    def abrupto(self):
        abrupto = Abrupto(self.p)
        abrupto.apply()

    def recurring(self):
        recurring = Recurring(self.p)
        recurring.apply()

    def incremental(self):
        incremental = Incremental(self.p)
        incremental.apply()

    def gradual(self):
        gradual = Gradual(self.p)
        gradual.apply()