package studia.po.spring

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.RestController

@RestController
class Controller {
    private val productList = listOf(
        Product(1, "Phone"),
        Product(2, "Charger"),
        Product(3, "Pen")
    )

    @GetMapping("/products")
    fun getProducts(): List<Product> {
        return productList
    }

    @GetMapping("/products/{id}")
    fun getProduct(@PathVariable id: Int): Product {
        return productList[id - 1]
    }
}