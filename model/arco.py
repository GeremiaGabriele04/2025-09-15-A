from dataclasses import dataclass


@dataclass
class Arco:
    driverId1: int
    driverId2: int
    peso: int

    def __hash__(self):
        return hash((self.driverId1, self.driverId2))
    def __eq__(self, other):
        return self.driverId1 == other.driverId1 and self.driverId2 == other.driverId2


