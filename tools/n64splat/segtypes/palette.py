import os
from segtypes.segment import N64Segment
from util.color import unpack_color
from util.iter import iter_in_groups


class N64SegPalette(N64Segment):
    require_unique_name = False

    def __init__(self, segment, next_segment, options):
        super().__init__(segment, next_segment, options)

        # palette segments must be named as one of the following:
        #  1) same as the relevant ci4/ci8 segment name (max. 1 palette)
        #  2) relevant ci4/ci8 segment name + "." + unique palette name
        #  3) unique, referencing the relevant ci4/ci8 segment using `image_name`
        self.image_name = segment.get("image_name", self.name.split(
            ".")[0]) if type(segment) is dict else self.name.split(".")[0]

        self.compressed = segment.get("compressed", False) if type(
            segment) is dict else False

    def should_run(self):
        return super().should_run() or "img" in self.options["modes"]

    def split(self, rom_bytes, base_path):
        out_dir = self.create_parent_dir(base_path + "/img", self.name)
        self.path = os.path.join(
            out_dir, os.path.basename(self.name) + ".png")

        data = rom_bytes[self.rom_start: self.rom_end]
        if self.compressed:
            data = Yay0decompress.decompress_yay0(data)

        self.palette = self.parse_palette(data)

    def parse_palette(self, data):
        palette = []

        for a, b in iter_in_groups(data, 2):
            palette.append(unpack_color([a, b]))

        return palette

    def max_length(self):
        if self.compressed:
            return None
        return 256 * 2

    def get_ld_files(self):
        ext = f".{self.type}.png"
        if self.compressed:
            ext += ".Yay0"

        return [("img", f"{self.name}{ext}", ".data")]
