package studia.po.spring

import org.springframework.stereotype.Service

@Service
object AuthService {
    private val mockUsers = mapOf("user" to "userPassword")

    fun isAuthorized(username: String, password: String): Boolean {
        if (username !in mockUsers) {
            return false
        }

        if (mockUsers[username] != password) {
            return false
        }

        return true
    }
}