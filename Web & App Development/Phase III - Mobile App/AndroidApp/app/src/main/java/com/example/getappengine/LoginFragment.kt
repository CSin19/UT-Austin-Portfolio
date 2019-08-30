package com.example.getappengine

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.OneShotPreDrawListener.add
import androidx.fragment.app.Fragment
import com.squareup.okhttp.*
import kotlinx.android.synthetic.main.activity_main.*
import org.jetbrains.anko.activityUiThread
import org.jetbrains.anko.doAsync
import org.json.JSONArray
import org.json.JSONObject
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import java.io.IOException
import android.R
import android.widget.TextView
import kotlinx.android.synthetic.main.fragment_login.*
import kotlinx.android.synthetic.main.fragment_login.view.*

class LoginFragment : Fragment() {


    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(com.example.getappengine.R.layout.fragment_login, container, false)
        // Set an error if the password is less than 8 characters.
        view.login_button.setOnClickListener {
            doAsync {

                var uname = username.text.toString()
                var upassword = password.text.toString()


                val gotresponse = fetchInfo(uname, upassword)
                val jsonobj = JSONObject(gotresponse)

                if (jsonobj.get("message") == "Success") {
                    Global.uid= jsonobj.get("user_id") as Int?
                    (activity as NavigationHost).navigateTo(HomeFragment(), false)
                }else if(jsonobj.get("message") == "User does not exist. Please sign up."){

                    textview.setVisibility(View.VISIBLE);

                } else{
                    print("failed")
                    username.setText("")
                    password.setText("")
                }

            }

        }


        view.login_signup.setOnClickListener {
            (activity as NavigationHost).navigateTo(RegisterFragment(), false)
        }

        return view
    }




    // Gets a string from the apad19 which is formatted as
    //  an Array of JSON objects: [{...},{...},...{...}]
    private fun fetchInfo(uname: String?, upassword: String?): String? {

        val url = "http://apad-project2.appspot.com/login"
        var okHttpClient = OkHttpClient()
        var formBody = FormBody.Builder()
            .add("username", "$uname")
            .add("password", "$upassword") //assign variable key and value
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




    override fun onResume() {
        super.onResume()

//        txtsearchuser.setText("")
//        txtsearchuser.setHint("Name")
    }
}




