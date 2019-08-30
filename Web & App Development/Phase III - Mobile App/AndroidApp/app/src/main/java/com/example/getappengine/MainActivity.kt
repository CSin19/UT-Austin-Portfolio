package com.example.getappengine

import android.os.Bundle
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import com.squareup.okhttp.OkHttpClient
import com.squareup.okhttp.Request
import kotlinx.android.synthetic.main.activity_main.*
import org.jetbrains.anko.activityUiThread
import org.jetbrains.anko.doAsync
import org.json.JSONArray
import org.json.JSONObject
import androidx.fragment.app.Fragment

class MainActivity : AppCompatActivity(), NavigationHost {

    override fun onCreate(savedInstanceState: Bundle?)  {
        super.onCreate(savedInstanceState)
        //Tie view to activity_main.xml
        setContentView(R.layout.activity_main)
        //Register a listener for button clicks
        if (savedInstanceState == null) {
            supportFragmentManager
                .beginTransaction()
                .add(R.id.container, IndexFragment())
                .commit()
        }
                }

        /*
            }
        }
        button3.setOnClickListener {
            //action to be performed on a click is its own thread (doAsync)
            doAsync {
                val gotresponse = fetchInfo() //time-consuming HTTP request; output string
                val jsonarray = JSONArray(gotresponse) //coverts JSON string to array of JSON objects
                //Access UI thread resources
                activityUiThread {
                    //iterate through the returned array of JSON objects
                    // and look for candiadate whose name we requested
                    for (i in 0..(jsonarray.length() - 1)) {
                        val user = jsonarray.getJSONObject(i)
                        if(user.get("candidate") == txtsearchuser.text.toString()) {
                            txtusername.text = user.get("email").toString()
                        }
                    }
                }
            }
        }
    }*/
    // Gets a string from the apad19 which is formatted as
    //  an Array of JSON objects: [{...},{...},...{...}]
    /*private fun fetchInfo(): String {
        val url = "apad"

        val client = OkHttpClient()
        val request = Request.Builder()
            .url(url)
            .header("User-Agent", "Android")
            .build()
        //fetch the URL, time consuming, check network connection, restart emulator
        val response = client.newCall(request).execute()
        val bodystr =  response.body().string() // this can be consumed only once

        return bodystr
    }

    override fun onResume() {
        super.onResume()

        txtsearchuser.setText("")
        txtsearchuser.setHint("Name")
    }*/

    override fun navigateTo(fragment: Fragment, addToBackstack: Boolean) {
        val transaction = supportFragmentManager
            .beginTransaction()
            .replace(R.id.container, fragment)

        if (addToBackstack) {
            transaction.addToBackStack(null)
        }

        transaction.commit()
    }
}