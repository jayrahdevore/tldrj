# tldrj | The friendly json drilldown

<p align="center">
<a href="https://github.com/jayrahdevore/tldr/actions"><img alt="Actions Status" src="https://github.com/jayrahdevore/tldrj/workflows/Lint/badge.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

**tldrj** is a script that takes an arbitrary json file and boils it down to a bite-sized excerpt.  It can also be used to infer datatypes, so you no longer need to look around a large file to see how it's structured.  This is useful when creating relational database schema to store json-structured data, or when trying to view how a file is structured when writnig a script to parse it.

---
### What it does

Say we have a neighborhood address book:
```
{
  "neighbors": [
    {
      "name": "Eddie Haskell",
      "address": "211 Pine Street",
      "num_cars": 0,
      "dependents": []
    },
    {
      "name": "Ward Cleaver",
      "address": "485 Maple Drive",
      "num_cars": 2,
      "dependents": [
        "June Cleaver",
        "Theodore Cleaver",
        "Wallace Cleaver"
      ]
    },
    {
      "name": "Clarence Rutherford",
      "address": "312 Rosewood Way",
      "num_cars": 1,
      "dependents": []
    }
  ],
  "neighborhood": "Happy Oaks",
  "city": "Mayfield"
}
```

**tldrj** can take this file and boil it down to a minimum working example

```
$ python3 tldrj.py -m example.json
{
    "neighbors": [
        {
            "name": "Ward Cleaver",
            "address": "485 Maple Drive",
            "num_cars": 2,
            "dependents": [
                "June Cleaver"
            ]
        }
    ],
    "neighborhood": "Happy Oaks",
    "city": "Mayfield"
}
```

**tldrj** can also take this file and infer a key and datatype schema

```
$ python3 tldrj.py -t example.json
{
    "neighbors": [
        {
            "name": "str",
            "address": "str",
            "num_cars": "int",
            "dependents": [
                "str"
            ]
        }
    ],
    "neighborhood": "str",
    "city": "str"
}
```
