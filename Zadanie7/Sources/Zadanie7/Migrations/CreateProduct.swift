import Fluent

struct CreateProduct: Migration {
    func prepare(on database: any Database) -> EventLoopFuture<Void> {
        return database.schema("products")
            .id()
            .field("name", .string, .required)
            .field("price", .double, .required)
            .create()
    }

    func revert(on database: any Database) -> EventLoopFuture<Void> {
        return database.schema("products").delete()
    }
}