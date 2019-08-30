package com.example.getappengine

class Venue_Model {

    var VenueId: Int? = null
    var VenueName: String? = null
    var VenueZipcode: String? = null
    var VenueAddress: String? = null
    var VenueOpeningTime: String? = null
    var VenueClosingTime: String? = null
    var VenueSports: String? = null

    fun getId(): Int? {
        return VenueId?.toInt()
    }

    fun getName(): String {
        return VenueName.toString()
    }

    fun getZipcode(): String {
        return VenueZipcode.toString()
    }

    fun getAddress(): String {
        return VenueAddress.toString()
    }

    fun getOpeningTime(): String {
        return VenueOpeningTime.toString()
    }

    fun getClosingTime(): String {
        return VenueClosingTime.toString()
    }

    fun getSports(): String {
        return VenueSports.toString()
    }

    fun setId(name: Int) {
        this.VenueId = name
    }

    fun setName(name: String) {
        this.VenueName = name
    }

    fun setZipcode(name: String) {
        this.VenueZipcode = name
    }

    fun setAddress(name: String) {
        this.VenueAddress = name
    }

    fun setOpeningTime(name: String) {
        this.VenueOpeningTime = name
    }

    fun setClosingTime(name: String) {
        this.VenueClosingTime = name
    }

    fun setSports(name: String) {
        this.VenueSports = name
    }
}