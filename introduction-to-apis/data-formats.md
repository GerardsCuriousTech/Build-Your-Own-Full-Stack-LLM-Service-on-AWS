# Data Formats

In order to make use of data on the internet we first need to parse our source. Our data source can be made up of structured and unstructured data.

\
**Structured Data**

1. **HTML (Hypertext Markup Language)**:
   * **Purpose**: HTML is primarily used for creating web pages. It defines the structure and layout of content on a webpage.
   * **Description**: HTML uses tags to mark up elements like headings, paragraphs, images, links, and forms. It’s readable by both humans and browsers.
   *   **Example**:**HTML**

       ```
       <!DOCTYPE html>
       <html>
         <head>
           <title>My Web Page</title>
         </head>
         <body>
           <h1>Welcome to My Page</h1>
           <p>This is some text.</p>
           <img src="my-image.jpg" alt="My Image">
         </body>
       </html>
       ```

       AI-generated code. Review and use carefully. [More info on FAQ](https://www.bing.com/new#faq).
   * **Parsing**: Browsers automatically parse HTML to render web pages.
2. **XML (Extensible Markup Language)**:
   * **Purpose**: XML is used for structuring and organizing data. It’s extensible because you can define your own tags.
   * **Description**: XML uses tags to create hierarchically organized documents. It’s readable by humans and easy to manipulate programmatically.
   *   **Example**:**XML**

       ```
       <?xml version="1.0" encoding="UTF-8"?>
       <friends>
         <friend>
           <name>John Ferreira</name>
           <age>26</age>
           <city>Porto</city>
           <profession>Full Stack Web Developer</profession>
           <hobby>Fitness</hobby>
         </friend>
         <!-- More friend records... -->
       </friends>
       ```

       AI-generated code. Review and use carefully. [More info on FAQ](https://www.bing.com/new#faq).
   * **Parsing**: You can use libraries (e.g., **`xml.etree.ElementTree`** in Python) to parse XML data.
3. **JSON (JavaScript Object Notation)**:
   * **Purpose**: JSON is widely used for data interchange between systems. It’s lightweight and easy to read.
   * **Description**: JSON represents data as key-value pairs. It’s commonly used in APIs, configuration files, and databases.
   *   **Example**:**JSON**

       ```
       {
         "friends": [
           {
             "name": "John Ferreira",
             "age": 26,
             "city": "Porto",
             "profession": "Full Stack Web Developer",
             "hobby": "Fitness"
           },
           // More friend records...
         ]
       }
       ```

       AI-generated code. Review and use carefully. [More info on FAQ](https://www.bing.com/new#faq).
   * **Parsing**: Most programming languages have built-in support for parsing JSON (e.g., **`json`** module in Python).
4. **CSV (Comma-separated Values)**:
   * **Purpose**: CSV is used for representing tabular data (rows and columns). It’s commonly used in spreadsheets and databases.
   * **Description**: CSV is plain text with records separated by commas. The first line often serves as the header.
   *   **Example**:

       ```
       name,age,city,profession,hobby
       John Ferreira,26,Porto,Full Stack Web Developer,Fitness
       Leonardo Marinho,18,London,Electric Engineer,Build lego
       Caroline Azevedo,34,Salvador,Entrepreneur,Sing
       ```
   * **Parsing**: You can read CSV files line by line and split values using commas.

<br>

**Unstructured Data**

**Unstructured data** refers to information that **doesn’t follow a specific format or structure**, making it challenging to process and analyze using conventional tools. [Unlike structured data, which neatly fits into tables (like those found in Microsoft Excel), unstructured data can’t be quickly analyzed and searched without further processing](https://www.coursera.org/articles/what-is-unstructured-data).

<br>
