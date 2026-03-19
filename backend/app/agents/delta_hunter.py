"""
Agent E: The Delta Hunter (Analyst Agent)
Function: Compares two vectors (V_A and V_B) and identifies feature shifts
This is the bridge between raw KataGo data and natural language
"""

import numpy as np
from typing import List, Tuple
from ..schemas.go_analysis import GroundTruthVector, DeltaVector


class DeltaHunterAgent:
    """
    The Delta Hunter - Difference Specialist
    Identifies and quantifies what changed between two moves
    """

    def __init__(self):
        # Thresholds for identifying significant changes
        self.winrate_significance = 0.02  # 2% change is significant
        self.lead_significance = 2.0  # 2 points is significant
        self.ownership_significance = 0.15  # 15% ownership change is significant

    def analyze_delta(
        self,
        vector_a: GroundTruthVector,
        vector_b: GroundTruthVector
    ) -> DeltaVector:
        """
        Compare two ground truth vectors and extract meaningful differences

        Args:
            vector_a: Ground truth for Move A (AI's best)
            vector_b: Ground truth for Move B (alternative)

        Returns:
            DeltaVector with quantified differences and natural language summary
        """

        # Calculate basic numerical deltas
        delta_winrate = vector_a.winrate - vector_b.winrate
        delta_lead = vector_a.lead - vector_b.lead

        # Calculate ownership difference map
        delta_ownership = self._calculate_ownership_delta(
            vector_a.ownership,
            vector_b.ownership
        )

        # Identify key differences in natural language
        key_differences = self._identify_key_differences(
            delta_winrate,
            delta_lead,
            delta_ownership,
            vector_a,
            vector_b
        )

        # Calculate overall magnitude of difference
        magnitude = self._calculate_magnitude(
            delta_winrate,
            delta_lead,
            delta_ownership
        )

        return DeltaVector(
            delta_winrate=delta_winrate,
            delta_lead=delta_lead,
            delta_ownership=delta_ownership,
            key_differences=key_differences,
            magnitude=magnitude
        )

    def _calculate_ownership_delta(
        self,
        ownership_a: List[List[float]],
        ownership_b: List[List[float]]
    ) -> List[List[float]]:
        """
        Calculate difference in territory ownership maps
        Returns 19x19 grid of ownership changes
        """

        delta = []
        for row_a, row_b in zip(ownership_a, ownership_b):
            delta_row = [a - b for a, b in zip(row_a, row_b)]
            delta.append(delta_row)

        return delta

    def _identify_key_differences(
        self,
        delta_winrate: float,
        delta_lead: float,
        delta_ownership: List[List[float]],
        vector_a: GroundTruthVector,
        vector_b: GroundTruthVector
    ) -> List[str]:
        """
        Identify the most important differences in natural language
        This is where we translate numbers into Go concepts
        """

        differences = []

        # 1. Winrate vs Territory Analysis
        # If winrate changes significantly but lead doesn't, or vice versa
        winrate_significant = abs(delta_winrate) >= self.winrate_significance
        lead_significant = abs(delta_lead) >= self.lead_significance

        if winrate_significant and not lead_significant:
            differences.append(
                "The main difference is not territory, but the safety and stability of groups"
            )
        elif lead_significant and not winrate_significant:
            differences.append(
                "The territorial difference is clear, but both moves are strategically similar"
            )
        elif winrate_significant and lead_significant:
            # Both changed - this is the expected case
            if abs(delta_winrate) > 0.05:  # >5% is large
                differences.append(
                    f"Strong positional advantage of {abs(delta_winrate) * 100:.1f}% winrate"
                )

        # 2. Analyze ownership map to find regional differences
        regions = self._analyze_ownership_regions(delta_ownership)

        if regions:
            differences.append(regions)

        # 3. Strategic direction analysis
        # Look at principal variations to understand strategic intent
        if len(vector_a.move_sequence) > 0 and len(vector_b.move_sequence) > 0:
            strategic_diff = self._analyze_strategic_direction(
                vector_a.move_sequence,
                vector_b.move_sequence
            )
            if strategic_diff:
                differences.append(strategic_diff)

        # 4. Thickness vs Territory trade-off
        thickness_analysis = self._analyze_thickness_tradeoff(
            delta_lead,
            delta_winrate
        )
        if thickness_analysis:
            differences.append(thickness_analysis)

        return differences if differences else ["Positional difference"]

    def _analyze_ownership_regions(
        self,
        delta_ownership: List[List[float]]
    ) -> str:
        """
        Identify specific coordinates where ownership changed significantly
        Returns concrete tactical information with coordinates
        """

        # Find all points with significant ownership change
        significant_changes = []

        for row in range(len(delta_ownership)):
            for col in range(len(delta_ownership[row])):
                change = delta_ownership[row][col]

                if abs(change) >= self.ownership_significance:
                    # Convert to Go coordinates (A-T, skip I)
                    col_letter = self._coord_to_letter(col)
                    row_number = 19 - row  # Invert row (0 -> 19, 18 -> 1)
                    coord = f"{col_letter}{row_number}"

                    significant_changes.append({
                        'coord': coord,
                        'change': change,
                        'row': row,
                        'col': col
                    })

        if not significant_changes:
            return ""

        # Cluster nearby changes into regions
        clusters = self._cluster_changes(significant_changes)

        # Generate tactical descriptions
        descriptions = []
        for cluster in clusters[:3]:  # Top 3 most significant clusters
            cluster_desc = self._describe_cluster(cluster)
            if cluster_desc:
                descriptions.append(cluster_desc)

        if descriptions:
            return "; ".join(descriptions)

        return ""

    def _coord_to_letter(self, col: int) -> str:
        """Convert column index to Go letter (A-T, skip I)"""
        if col < 8:
            return chr(ord('A') + col)
        else:
            return chr(ord('A') + col + 1)  # Skip I

    def _cluster_changes(self, changes: List[dict]) -> List[List[dict]]:
        """Group nearby coordinate changes into tactical clusters"""
        if not changes:
            return []

        # Sort by absolute change magnitude
        changes.sort(key=lambda x: abs(x['change']), reverse=True)

        clusters = []
        used = set()

        for point in changes:
            if point['coord'] in used:
                continue

            # Start a new cluster
            cluster = [point]
            used.add(point['coord'])

            # Find nearby points (within 2 intersections)
            for other in changes:
                if other['coord'] in used:
                    continue

                if abs(point['row'] - other['row']) <= 2 and abs(point['col'] - other['col']) <= 2:
                    cluster.append(other)
                    used.add(other['coord'])

            # Only keep clusters with significant total change
            total_change = sum(abs(p['change']) for p in cluster)
            if total_change >= 0.3 or len(cluster) >= 3:
                clusters.append(cluster)

        return clusters

    def _describe_cluster(self, cluster: List[dict]) -> str:
        """Generate tactical description of a cluster"""
        if not cluster:
            return ""

        # Get center coordinate
        center = cluster[0]['coord']
        total_change = sum(p['change'] for p in cluster)
        cluster_size = len(cluster)

        # Determine the type of change
        if total_change > 0.5:
            # Strong gain for Move A
            if cluster_size >= 4:
                return f"Region around {center} becomes strongly controlled (+{abs(total_change):.1f} ownership shift, {cluster_size} points affected)"
            else:
                return f"Territory at {center} secured"
        elif total_change < -0.5:
            # Strong loss for Move A (gain for Move B)
            if cluster_size >= 4:
                return f"Region around {center} becomes vulnerable ({abs(total_change):.1f} ownership lost, {cluster_size} points at risk)"
            else:
                return f"Weakness at {center}"

        return ""

    def _region_average(
        self,
        ownership: List[List[float]],
        r1: int, r2: int, c1: int, c2: int
    ) -> float:
        """Calculate average ownership in a rectangular region"""
        total = 0.0
        count = 0

        for r in range(r1, min(r2, len(ownership))):
            for c in range(c1, min(c2, len(ownership[r]))):
                total += ownership[r][c]
                count += 1

        return total / count if count > 0 else 0.0

    def _analyze_strategic_direction(
        self,
        pv_a: List[str],
        pv_b: List[str]
    ) -> str:
        """
        Analyze principal variations to understand strategic intent
        """
        # This is a simplified analysis
        # In production, you'd parse move coordinates and analyze patterns

        if len(pv_a) > 2 and len(pv_b) > 2:
            if pv_a[1] != pv_b[1]:
                return "Moves lead to fundamentally different strategic directions"

        return ""

    def _analyze_thickness_tradeoff(
        self,
        delta_lead: float,
        delta_winrate: float
    ) -> str:
        """
        Detect thickness vs territory trade-offs
        If lead changes little but winrate changes significantly,
        it suggests one move creates thickness (influence) over territory
        """

        # If winrate gain is disproportionate to territory gain
        if abs(delta_winrate) > 0.04 and abs(delta_lead) < 3.0:
            if delta_winrate > 0:
                return "Move A creates thickness and influence rather than immediate territory"
            else:
                return "Move B focuses on immediate territory over long-term influence"

        return ""

    def _calculate_magnitude(
        self,
        delta_winrate: float,
        delta_lead: float,
        delta_ownership: List[List[float]]
    ) -> float:
        """
        Calculate overall magnitude of difference
        Combines multiple metrics into a single score
        """

        # Normalize different metrics to 0-1 scale
        winrate_component = abs(delta_winrate) / 0.20  # Assume 20% is max meaningful diff
        lead_component = abs(delta_lead) / 20.0  # Assume 20 points is max meaningful diff

        # Ownership: Calculate standard deviation of changes
        flat_ownership = [val for row in delta_ownership for val in row]
        ownership_component = np.std(flat_ownership) if len(flat_ownership) > 0 else 0.0

        # Weighted combination
        magnitude = (
            winrate_component * 0.5 +
            lead_component * 0.3 +
            ownership_component * 0.2
        )

        return min(magnitude, 1.0)  # Cap at 1.0
