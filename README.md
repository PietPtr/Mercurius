# Mercurius Project Starter

Configure projects in projects.json and start all relevant programs and terminals quickly with Mercurius.

Example configuration:

```
{
    "projects": [
        {
            "name": "Flatsite",                                         // name of the project
            "color": "#ff0097",                                         // color for the button
            "fields": {
                "path": "/home/user/web/flatsite"                       // fields used by startup commands
            },
            "windows": {
                "editor": "atom $path",                                 // all programs needed
                "terminal": "gnome-terminal $path"
            },
            "terminals": {
                "runserver": {
                    "command": "python3 $path/manage.py runserver",     // start a terminal that is already
                    "location": "$path"                                 // running a program and can be used after
                }
            },
            "enabled": true
        }
    ]
}


```
