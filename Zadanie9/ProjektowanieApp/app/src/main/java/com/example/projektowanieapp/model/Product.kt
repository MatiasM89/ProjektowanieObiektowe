package com.example.projektowanieapp.model

data class Product(
    val id: Int,
    val name: String,
    val price: Double,
    val imageResId: Int = 0
)