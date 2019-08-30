package com.example.getappengine

import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ListView
import androidx.fragment.app.Fragment
import com.squareup.okhttp.OkHttpClient
import com.squareup.okhttp.Request
import kotlinx.android.synthetic.main.fragment_searcheventsresult.view.*
import kotlinx.android.synthetic.main.fragment_showevents.view.*
import okhttp3.FormBody
import org.jetbrains.anko.doAsync
import org.json.JSONArray
import org.json.JSONException
import org.json.JSONObject
import java.io.IOException
import java.util.ArrayList

class SearchEventsResultFragment : Fragment(){
    private var response: String? = null
    private var eventlist: ListView? = null
    private var eventArrayList: ArrayList<String>? = null
    private var eventModelArrayList: ArrayList<Event_Model>? = null
    private var customAdapterShowEvents: CustomAdapterShowEvents? = null

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view =  inflater.inflate(R.layout.fragment_searcheventsresult, container, false)

        doAsync {
            try {

                eventlist = view.eventlistsearch
//        userModelArrayList = getInfo(response)  // uncomment this and comment the next line if response is above
                response = fetchInfo()
                val handler = Handler(Looper.getMainLooper())
                handler.post {
                    try {

                        eventModelArrayList = getInfo(response!!)
                        print("Mark2")
                        // Create a Custom Adapter that gives us a way to "view" each user in the ArrayList

                        customAdapterShowEvents = CustomAdapterShowEvents(view.context, eventModelArrayList!!)
                        // set the custom adapter for the userlist viewing
                        eventlist!!.adapter = customAdapterShowEvents
                    } catch (e: java.lang.Exception) {
                        println("Error" + e.toString())
                    }

                }
            }
            catch(e: Exception) {
                println("Error" + e.toString())
            }

        }
        view.jbutton.setOnClickListener {
            //action to be performed on a click is its own thread (doAsync)
            (activity as NavigationHost).navigateTo(HomeFragment(), false)
        }

        return view;
    }
    override fun onResume() {
        super.onResume()

//        txtsearchuser.setText("")
//        txtsearchuser.setHint("Name")
    }
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


private fun fetchInfo(): String? {


    val url = "http://apad-project2.appspot.com/searchEventsMobile/${Global.uid}"
    var okHttpClient = okhttp3.OkHttpClient()
    var formBody = FormBody.Builder()
        .add("name", "${Global.vname}")
        .add("date", "${Global.edate}") //assign variable key and value
        .add("start", "${Global.estarttime}")
        .add("end", "${Global.eendtime}")
        .build()

    var request = okhttp3.Request.Builder()
        .url(url)
        .header("User-Agent", "Android")
        .post(formBody)
        .build()

    try {
        var response = okHttpClient.newCall(request).execute()
        var result = response.body()?.string()
        Log.d("result", result)
        response.body()?.close()
        return result
    } catch (e: IOException) {
        e.printStackTrace()
        return "Error"
    }
}




