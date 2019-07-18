import argparse
from json_util import JSONReader
from trc_util import TRCWriter


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
        metavar="FILE",
        help="path to destination trc file",
    )

    args = parser.parse_args()

    scale_factor = float(args.scale_factor)

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
                marker_coors.extend([frame[marker_name]['x'] * scale_factor,
                                     frame[marker_name]['y'] * scale_factor,
                                     frame[marker_name]['z'] * scale_factor])
            trc_writer.add_frame(frame_num, time, marker_coors)


if __name__ == "__main__":
    main()
