package com.example.getappengine

class Event_Model {

    var EventId: Int? = null
    var EventTeamSize: Int? = null
    var EventSpotsLeft: Int? = null
    var VenueId: Int? = null
    var EventHost: Int? = null
    var EventName: String? = null
    var EventDate: String? = null
    var EventSport: String? = null
    var EventStartTime: String? = null
    var EventEndTime: String? = null
    var EventDesc: String? = null

    fun getId(): Int? {
        return EventId?.toInt()
    }

    fun getTeamSize(): Int? {
        return EventTeamSize?.toInt()
    }
    fun getSpotsLeft(): Int? {
        return EventSpotsLeft?.toInt()
    }
    fun getVId(): Int? {
        return VenueId?.toInt()
    }
    fun getHostId(): Int? {
        return EventHost?.toInt()
    }

    fun getName(): String {
        return EventName.toString()
    }

    fun getDate(): String {
        return EventDate.toString()
    }

    fun getSport(): String {
        return EventSport.toString()
    }

    fun getStartTime(): String {
        return EventStartTime.toString()
    }

    fun getEndTime(): String {
        return EventEndTime.toString()
    }

    fun getDesc(): String {
        return EventDesc.toString()
    }

    fun setId(name: Int) {
        this.EventId = name
    }

    fun setTeamSize(name: Int) {
        this.EventTeamSize = name
    }

    fun setSpotsLeft(name: Int) {
        this.EventSpotsLeft = name
    }

    fun setHost(name: Int) {
        this.EventHost = name
    }

    fun setVId(name: Int) {
        this.VenueId = name
    }

    fun setName(name: String) {
        this.EventName = name
    }


    fun setDate(name: String) {
        this.EventDate = name
    }

    fun setSport(name: String) {
        this.EventSport = name
    }

    fun setStartTime(name: String) {
        this.EventStartTime = name
    }

    fun setEndTime(name: String) {
        this.EventEndTime = name
    }

    fun setDesc(name: String) {
        this.EventDesc = name
    }

}