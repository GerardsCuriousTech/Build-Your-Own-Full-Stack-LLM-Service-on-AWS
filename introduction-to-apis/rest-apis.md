# Rest APIs

This course will focus on REST APIs.\
\
[A REST API (Representational State Transfer Application Programming Interface) is a set of rules and conventions for building and interacting with web services](https://www.freecodecamp.org/news/what-is-rest-rest-api-definition-for-beginners/).

Here are some key points about REST APIs:

1. [**Uniform Interface**: REST APIs have a uniform interface, which helps to decouple the client and server and allow each to evolve independently](https://aws.amazon.com/what-is/restful-api/).
2. [**Stateless**: Each request from a client to a server must contain all the information needed to understand and process the request](https://www.freecodecamp.org/news/what-is-rest-rest-api-definition-for-beginners/)[1](https://www.freecodecamp.org/news/what-is-rest-rest-api-definition-for-beginners/). [The server should not store anything about the latest HTTP request the client made](https://www.freecodecamp.org/news/what-is-rest-rest-api-definition-for-beginners/)[1](https://www.freecodecamp.org/news/what-is-rest-rest-api-definition-for-beginners/).
3. [**Client-Server Architecture**: The client is responsible for the user interface and user experience, and the server is responsible for processing requests and managing resources](https://www.freecodecamp.org/news/what-is-rest-rest-api-definition-for-beginners/)[1](https://www.freecodecamp.org/news/what-is-rest-rest-api-definition-for-beginners/).
4. **Cacheable**: Responses from the server can be cached by the client. [This can improve performance as it reduces the load on the server and network](https://www.freecodecamp.org/news/what-is-rest-rest-api-definition-for-beginners/)[1](https://www.freecodecamp.org/news/what-is-rest-rest-api-definition-for-beginners/).
5. [**Layered System**: The architecture allows for layers of servers (e.g., load balancers, cache servers, etc.) that can be added to improve scalability and performance](https://www.freecodecamp.org/news/what-is-rest-rest-api-definition-for-beginners/)[1](https://www.freecodecamp.org/news/what-is-rest-rest-api-definition-for-beginners/).

[REST APIs use standard HTTP methods, like `GET`, `POST`, `PUT`, `DELETE`, etc., to perform operations on the data](https://www.freecodecamp.org/news/what-is-rest-rest-api-definition-for-beginners/)[1](https://www.freecodecamp.org/news/what-is-rest-rest-api-definition-for-beginners/). [The data that is sent and received is often in the form of JSON or XML](https://www.freecodecamp.org/news/what-is-rest-rest-api-definition-for-beginners/).

For example, if you wanted to retrieve a user’s information from a database, you might send a `GET` request to `http://api.example.com/users/123`. [The server would then respond with the data for the user with ID](https://www.freecodecamp.org/news/what-is-rest-rest-api-definition-for-beginners/).

[REST APIs have become very popular for their simplicity, scalability, and performance](https://www.freecodecamp.org/news/what-is-rest-rest-api-definition-for-beginners/). [They are used in many types of applications, from web and mobile apps to microservices architecture](https://www.freecodecamp.org/news/what-is-rest-rest-api-definition-for-beginners/)
