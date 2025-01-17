from dataclasses import dataclass


@dataclass
class LayerParams:
    scale: int
    orux_layer: int
    m_per_pixel: float
    tiff_filename: str = None
    tiff_url: str = None
    # pixel_per_tile: int = 400
    pixel_per_tile: int = 1000

    @property
    def name(self):
        return f"{self.scale:04d}"

    @property
    def m_per_tile(self) -> float:
        return self.pixel_per_tile * self.m_per_pixel

    def verify_m_per_pixel(self, m_per_pixel: float):
        assert isinstance(m_per_pixel, float)
        assert abs((m_per_pixel / self.m_per_pixel) - 1.0) < 0.001

    @property
    def valid_data(self) -> bool:
        # The 1:1Mio maps (50 m_per_pixel) has extremely large
        return self.m_per_pixel < 24


LIST_LAYERS = (
    # LayerParams(
    #     scale=5000,
    #     orux_layer=8,
    # ),
    # LayerParams(
    #     scale=2000,
    #     orux_layer=8,
    #     m_per_pixel=32.0,
    # ),
    LayerParams(scale=1000, orux_layer=10,  m_per_pixel=50.0),
    LayerParams(scale=500, orux_layer=11, m_per_pixel=25.0),
    # Below line will result in bug as the maps are not aligned to 400px
    LayerParams(scale=200, orux_layer=12, m_per_pixel=10.0),
    # Below line will create a pattern: (tile,empty,empty,emtpy) whe combinde with outer layers
    # LayerParams(scale=200, orux_layer=12, m_per_pixel=10.0, pixel_per_tile=100),
    LayerParams(scale=100, orux_layer=13, m_per_pixel=5.0),
    LayerParams(scale=50, orux_layer=14, m_per_pixel=2.5),
    LayerParams(scale=25, orux_layer=15, m_per_pixel=1.25),
    LayerParams(scale=10, orux_layer=16, m_per_pixel=0.5, pixel_per_tile=500),
)
