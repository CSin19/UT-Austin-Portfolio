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
import kotlinx.android.synthetic.main.fragment_login.*
import kotlinx.android.synthetic.main.fragment_login.view.*
import kotlinx.android.synthetic.main.fragment_login.view.password
import kotlinx.android.synthetic.main.fragment_login.view.textview
import kotlinx.android.synthetic.main.fragment_login.view.username
import kotlinx.android.synthetic.main.fragment_searchevents.*
import kotlinx.android.synthetic.main.fragment_searchevents.view.*
import kotlinx.android.synthetic.main.fragment_showevents.view.*
import okhttp3.FormBody
import org.jetbrains.anko.doAsync
import org.json.JSONArray
import org.json.JSONException
import org.json.JSONObject
import java.io.IOException
import java.util.ArrayList

class SearchEventsFragment : Fragment(){


    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view =  inflater.inflate(R.layout.fragment_searchevents, container, false)

        view.search_button.setOnClickListener {

                Global.vname = venuenameinput.text.toString()
                Global.edate = eventdateinput.text.toString()
                Global.estarttime = eventstarttimeinput.text.toString()
                Global.eendtime = eventendtimeinput.text.toString()
                (activity as NavigationHost).navigateTo(SearchEventsResultFragment(), false)
            }
        return view;
    }

}


