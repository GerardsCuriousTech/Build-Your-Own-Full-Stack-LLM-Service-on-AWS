# What is cURL?

`cURL` (client URL) is a command-line tool for transferring data to and from a server. It supports HTTP, HTTPS, and many other protocols, and runs on almost every platform. This makes cURL ideal for testing API communication from any device with a command line and network connectivity.

The most basic command is `curl [URL]`. The `curl` command followed by a URL retrieves the resource at that address — for a web page, it returns the HTML source.

To use cURL with REST APIs, you specify different HTTP methods along with headers and data. Here are common examples:

1.  **GET Request** — retrieve data from the server:

    ```
    curl http://api.example.com/resource
    ```
2.  **POST Request** — send data to the server (JSON in this case):

    ```
    curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' http://api.example.com/resource
    ```
3.  **PUT Request** — update existing data on the server:

    ```
    curl -X PUT -H "Content-Type: application/json" -d '{"key":"value"}' http://api.example.com/resource/id
    ```
4.  **DELETE Request** — delete existing data from the server:

    ```
    curl -X DELETE http://api.example.com/resource/id
    ```

In these examples, `-X` specifies the HTTP method, `-H` sets request headers, and `-d` sends data in the request body.

The actual commands vary based on the API's specifications. Always refer to the API documentation for accurate request formats.

### Key cURL Resources

* The Tutorial from the official cURL website
  * [https://curl.se/docs/tutorial.html](https://curl.se/docs/tutorial.html)
* The open source cURL book from the Everything cURL website
  * [https://everything.curl.dev/index.html](https://everything.curl.dev/index.html)
