package com.example.getappengine

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.Button
import android.widget.TextView
import kotlinx.android.synthetic.main.fragment_showevents.view.*
import java.util.ArrayList

/**
 * Orignial author: Parsania Hardik on 03-Jan-17.
 * Modified by Ramesh Yerraballi on 8/12/19
 */
class CustomAdapterShowEvents(private val context: Context, private val eventsModelArrayList: ArrayList<Event_Model>) :
    BaseAdapter() {

    override fun getViewTypeCount(): Int {
        return count
    }

    override fun getItemViewType(position: Int): Int {

        return position
    }

    override fun getCount(): Int {
        return eventsModelArrayList.size
    }

    override fun getItem(position: Int): Any {
        return eventsModelArrayList[position]
    }

    override fun getItemId(position: Int): Long {
        return 0
    }

    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
        var convertView = convertView
        val holder: ViewHolder

        if (convertView == null) {
            holder = ViewHolder()
            val inflater = context
                .getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater
            convertView = inflater.inflate(R.layout.event, null, true)

            holder.name = convertView!!.findViewById(R.id.name) as TextView
            holder.date = convertView.findViewById(R.id.date) as TextView
            holder.sport = convertView.findViewById(R.id.sport) as TextView
            holder.spots = convertView.findViewById(R.id.spots) as TextView
            holder.desc = convertView.findViewById(R.id.desc) as TextView
            holder.starttime = convertView.findViewById(R.id.starttime) as TextView
            holder.endtime = convertView.findViewById(R.id.endtime) as TextView


            convertView.tag = holder
        } else {
            // the getTag returns the viewHolder object set as a tag to the view
            holder = convertView.tag as ViewHolder
        }

        holder.name!!.text = "Name: " + eventsModelArrayList[position].getName()
        holder.date!!.text = "Date: " + eventsModelArrayList[position].getDate()
        holder.sport!!.text = "Sports: " + eventsModelArrayList[position].getSport()
        holder.spots!!.text = "Spots: " + eventsModelArrayList[position].getSpotsLeft()
        holder.desc!!.text = "Email: " + eventsModelArrayList[position].getDesc()
        holder.starttime!!.text = "Start Time: " + eventsModelArrayList[position].getStartTime()
        holder.endtime!!.text = "End Time: " + eventsModelArrayList[position].getEndTime()

        return convertView
    }

    private inner class ViewHolder {

        var name: TextView? = null
        var date: TextView? = null
        var sport: TextView? = null
        var spots: TextView? = null
        var desc: TextView? = null
        var starttime: TextView? = null
        var endtime: TextView? = null
    }

}