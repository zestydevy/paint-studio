from segtypes.segment import N64Segment
from segtypes.rgba16 import N64SegRgba16
import png
import os
from util import Yay0decompress


class N64SegCi8(N64SegRgba16):
    def __init__(self, segment, next_segment, options):
        super().__init__(segment, next_segment, options)

        self.path = None

    def split(self, rom_bytes, base_path):
        out_dir = self.create_parent_dir(base_path + "/img", self.name)
        self.path = os.path.join(out_dir, os.path.basename(self.name) + ".png")

        data = rom_bytes[self.rom_start: self.rom_end]
        if self.compressed:
            data = Yay0decompress.decompress_yay0(data)

        self.image = self.parse_image(data)

    def postsplit(self, segments):
        palettes = [seg for seg in segments if seg.type ==
                    "palette" and seg.image_name == self.name]

        if len(palettes) == 0:
            print(f"ERROR: {self.type} {self.name} requires at least one palette")
            exit(1)

        seen_paths = []

        for pal_seg in palettes:
            if pal_seg.path in seen_paths:
                print(f"ERROR: Palette name {pal_seg.name} is not unique")
                exit(1)
            seen_paths.append(pal_seg.path)

            w = png.Writer(self.width, self.height, palette=pal_seg.palette)

            with open(pal_seg.path, "wb") as f:
                w.write_array(f, self.image)
                self.log(f"Wrote {pal_seg.name} to {pal_seg.path}")

        # canonical version of image (not palette!) data
        if self.path not in seen_paths:
            w = png.Writer(self.width, self.height,
                           palette=palettes[0].palette)

            with open(self.path, "wb") as f:
                w.write_array(f, self.image)
                self.log(
                    f"No unnamed palette for {self.name}; wrote image data to {self.path}")

    def parse_image(self, data):
        return data

    def max_length(self):
        if self.compressed:
            return None
        return self.width * self.height
