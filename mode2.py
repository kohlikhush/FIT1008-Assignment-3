from landsites import Land
from typing import Union, List, Tuple
import heapq

class Mode2Navigator:
    """
    A class to simulate the qualifying game where multiple adventure teams compete for treasures.
    """

    def __init__(self, n_teams: int) -> None:
        """
        Initializes the Mode2Navigator object with the number of adventure teams.
        """
        self.n_teams = n_teams
        self.land_sites: List[Land] = []

    def add_sites(self, sites: List[Land]) -> None:
        """
        Adds land sites to the game.
        
        Time Complexity: O(N + S)
            - Where N is the number of existing land sites and S is the length of the additional land sites (input sites) to be added.
        """
        self.land_sites.extend(sites)

    def compute_score(self, land: Land, adventurer_size: int) -> Tuple[float, int, int]:
        """
        Computes the score, remaining adventurers, and reward for a land site.
        
        Time Complexity: O(1)
        """
        remaining_adventurers = max(0, adventurer_size - land.guardians)
        if remaining_adventurers > 0:
            reward = min((remaining_adventurers * land.gold) / land.guardians, land.gold)
        else:
            reward = 0
        score = 2.5 * remaining_adventurers + reward
        return score, remaining_adventurers, reward
    
    def calculate_score_data_structure(self, adventurer_size: int) -> List[Tuple[float, Land]]:
        """
        Create a max-heap data structure for land sites based on their score.
        
        Time Complexity: O(N)
            - Building the heap from the list of land sites takes O(N) time.
        """
        heap_data = [(-self.compute_score(site, adventurer_size)[0], site) for site in self.land_sites]
        heapq.heapify(heap_data)
        return heap_data

    def simulate_day(self, adventurer_size: int) -> List[Union[Tuple[Land, int], None]]:
        """
        Simulates a day of the game.
        
        Time Complexity: O(N + K log(N))
            - Building the initial heap takes O(N).
            - Each of the K teams' heap operations take O(log(N)), resulting in O(K log(N)).
        """
        # Create a max-heap based on the gold value of the land sites, adding index for tie-breaking
        heap_data = [(-site.gold, i, site) for i, site in enumerate(self.land_sites)]
        heapq.heapify(heap_data)

        results = []
        for _ in range(self.n_teams):
            if heap_data:
                # Choose the land site with the highest gold value
                _, _, best_site = heapq.heappop(heap_data)
                score, remaining_adventurers, reward = self.compute_score(best_site, adventurer_size)
                results.append((best_site, remaining_adventurers))
                # Update land site details
                best_site.gold -= reward
                best_site.guardians -= min(adventurer_size, best_site.guardians)
                # If the site still has gold or guardians left, push it back into the heap
                if best_site.gold > 0 and best_site.guardians > 0:
                    heapq.heappush(heap_data, (-best_site.gold, _, best_site))
            else:
                # If no land sites left, append None and 0 adventurers
                results.append((None, 0))
        
        return results