package com.example.getappengine

import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ListView
import androidx.fragment.app.Fragment
import com.squareup.okhttp.OkHttpClient
import com.squareup.okhttp.Request
import kotlinx.android.synthetic.main.fragment_home.view.*
import kotlinx.android.synthetic.main.fragment_showevents.view.*
import org.json.JSONArray
import org.json.JSONException
import org.jetbrains.anko.doAsync
import java.util.ArrayList

class ShowEventsFragment : Fragment(){
    private var response: String? = null
    private var eventlist: ListView? = null
    private var eventArrayList: ArrayList<String>? = null
    private var eventModelArrayList: ArrayList<Event_Model>? = null
    private var customAdapterShowEvents: CustomAdapterShowEvents? = null

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view =  inflater.inflate(R.layout.fragment_showevents, container, false)

        val doAsync = doAsync {
            try {


                eventlist = view.eventlist
//        userModelArrayList = getInfo(response)  // uncomment this and comment the next line if response is above
                response = fetchInfo()

                val handler = Handler(Looper.getMainLooper())
                handler.post({
                    try {
                        eventModelArrayList = getInfo(response!!)
                        // Create a Custom Adapter that gives us a way to "view" each user in the ArrayList

                        customAdapterShowEvents = CustomAdapterShowEvents(view.context, eventModelArrayList!!)
                        // set the custom adapter for the userlist viewing
                        eventlist!!.adapter = customAdapterShowEvents
                    } catch (e: java.lang.Exception) {
                        println("Error" + e.toString())
                    }

                })
            } catch (e: Exception) {
                println("Error" + e.toString())
            }

        }
        view.showevents.setOnClickListener {
            //action to be performed on a click is its own thread (doAsync)
            (activity as NavigationHost).navigateTo(HomeFragment(), false)
        }

        return view
    }
    override fun onResume() {
        super.onResume()

//        txtsearchuser.setText("")
//        txtsearchuser.setHint("Name")
    }
}

    private fun fetchInfo(): String? {
        val url = "https://apad-project2.appspot.com/showEvents/${Global.uid}"
        val client = OkHttpClient()
        val request = Request.Builder()
            .url(url)
            .header("User-Agent", "Android")
            .build()
        //fetch the URL, time consuming, check network connection, restart emulator
        val response = client.newCall(request).execute()
        val bodystr =  response.body()?.string() // this can be consumed only once
        println(bodystr)
        return bodystr
    }

    private fun getInfo(response: String): ArrayList<Event_Model> {
        val eventModelArrayList = ArrayList<Event_Model>()
        try {
            val dataArray = JSONArray(response)
            for (i in 0 until dataArray.length()) {
                val eventModel = Event_Model()
                val dataobj = dataArray.getJSONObject(i)
                eventModel.setName(dataobj.getString("EventName"))
                eventModel.setDate(dataobj.getString("EventDate"))
                eventModel.setDesc(dataobj.getString("EventDesc"))
                eventModel.setSport(dataobj.getString("EventSport"))
                eventModel.setSpotsLeft(dataobj.getString("EventSpotsLeft").toInt())
                eventModel.setStartTime(dataobj.getString("EventStartTime"))
                eventModel.setEndTime(dataobj.getString("EventEndTime"))
                eventModelArrayList.add(eventModel)
            }
        } catch (e: JSONException) {
            e.printStackTrace()
        }

        return eventModelArrayList
    }

