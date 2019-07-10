import json


class JSONReader(object):
    def __init__(self, json_file):
        json_data = json.load(json_file)
        self.data = json_data["timeFrames"][1:]     # discard the first frame
        self.marker_names = self.get_marker_names()
        assert len(self.data) > 1, "NOT ENOUGH DATA IN UNITY JSON"

    def get_marker_names(self):
        return [markerInfo["markerName"] for markerInfo in self.data[0]["markerInfos"]]

    def __getitem__(self, idx):
        time_frame = self.data[idx]
        frame_dict = {}
        frame_dict["time"] = time_frame["time"]
        frame_dict["frame_num"] = idx + 1
        for markerInfo in time_frame["markerInfos"]:
            marker_name = markerInfo["markerName"]
            frame_dict[marker_name] = {
                "x": markerInfo["x"],
                "y": markerInfo["y"],
                "z": -markerInfo["z"],
            }
        return frame_dict

    def get_data_rate(self):
        return 1. / (float(self.data[1]["time"]) - float(float(self.data[0]["time"])))

    def get_num_frames(self):
        return len(self.data)

    def get_num_markers(self):
        return len(self.marker_names)
