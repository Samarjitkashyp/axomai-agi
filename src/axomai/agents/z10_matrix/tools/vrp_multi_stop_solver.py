"""
Z10 Matrix - Multi-Stop Vehicle Routing Problem (VRP / 2-Opt TSP) Solver.
Uses Nearest-Neighbor + 2-Opt combinatorial local search optimization
to find the shortest multi-stop delivery sequence across regional hubs,
quantifying exact deadhead km and diesel cost savings vs naive ordering.
"""

from typing import Dict, Any, List, Tuple
from axomai.agents.z10_matrix.tools.route_optimizer import route_optimizer, haversine_distance_km


class VrpMultiStopSolver:
    """Combinatorial Multi-Stop Fleet Routing & 2-Opt Sequence Optimizer."""

    def _dist(self, c1: Tuple[float, float], c2: Tuple[float, float]) -> float:
        return round(haversine_distance_km(c1[0], c1[1], c2[0], c2[1]) * 1.28, 1)

    def _total_route_km(self, order: List[int], matrix: List[List[float]]) -> float:
        total = 0.0
        for i in range(len(order) - 1):
            total += matrix[order[i]][order[i + 1]]
        return round(total, 1)

    def solve_multi_stop_sequence(
        self,
        origin: str,
        destinations: List[str],
        diesel_price_inr: float = 91.5,
        mileage_km_per_l: float = 4.2
    ) -> Dict[str, Any]:
        """
        Solves optimal visit sequence starting at `origin` and visiting all `destinations`
        using Nearest Neighbor initialization followed by 2-Opt local search.
        """
        nodes = [origin.title()] + [d.title() for d in destinations if d.lower() != origin.lower()]
        coords = []
        valid_nodes = []
        for n in nodes:
            c = route_optimizer.geocode_city(n)
            if c:
                coords.append(c)
                valid_nodes.append(n)

        n_cnt = len(valid_nodes)
        if n_cnt <= 2:
            d_km = self._dist(coords[0], coords[1]) if n_cnt == 2 else 0.0
            return {
                "vrp_algorithm": "DIRECT_CORRIDOR (<= 2 Nodes)",
                "optimal_sequence": valid_nodes,
                "naive_distance_km": d_km,
                "optimized_distance_km": d_km,
                "distance_saved_km": 0.0,
                "fuel_savings_inr": 0.0
            }

        # Build NxN road-circuity distance matrix
        matrix = [[0.0] * n_cnt for _ in range(n_cnt)]
        for i in range(n_cnt):
            for j in range(n_cnt):
                if i != j:
                    matrix[i][j] = self._dist(coords[i], coords[j])

        naive_order = list(range(n_cnt))
        naive_km = self._total_route_km(naive_order, matrix)

        # Nearest Neighbor starting from node 0 (origin)
        unvisited = set(range(1, n_cnt))
        nn_order = [0]
        while unvisited:
            last = nn_order[-1]
            nxt = min(unvisited, key=lambda x: matrix[last][x])
            nn_order.append(nxt)
            unvisited.remove(nxt)

        # 2-Opt local search improvement
        best_order = nn_order[:]
        improved = True
        while improved:
            improved = False
            best_dist = self._total_route_km(best_order, matrix)
            for i in range(1, n_cnt - 1):
                for j in range(i + 1, n_cnt):
                    candidate = best_order[:i] + best_order[i:j + 1][::-1] + best_order[j + 1:]
                    cand_dist = self._total_route_km(candidate, matrix)
                    if cand_dist < best_dist - 0.1:
                        best_order = candidate
                        best_dist = cand_dist
                        improved = True

        opt_km = self._total_route_km(best_order, matrix)
        saved_km = round(max(0.0, naive_km - opt_km), 1)
        fuel_saved_inr = round((saved_km / mileage_km_per_l) * diesel_price_inr, 2)

        return {
            "vrp_algorithm": "NEAREST_NEIGHBOR_PLUS_2OPT_TSP",
            "optimal_sequence": [valid_nodes[idx] for idx in best_order],
            "naive_distance_km": naive_km,
            "optimized_distance_km": opt_km,
            "distance_saved_km": saved_km,
            "efficiency_gain_pct": round((saved_km / max(naive_km, 1.0)) * 100.0, 1),
            "fuel_savings_inr": fuel_saved_inr
        }


vrp_solver = VrpMultiStopSolver()
