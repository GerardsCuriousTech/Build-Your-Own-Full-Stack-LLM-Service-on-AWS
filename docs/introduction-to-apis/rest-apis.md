# REST APIs

This course focuses on REST APIs.

A REST API (Representational State Transfer Application Programming Interface) is a set of rules and conventions for building and interacting with web services.

Here are the key principles of REST APIs:

1. **Uniform Interface**: REST APIs have a uniform interface, which decouples the client and server and allows each to evolve independently.
2. **Stateless**: Each request from a client to a server must contain all the information needed to understand and process the request. The server does not store anything about the latest HTTP request the client made.
3. **Client-Server Architecture**: The client is responsible for the user interface and user experience, and the server is responsible for processing requests and managing resources.
4. **Cacheable**: Responses from the server can be cached by the client. This improves performance by reducing the load on the server and network.
5. **Layered System**: The architecture allows for layers of servers (e.g., load balancers, cache servers) that can be added to improve scalability and performance.

REST APIs use standard HTTP methods like `GET`, `POST`, `PUT`, and `DELETE` to perform operations on data. The data sent and received is typically in JSON or XML format.

For example, to retrieve a user's information from a database, you might send a `GET` request to `http://api.example.com/users/123`. The server responds with the data for the user with that ID.

REST APIs are widely adopted for their simplicity, scalability, and performance. They are used in web apps, mobile apps, and microservices architectures.
