# Full Stack Excel

Full Stack Excel (FSE) provides a scalable, enterprise-ready web development solution to anyone looking to build a website using Microsoft Excel.

FSE currently supports:

- **The Flask blueprint pattern**: Define blueprints using a special `#blueprints` sheet that treats external Excel files as Flask blueprints. You can now use as many Excel files as you'd like!
- **Jinja2 templating**: template "files" are just worksheets defined in a special `#templates` sheet.
- **Massive scalability**: Excel sheets [support](https://support.microsoft.com/en-us/office/excel-specifications-and-limits-1672b34d-7043-467e-8e27-269d656771c3) up to 1,048,576 rows of data, which means this is the maximum number of endpoints + rules you can define in the `#routes` worksheet of any base app file or blueprint file. That' a lot of routes!

FSE requires Python 3.6+. Although FSE is built in Python, your website won't need to be. Everything you do to define your website's behavior can be done in Excel alone.

https://twitter.com/ryxcommar/status/1288620264725663744?s=20

![](https://pbs.twimg.com/media/EeJY1N5WoAA0sD3?format=png&name=900x900)

## Run Demo

```shell script
git clone https://github.com/ryxcommar/fullstackexcel.git
cd fullstackexcel
pip install -e .
fse create-demo
fse run-excel --env development demo_website.xlsx
```

Powered by Flask.

**Note: this library is currently in alpha. The API is subject to breakage until this message is removed.**
