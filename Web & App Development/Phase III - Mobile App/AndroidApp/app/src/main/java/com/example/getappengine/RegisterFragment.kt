package com.example.getappengine

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import com.squareup.okhttp.OkHttpClient
import com.squareup.okhttp.Request
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.fragment_register.*
import kotlinx.android.synthetic.main.fragment_register.view.*
import kotlinx.android.synthetic.main.fragment_register.view.email
import kotlinx.android.synthetic.main.fragment_register.view.password
import kotlinx.android.synthetic.main.fragment_register.view.phone
import kotlinx.android.synthetic.main.fragment_register.view.username
import kotlinx.android.synthetic.main.fragment_register.view.zipcode
import okhttp3.FormBody
import org.jetbrains.anko.activityUiThread
import org.jetbrains.anko.doAsync
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException

class RegisterFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.fragment_register, container, false)
        // Set an error if the password is less than 8 characters.
        view.register_button.setOnClickListener({

            doAsync {

                var uname = username.text.toString()
                var upassword = password.text.toString()
                var uphone = phone.text.toString()
                var uemail = email.text.toString()
                var zipcode = zipcode.text.toString()


                val gotresponse = fetchInfo(uname, upassword, uphone,uemail,zipcode)
                val jsonobj = JSONObject(gotresponse)


                if (jsonobj.get("message") == "User created") {
                    Global.uid= jsonobj.get("user_id") as Int?
                    (activity as NavigationHost).navigateTo(HomeFragment(), false)

                }else{
                    print("failed")
                    username.setText("")
                    password.setText("")
                }

            }

        })

        return view
    }

    // Gets a string from the apad19 which is formatted as
    //  an Array of JSON objects: [{...},{...},...{...}]
    private fun fetchInfo(uname: String?, upassword: String?, uphone:String?, uemail:String?, zipcode:String?): String? {
        val url = "http://apad-project2.appspot.com/createAccount"
        var okHttpClient = okhttp3.OkHttpClient()
        var formBody = FormBody.Builder()
            .add("username", "$uname")
            .add("password", "$upassword")
            .add("phone", "$uphone")
            .add("email", "$uemail")
            .add("zipcode", "$zipcode")
            .add("admin", "False")
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

    override fun onResume() {
        super.onResume()

//        txtsearchuser.setText("")
//        txtsearchuser.setHint("Name")
    }
}

