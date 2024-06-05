from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._clientiMaxBest = 0
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()



    def worstCase(self, nerc, maxY, maxH):
        self.loadEvents(nerc)

        parziale = []

        self.ricorsione(parziale, maxY, maxH, 0)
        pass
    def ricorsione(self, parziale, maxY, maxH, pos):
        if self.sumDurata(parziale)/60/60 >= maxH:
            return

        if self.countCustomers(parziale) > self._clientiMaxBest:
            self._solBest = parziale[:]
            self._clientiMaxBest = self.countCustomers(parziale)

        i = pos
        for e in self._listEvents[pos:]:
            parziale.append(e)
            if self.getRangeAnni(parziale) > maxY:
                parziale.remove(e)
                return
            i+=1
            self.ricorsione(parziale, maxY, maxH, i)
            parziale.remove(e)

    def getRangeAnni(self, parziale):
        if len(parziale) < 2:
            return 0

        first = parziale[0].date_event_began
        last = parziale[-1].date_event_finished
        return int(last.year - first.year)

    def countCustomers(self, parziale):
        if len(parziale) == 0:
            return 0
        numCostumers = 0
        for e in parziale:
            numCostumers += e.customers_affected
        return numCostumers

    def sumDurata(self, parziale):
        if len(parziale) == 0:
            return 0
        sum = 0
        for e in parziale:
            sum += self.durata(e)
        return sum

    def durata(self, e):
        return (e.date_event_finished - e.date_event_began).total_seconds()

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc