import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np

from scripts.backend.battleboard.topology.discrete_topology import Tiling


class ProceduralGenerator(object):
    def __init__(self, tiling:Tiling, polygon_vertices, polygon_orientation, *args, **kwargs):
        self.tiling = tiling
        self.polygon_vertices = polygon_vertices
        self.polygon_orientation = polygon_orientation

        self.mapping = {tile: 0 for tile in self.tiling}

    def generate(self, seed):
        np.random.seed(seed)
        for tile in self.mapping:
            self.mapping[tile] = np.random.choice([0, 1])

        return

    def plot(self):
        # https://stackoverflow.com/questions/26935701/ploting-filled-polygons-in-python
        fig = plt.figure(dpi=150)
        ax = fig.add_subplot(111, aspect='equal')
        patches = []
        for tile in self.tiling:
            color = .75 * self.mapping[tile]
            polygon = RegularPolygon(
                xy=self.tiling.to_cartesian(tile),
                numVertices=self.polygon_vertices,
                radius=self.tiling.tile_size,
                orientation=self.polygon_orientation,
                fc=(color, color, color, .5),
                ec=(0, 0, 0, 1),
                lw=1,
            )
            ax.add_artist(polygon)
            patches.append(polygon)
        # ax.add_collection(PatchCollection(patches))
        plt.xlim(1.1 * min(patch.xy[0] for patch in patches), 1.1 * max(patch.xy[0] for patch in patches))
        plt.ylim(1.1 * min(patch.xy[1] for patch in patches), 1.1 * max(patch.xy[1] for patch in patches))
        plt.show()


if __name__ == "__main__":
    from scripts.backend.battleboard.topology.wraparound_hex_grid import TwistedTorusHexTiling
    m = ProceduralGenerator(
        tiling=TwistedTorusHexTiling(board_radius=20, tile_size=1),
        polygon_vertices=6,
        polygon_orientation=2*np.pi/12,
    )
    m.generate(0)
    m.plot()
