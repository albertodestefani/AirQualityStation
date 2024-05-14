from math import radians, cos, sin, asin, sqrt

class HaversineCalculator:
    def __init__(self):
        pass

    def haversine(self, lon1, lat1, lon2, lat2):
        """
        Calcola la distanza tra due punti sulla Terra data la loro longitudine e latitudine in gradi.
        Restituisce la distanza in metri.
        """
        # Conversione da gradi a radianti
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # Differenze di longitudine e latitudine
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        # Formula di Haversine
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371000  # Raggio della Terra in metri
        return c * r

    def coordinateInRange(self, coordinates1, coordinates2, raggio):
        distanza = self.haversine(coordinates1['longitude'], coordinates1['latitude'], coordinates2['longitude'], coordinates2['latitude'])
        return (distanza <= raggio)

# Esempio di utilizzo
haversine_calculator = HaversineCalculator()

