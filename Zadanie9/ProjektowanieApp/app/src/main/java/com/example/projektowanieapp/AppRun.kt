package com.example.projektowanieapp

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.projektowanieapp.adapter.CategoryAdapter
import com.example.projektowanieapp.model.Category
import com.example.projektowanieapp.model.Product

class AppRun : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.app_run)

        val categoriesRecyclerView = findViewById<RecyclerView>(R.id.categoriesRecyclerView)

        val electronicsProducts = listOf(
            Product(1, "Smartphone", 800.0),
            Product(2, "Laptop", 1000.0)
        )
        val electronics = Category(1, "Electronics", electronicsProducts)

        val clothingProducts = listOf(
            Product(3, "T-Shirt", 20.0),
            Product(4, "Jeans", 50.0)
        )
        val clothing = Category(2, "Clothing", clothingProducts)

        val categories =  listOf(electronics, clothing)

        categoriesRecyclerView.layoutManager = LinearLayoutManager(this)
        categoriesRecyclerView.adapter = CategoryAdapter(categories)
    }
}