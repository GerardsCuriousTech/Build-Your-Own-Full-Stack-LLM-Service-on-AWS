# What is cURL?

[`cURL`, which stands for client URL, is a command-line tool that developers use to transfer data to and from a server](https://developer.ibm.com/articles/what-is-curl-command/). [It supports several different protocols, including HTTP and HTTPS, and runs on almost every platform](https://developer.ibm.com/articles/what-is-curl-command/)[1](https://developer.ibm.com/articles/what-is-curl-command/). [This makes cURL ideal for testing communication from almost any device (as long as it has a command line and network connectivity) from a local server to most edge devices](https://developer.ibm.com/articles/what-is-curl-command/)[1](https://developer.ibm.com/articles/what-is-curl-command/).

The most basic command in cURL is `curl [URL]`. [The `curl` command is followed by the URL, from which we would like to retrieve some kind of data](https://developer.ibm.com/articles/what-is-curl-command/)[1](https://developer.ibm.com/articles/what-is-curl-command/). [In this case, it would return the HTML source for the specified URL](https://developer.ibm.com/articles/what-is-curl-command/).

Now, to use `cURL` with REST APIs, you can use different HTTP methods like `GET`, `POST`, `PUT`, `DELETE`, etc. Here are some examples:

1.  **GET Request**: This is used to retrieve data from the server. The command would look like this:

    ```
    curl http://api.example.com/resource
    ```
2.  **POST Request**: This is used to send data to the server. Here’s an example where we’re sending JSON data:

    ```
    curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' http://api.example.com/resource
    ```
3.  **PUT Request**: This is used to update existing data on the server. An example would be:

    ```
    curl -X PUT -H "Content-Type: application/json" -d '{"key":"value"}' http://api.example.com/resource/id
    ```
4.  **DELETE Request**: This is used to delete existing data from the server. Here’s how you can do it:

    ```
    curl -X DELETE http://api.example.com/resource/id
    ```

[In these examples, `-X` is used to specify the HTTP method, `-H` is used to specify request headers, and `-d` is used to send data in the request body](https://developer.ibm.com/articles/what-is-curl-command/).

Remember, the actual commands may vary based on the API’s specifications. [Always refer to the API documentation for accurate information](https://linuxize.com/post/curl-rest-api/).

### Key CURL Resources

* The Tutorial from the official cURL website
  * [https://curl.se/docs/tutorial.html](https://curl.se/docs/tutorial.html)
* The open source cURL book from the Everything cURL website
  * [https://everything.curl.dev/index.html](https://everything.curl.dev/index.html)
