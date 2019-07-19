import argparse
import re
from json_util import JSONReader
from trc_util import TRCWriter


class CoorReorder(object):
    def __init__(self, axes_order):
        self.axes_dict = {'x': 0, 'y': 1, 'z': 2}
        self.re_pattern = r"(-?[xyz])(-?[xyz])(-?[xyz])"
        self.axes = re.match(self.re_pattern, axes_order).groups()
        assert len(self.axes) is 3
        self.coor_order = []
        self.coor_sign = []
        for axis in self.axes:
            self.coor_order.append(self.axes_dict[axis[-1]])
            if '-' in axis:
                self.coor_sign.append(-1)
            else:
                self.coor_sign.append(1)

    def __call__(self, coors):
        return [sign * coors[order] for order, sign in zip(self.coor_order, self.coor_sign)]


def main():
    parser = argparse.ArgumentParser(description="Unity exported json to OpenSim friendly trc")
    parser.add_argument(
        "--json-file",
        default="unity.json",
        metavar="FILE",
        help="path to unity exported json file",
    )
    parser.add_argument(
        "--trc-file",
        default="motion.trc",
        metavar="FILE",
        help="path to destination trc file",
    )

    parser.add_argument(
        "--scale-factor",
        default=1.,
        metavar="SCALE",
        help="path to destination trc file",
    )

    parser.add_argument(
        "--axes-order",
        default="xyz",
        metavar="ORDER",
        help="path to destination trc file",
    )

    args = parser.parse_args()

    scale_factor = float(args.scale_factor)

    coor_reorderer = CoorReorder(args.axes_order)

    with open(args.json_file, 'r') as json_file, open(args.trc_file, 'w') as trc_file:
        json_reader = JSONReader(json_file)
        trc_writer = TRCWriter(trc_file)

        trc_writer.add_header(args.trc_file)
        trc_writer.add_frame_info(
            data_rate=json_reader.get_data_rate(),
            camera_rate=json_reader.get_data_rate(),
            num_frames=json_reader.get_num_frames(),
            num_markers=json_reader.get_num_markers(),
            units="mm",  # TODO: fix later
            orig_data_rate=json_reader.get_data_rate(),
            orig_data_start_frame="1",
            orig_num_frames=json_reader.get_num_frames(),
        )

        marker_names = json_reader.marker_names

        trc_writer.add_markers(marker_names)

        for frame in json_reader:
            frame_num = frame["frame_num"]
            time = frame["time"]
            marker_coors = []
            for marker_name in marker_names:
                marker_coors.extend(
                    coor_reorderer(
                        [
                            frame[marker_name]['x'] * scale_factor,
                            frame[marker_name]['y'] * scale_factor,
                            frame[marker_name]['z'] * scale_factor,
                        ]
                    )
                )
            trc_writer.add_frame(frame_num, time, marker_coors)


if __name__ == "__main__":
    main()
