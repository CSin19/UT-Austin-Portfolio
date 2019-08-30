package com.example.getappengine

class User_Model {

    var uId: Int? = null
    var uName: String? = null
    var uPhone: String? = null
    var uEmail: String? = null
    var uPassword: String? = null
    var uZipcode: String? = null
    var admin: String? = null

    fun getId(): Int? {
        return uId?.toInt()
    }

    fun getName(): String {
        return uName.toString()
    }

    fun getPhone(): String {
        return uPhone.toString()
    }

    fun getEmail(): String {
        return uEmail.toString()
    }

    fun getPassword(): String {
        return uPassword.toString()
    }

    fun getZipcode(): String {
        return uZipcode.toString()
    }

    fun getadmin(): String {
        return admin.toString()
    }

    fun setId(name: Int) {
        this.uId = name
    }

    fun setName(name: String) {
        this.uName = name
    }

    fun setEmail(name: String) {
        this.uEmail = name
    }

    fun setPhone(name: String) {
        this.uPhone = name
    }

    fun setPassword(name: String) {
        this.uPassword = name
    }

    fun setZipcode(name: String) {
        this.uZipcode = name
    }

    fun setadmin(name: String) {
        this.admin = name
    }
}