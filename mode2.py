from landsites import Land
from typing import Union

class Mode2Navigator:
    """
    Student-TODO: short paragraph as per
    https://edstem.org/au/courses/14293/lessons/46720/slides/318306
    """

    def __init__(self, n_teams: int) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        raise NotImplementedError()

    def add_sites(self, sites: list[Land]) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        raise NotImplementedError()

    def simulate_day(self, adventurer_size: int) -> list[Union[tuple[Land, int], None]]:
        """
        Student-TODO: Best/Worst Case
        """
        raise NotImplementedError()
