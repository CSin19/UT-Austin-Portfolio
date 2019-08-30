package com.example.getappengine

class User_Event_Model {

    var uId: Int? = null
    var EventId: Int? = null

    fun getUserId(): Int? {
        return uId?.toInt()
    }

    fun getEId(): Int? {
        return EventId?.toInt()
    }

    fun setUserId(name: Int) {
        this.uId = name
    }

    fun setEId(name: Int) {
        this.EventId = name
    }
}