from app.models.crime_stats import DistrictCrimeStats


class CrimeStatsBuilder:
    def __init__(self):
        self._data = {
            "district_ubigeo": None,
            "district_name": None,
            "total_incidents_count": 0,
            "violent_incidents_count": 0,
            "weighted_crime_rate": 0.0,
        }

    def with_ubigeo(self, ubigeo: str):
        self._data["district_ubigeo"] = ubigeo
        return self

    def with_name(self, name: str):
        self._data["district_name"] = name
        return self

    def with_total_incidents(self, total: int):
        self._data["total_incidents_count"] = total
        return self

    def with_weighted_rate(self, rate: float):
        self._data["weighted_crime_rate"] = rate
        return self

    def with_violent_incidents(self, violent_count: int):
        self._data["violent_incidents_count"] = violent_count
        return self

    def build(self) -> DistrictCrimeStats:
        return DistrictCrimeStats(
            district_ubigeo=self._data["district_ubigeo"],
            district_name=self._data["district_name"],
            total_incidents_count=self._data["total_incidents_count"],
            violent_incidents_count=self._data["violent_incidents_count"],
            weighted_crime_rate=self._data["weighted_crime_rate"],
        )
