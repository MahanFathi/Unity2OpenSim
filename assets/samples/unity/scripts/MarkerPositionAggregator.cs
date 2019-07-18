using System;
using UnityEngine;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using Newtonsoft.Json; // import this package github.com/SaladLab/Json.Net.Unity3D/releases

public class MarkerInfo 
{
    public string markerName;
    public float x, y, z;
}

public class TimeFrame
{
    public float time;
    public MarkerInfo[] markerInfos;
    public TimeFrame(int markerCount) {
        markerInfos = new MarkerInfo[markerCount];
        for (int i = 0; i < markerCount; i++) 
        {
            markerInfos[i] = new MarkerInfo();
        }
    }
    public string SaveToString()
    {
        return JsonUtility.ToJson(this);
    }
}

public class TimeFrames 
{
    public TimeFrame[] timeFrames;
}

public class MarkerPositionAggregator : MonoBehaviour
{
    public string exportDirectory = "./exports/";
    GameObject[] markerObjects;
    List<TimeFrame> timeFrames = new List<TimeFrame>();
 
    // Start is called before the first frame update
    void Start()
    {
        markerObjects = GameObject.FindGameObjectsWithTag("OpenSimMarker");
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        TimeFrame timeFrame = new TimeFrame(markerObjects.Length);
        timeFrame.time = Time.time;
            // MarkerInfo markerInfo = new MarkerInfo();
        for (int i = 0; i < markerObjects.Length; i++)
        {
            timeFrame.markerInfos[i].markerName = markerObjects[i].name;
            timeFrame.markerInfos[i].x = (markerObjects[i].GetComponent<MarkerPosition>()).globalPos.x;
            timeFrame.markerInfos[i].y = (markerObjects[i].GetComponent<MarkerPosition>()).globalPos.y;
            timeFrame.markerInfos[i].z = (markerObjects[i].GetComponent<MarkerPosition>()).globalPos.z;
        }
        timeFrames.Add(timeFrame);
    }

    void OnApplicationQuit() 
    {

        Int32 unixTimestamp = (Int32)(System.DateTime.UtcNow.Subtract(new DateTime(1970, 1, 1))).TotalSeconds;
        TimeFrames timeFramesObject = new TimeFrames();
        timeFramesObject.timeFrames = new TimeFrame[timeFrames.Count];
        timeFramesObject.timeFrames = timeFrames.ToArray();

        if (!(Directory.Exists(exportDirectory))) {
            Directory.CreateDirectory(exportDirectory);
        }

        string savePath = Path.Combine(exportDirectory, this.transform.name + "_" + unixTimestamp + ".json");

        var json = JsonConvert.SerializeObject(timeFramesObject);
        using (var streamWriter = File.CreateText(savePath)) {
          streamWriter.Write(json);
          Debug.Log("Saved marker positions to path: " + savePath);
        }
    }
}
