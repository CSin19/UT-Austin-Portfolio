package com.example.getappengine

import android.os.Bundle
import android.text.Editable
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.fragment_home.*
import kotlinx.android.synthetic.main.fragment_home.view.*
import org.json.JSONArray

class HomeFragment: Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.fragment_home, container, false)
        // Set an error if the password is less than 8 characters.

        view.button1.setOnClickListener {
            //action to be performed on a click is its own thread (doAsync)
            (activity as NavigationHost).navigateTo(SearchEventsFragment(), false)
        }

        view.button2.setOnClickListener {
            //action to be performed on a click is its own thread (doAsync)
            (activity as NavigationHost).navigateTo(JoinEventsFragment(), false)
        }

        view.button3.setOnClickListener {
            //action to be performed on a click is its own thread (doAsync)
            (activity as NavigationHost).navigateTo(ShowEventsFragment(), false)
                }

        view.button4.setOnClickListener {
            //action to be performed on a click is its own thread (doAsync)
            Global.uid=null
            Global.vname=null
            Global.edate= null
            Global.eendtime=null
            Global.estarttime=null
            Global.selectedeventspots=null
            Global.selectedevent=null
            (activity as NavigationHost).navigateTo(IndexFragment(), false)
        }
        return view
    }
}