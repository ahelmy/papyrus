# Papyrus (under development)
<p align="center">
  <img src="assets/img/papyrus.png"  width="256"/>
</p>

## Why another reporting generator tool?
Papyrus is a simple reporting generator tool that allows you to create reports in a simple and easy way. It is designed to be used in a variety of scenarios, from generating simple reports to complex reports with multiple sections and sub-sections. Papyrus is designed to be easy to use and flexible, allowing you to create reports in a variety of formats, including HTML, Docx, PDF, and plain text.

## Name origin?
A material prepared in ancient Egypt from the pithy stem of a water plant, used in sheets throughout the ancient Mediterranean world for writing or painting on and also for making articles such as rope.

## Features
- Simple and easy to use
- Flexible and customizable

## Supported conversions
| From | To   |  Supported  |
|------|------|:-----------:|
| Docx | Docx |      ✅      |
| HTML | HTML |      ✅      |
| HTML | PDF  |      ✅      |
| Docx | PDF  |      ✅      |



## Installation
```bash
docker run -p 8000:8000 ahelmy0/papyrus:latest
```

## Usage
### Placeholders
Use HTML, Docx, or plain text to create your template. You can use the following placeholders to replace them with your data:
- `{{name}}`
- `{{date}}`
- Nested placeholders:
  - `{{address.city}}`
- For loop:
  - `{% for item in items %} {{item.name}} {% endfor %}` 
- If condition:
  - `{% if condition %} {{name}} {% endif %}`
  - `{% if condition %} {{name}} {% else %} {{date}} {% endif %}`

Example:
1. Create `test.html` file with the following content:
```html
<html>
  <body>
    <h1>Hello {{name}}</h1>
    <h2>Date: {{date}}</h2>
    <table style="border: 2px solid black;">
        {% for item in list %}
        <tr>
            <td style="border: 2px solid black;">{{item.name}}</td>
            <td style="border: 2px solid black;">{{item.age}}</td>
        </tr>
        {% endfor %}
    </table>
  </body>
</html>

```
2. Upload the template:
```bash
curl -X POST "http://127.0.0.1:8000/upload-template/" \
-F "file=@./test.html" 
```

3. Render the template:

```bash
curl -X POST "http://127.0.0.1:8000/render-template/" \
-H "Content-Type: application/json" \
-d '{
  "template_id": "test.docx",
  "data": {
    "name": "John Doe",
    "date": "2024-08-20",
    "items" : [
      {
        "name": "item1",
        "age": 20
      },
      {
        "name": "item2",
        "age": 30
      }
    ]
  },
  "format": "docx"
}'
```



## Contributing


If you are interested to fix an issue or to add new feature, you can just open a pull request.
  

### Contributors

<a  href = "https://github.com/ahelmy/papyrus/graphs/contributors">

<img  src = "https://contrib.rocks/image?repo=ahelmy/papyrus"/>

</a>

  

## License

Licensed with Apache 2.0
