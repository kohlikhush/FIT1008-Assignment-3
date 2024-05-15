from landsites import Land


class Mode1Navigator:
    """
    Navigator class for selecting land sites and optimizing rewards.
    """

    def __init__(self, sites: list[Land], adventurers: int) -> None:
        """
        Initializes the Mode1Navigator with the initial state of land sites and total adventurers.
        
        Complexity: O(N log N), where N is the number of land sites.
        """
        self.sites = self.merge_sort(sites)
        self.adventurers = adventurers

    def merge_sort(self, sites: list[Land]) -> list[Land]:
        """
        Sorts the list of land sites based on the ratio of guardians to reward using merge sort.
        """
        if len(sites) <= 1:
            return sites
        mid = len(sites) // 2
        left_half = sites[:mid]
        right_half = sites[mid:]
        left_sorted = self.merge_sort(left_half)
        right_sorted = self.merge_sort(right_half)
        return self.merge(left_sorted, right_sorted)

    def merge(self, left: list[Land], right: list[Land]) -> list[Land]:
        """
        Merges two sorted lists of land sites into a single sorted list.
        """
        merged = []
        left_index = right_index = 0
        while left_index < len(left) and right_index < len(right):
            if left[left_index].guardians / left[left_index].gold < right[right_index].guardians / right[right_index].gold:
                merged.append(left[left_index])
                left_index += 1
            else:
                merged.append(right[right_index])
                right_index += 1
        merged.extend(left[left_index:])
        merged.extend(right[right_index:])
        return merged


    def select_sites(self) -> list[tuple[Land, int]]:
        """
        Selects the land sites to attack and the number of adventurers to send to each site.
        
        Complexity: O(N) in the worst case, O(log N) in the best case.
        """
        selected_sites = []
        remaining_adventurers = self.adventurers

        # Iterate through sorted land sites
        for land in self.sites:
            # Calculate the number of adventurers to send
            adventurers_to_send = min(remaining_adventurers, land.guardians)
            selected_sites.append((land, adventurers_to_send))
            remaining_adventurers -= adventurers_to_send

            # Break if all adventurers are assigned
            if remaining_adventurers == 0:
                break

        return selected_sites

    def select_sites_from_adventure_numbers(self, adventure_numbers: list[int]) -> list[float]:
        """
        Calculates the maximum reward for different adventurer numbers.

        Complexity: O(A * N), where A is the length of adventure_numbers and N is the number of land sites.
        """
        max_rewards = []

        for adventurers in adventure_numbers:
            reward = 0
            remaining_adventurers = adventurers

            # Iterate through sorted land sites
            for land in self.sites:
                # Calculate the reward for the current land site
                r = land.get_gold()
                adventurers_to_send = min(remaining_adventurers, land.guardians)
                reward_from_site = min((adventurers_to_send * r)/land.get_guardians(), r)
                reward += reward_from_site
                remaining_adventurers -= adventurers_to_send

                # Break if all adventurers are assigned
                if remaining_adventurers == 0:
                    break

            max_rewards.append(reward)

        return max_rewards

    def update_site(self, land: Land, new_reward: float, new_guardians: int) -> None:
        """
        Updates the state of a land site with new reward and number of guardians.
        
        Complexity: O(log N), where N is the number of land sites.
        """
        # Update the reward and guardians of the specified land site
        land.gold = new_reward
        land.guardians = new_guardians
