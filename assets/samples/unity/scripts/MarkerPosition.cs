using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MarkerPosition : MonoBehaviour
{
    public Vector3 globalPos;
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
	    globalPos = transform.position;
    }
}
