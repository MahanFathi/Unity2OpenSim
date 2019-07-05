import csv


class TRCWriter(object):
    def __init__(self, trc_file):
        self.csv_writer = csv.writer(trc_file, delimiter='\t')

    def add_header(self, filename):
        self.csv_writer.writerow('PathFileType', '4', r'(X\Y\Z)', filename)

    def add_frame_info(self,
                       data_rate='',
                       camera_rate='',
                       num_frames='',
                       num_markers='',
                       units='',
                       orig_data_rate='',
                       orig_data_start_frame='',
                       orig_num_frames='',
                       ):
        self.csv_writer.writerow(["DataRate",
                                  "CameraRate",
                                  "NumFrames",
                                  "NumMarkers",
                                  "Units",
                                  "OrigDataRate",
                                  "OrigDataStartFrame",
                                  "OrigNumFrames"])
        self.csv_writer.writerow([data_rate,
                                  camera_rate,
                                  num_frames,
                                  num_markers,
                                  units,
                                  orig_data_rate,
                                  orig_data_start_frame,
                                  orig_num_frames
                                  ])

    def add_markers(self, markers):
        tab_separated_markers = []
        for marker in markers:
            tab_separated_markers.extend([marker, '', ''])
        self.csv_writer.writerow(['Frame#', 'Time'] + tab_separated_markers)

        marker_coordinates = []
        for i in range(len(markers)):
            marker_coordinates.extend([axis.format(i) for axis in ['X{}', 'Y{}', 'Z{}']])
        self.csv_writer.writerow(['', ''] + marker_coordinates)
        self.csv_writer.writerow([])    # write an empty row

    def add_frame(self, frame, time, marker_coors):
        self.csv_writer.writerow([int(frame), round(time, 6), [round(coor, 6) for coor in marker_coors]])
