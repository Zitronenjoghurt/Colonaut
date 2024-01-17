# Text Model Tutorial
A short explanation on how to create text models.

## What is a text model?
In my application I define text models to generate a great variety of different texts from provided templates and replace values.

## How to create a text model?
### Create a .json-File
You will first have to create a .json File, for example `ice_caves.json`. I recommend Visual Studio Code (great editor).

You can copy this empty template to work with:
```json
{
    "replace_values": {

    },
    "templates": [
        {
            "text": "define your first template here"
        },
        {
            "text": "define your second template here"
        },
        {
            "text": "define however many templates you want"
        }
    ]
}
```

### Define Templates
Templates are basically just texts which can include placeholders like `{placeholder}`.

An example template could look like this:
```json
{
    "replace_values": {

    },
    "templates": [
        {
            "text": "The ice caves of the planet are {adjective}."
        }
    ]
}
```

### Define Replace Values
To determine which values can replace the placeholders at random, you have to specify them in the `"replace_values"` section of the model.

To insert random adjectives into the template we specified before, you can define them like this:
```json
{
    "replace_values": {
        "adjective": ["vast", "cold", "big", "empty"]
    },
    "templates": [
        {
            "text": "The ice caves of the planet are {adjective}."
        }
    ]
}
```

The `{adjective}` placeholder will be randomly replaced with one of the adjectives you have defined.

Remember that all replace values need a unique name. Though you can use them multiple times throughout the templates.

Use them to get as much variety into the text as possible^^

### Results
Possible results can now be:
```
"The ice caves of the planet are vast."
"The ice caves of the planet are cold."
"The ice caves of the planet are big."
"The ice caves of the planet are empty."
```