package studia.po.spring

import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.RequestHeader
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.server.ResponseStatusException

@RestController
class Controller (private val authService: AuthService) {

    private val productList = listOf(
        Product(1, "Phone"),
        Product(2, "Charger"),
        Product(3, "Pen")
    )

    @GetMapping("/products")
    fun getProducts(@RequestHeader("Username") username: String, @RequestHeader("Password") password: String): List<Product> {
        if (!authService.isAuthorized(username, password)) {
            throw ResponseStatusException(HttpStatus.UNAUTHORIZED, "Invalid credentials")
        }
        return productList
    }

    @GetMapping("/products/{id}")
    fun getProduct(
        @PathVariable id: Int,
        @RequestHeader("Username") username: String,
        @RequestHeader("Password") password: String
    ): Product {
        if (!authService.isAuthorized(username, password)) {
            throw ResponseStatusException(HttpStatus.UNAUTHORIZED, "Invalid credentials")
        }
        return productList[id - 1]
    }
}