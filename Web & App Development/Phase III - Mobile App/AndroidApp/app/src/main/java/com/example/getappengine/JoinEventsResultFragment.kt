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
import kotlinx.android.synthetic.main.fragment_joineventsresult.view.*
import kotlinx.android.synthetic.main.fragment_login.*
import kotlinx.android.synthetic.main.fragment_searcheventsresult.view.*
import kotlinx.android.synthetic.main.fragment_showevents.view.*
import okhttp3.FormBody
import okhttp3.Request
import org.jetbrains.anko.doAsync
import org.json.JSONArray
import org.json.JSONException
import org.json.JSONObject
import java.io.IOException
import java.util.ArrayList

class JoinEventsResultFragment : Fragment(){


    private var response: String? = null
    private var eventlist: ListView? = null
    private var eventArrayList: ArrayList<String>? = null
    private var eventModelArrayList: ArrayList<Event_Model>? = null
    private var customAdapterShowEvents: CustomAdapterShowEvents? = null

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view =  inflater.inflate(R.layout.fragment_joineventsresult, container, false)

        doAsync {
            try {

//        userModelArrayList = getInfo(response)  // uncomment this and comment the next line if response is above
                response = fetchInfo()
                val handler = Handler(Looper.getMainLooper())
                handler.post {
                    try {

                        val jsonobj = JSONObject(response)

                        if (jsonobj.get("message") == "Success") {

                            textview.setVisibility(View.VISIBLE);
                        }


                    } catch (e: java.lang.Exception) {
                        println("Error" + e.toString())
                    }

                }
            }
            catch(e: Exception) {
                println("Error" + e.toString())
            }

        }
        view.joinbutton.setOnClickListener {
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



private fun fetchInfo(): String? {


    val url = "http://apad-project2.appspot.com/joinEventsResultMobile/${Global.uid}"
    var okHttpClient = okhttp3.OkHttpClient()
    var formBody = FormBody.Builder()
        .add("eid", "${Global.selectedevent}")
        .add("spots", "${Global.selectedeventspots}") //assign variable key and value
        .build()

    var request = Request.Builder()
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




