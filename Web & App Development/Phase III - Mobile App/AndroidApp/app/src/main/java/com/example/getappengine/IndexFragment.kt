package com.example.getappengine

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import com.squareup.okhttp.OkHttpClient
import com.squareup.okhttp.Request
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.fragment_index.view.*
import org.jetbrains.anko.activityUiThread
import org.jetbrains.anko.doAsync
import org.json.JSONArray
import org.json.JSONObject

class IndexFragment: Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.fragment_index, container, false)
        // Set an error if the password is less than 8 characters.
        view.index_login.setOnClickListener({
            //            if (!isPasswordValid(password_edit_text.text!!)) {
//                password_text_input.error = getString(R.string.error_password)
//            } else {
//                // Clear the error.
//                password_text_input.error = null
//                // Navigate to the next Fragment.
            (activity as NavigationHost).navigateTo(LoginFragment(), false)
//            }
        })

        view.index_register.setOnClickListener({
            //            if (!isPasswordValid(password_edit_text.text!!)) {
//                password_text_input.error = getString(R.string.error_password)
//            } else {
//                // Clear the error.
//                password_text_input.error = null
//                // Navigate to the next Fragment.
            (activity as NavigationHost).navigateTo(RegisterFragment(), false)
//            }
        })

        // Clear the error once more than 8 characters are typed.
//        view.password_edit_text.setOnKeyListener({ _, _, _ ->
//            if (isPasswordValid(password_edit_text.text!!)) {
//                // Clear the error.
//                password_text_input.error = null
//            }
//            false
//        })
        return view
    }

    // Gets a string from the apad19 which is formatted as
    //  an Array of JSON objects: [{...},{...},...{...}]
    private fun fetchInfo(): String {
        val url = "https://apad19.appspot.com/list/"

        val client = OkHttpClient()
        val request = Request.Builder()
            .url(url)
            .header("User-Agent", "Android")
            .build()
        val response = client.newCall(request).execute()
        val bodystr =  response.body().string() // this can be consumed only once

        return bodystr
    }

    override fun onResume() {
        super.onResume()

//        txtsearchuser.setText("")
//        txtsearchuser.setHint("Name")
    }
}