from math import radians, cos, sin, asin, sqrt

class HaversineCalculator:
    def __init__(self):
        pass

    def haversine(self, lon1, lat1, lon2, lat2):
        """
        Calculates the distance between two points on Earth given their longitude and latitude in degrees.
        Returns the distance in meters.
        """
        # Convert from degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # Differences in longitude and latitude
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        # Haversine formula
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371000  # Radius of the Earth in meters
        return c * r

    def coordinatesInRange(self, coordinates1, coordinates2, radius):
        """
        Checks if the distance between two sets of coordinates is within the given radius.
        Returns True if within the radius, False otherwise.
        """
        distance = self.haversine(coordinates1['longitude'], coordinates1['latitude'], coordinates2['longitude'], coordinates2['latitude'])
        return (distance <= radius)

# Example usage
# haversine_calculator = HaversineCalculator()
