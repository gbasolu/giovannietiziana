from flask import Flask, jsonify, request, redirect, send_from_directory, send_file
from flask_cors import CORS
import logging
import json

app = Flask('matrimonio')
CORS(app)

import yaml

def file_manager(language):
    full_page=""
    file_name=f'./translations/{language}-b.yaml'
    print(file_name)
    with open(file_name, 'r') as file:

        translation = yaml.safe_load(file)
        full_page=navigate_object(translation, [], full_page)

    full_page=f"<form action='/save/{language}' method='post'>{full_page} <input type='submit' value='Submit'></form>"
    return full_page

def navigate_object(obj, path, full_page):
    """Navigates a multilevel object and returns a list of all its values.

    Args:
        obj: The object to navigate.

    Returns:
        A list containing all the values found in the object,
        preserving the structure of arrays and objects.
    """

    values = []
    if isinstance(obj, str):
        path_string=",".join(path)
        name_string="_".join(path)
        full_page=f"{full_page}<div><textarea name='{name_string}' path='{path_string}' style='width:1000px; height:200px'>{obj}</textarea></div>"
        # values.append(obj)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            full_page=f"{full_page}<div style='padding-left:10px'>"
            path.append(f"{i}")
            full_page=navigate_object(item, path, full_page)
            path.pop()
            full_page=f"{full_page}</div>"
            # values.append(navigate_object(item))
    elif isinstance(obj, dict):
        for key, value in obj.items():
            full_page=f"{full_page}<div>{key}:</div>"
            full_page=f"{full_page}<div style='padding-left:10px'>"
            path.append(key)
            full_page=navigate_object(value, path, full_page)
            path.pop()
            full_page=f"{full_page}</div>"
            # values.append({key: navigate_object(value)})  # Preserve object structure
    return full_page


@app.route('/edit')
def edit():
    page="""
    <html>
        <body>
            <div>
                Inglese
                <a href="/edit/en">EDIT</a>
                <a href="/download/en">DOWNLOAD</a>

            </div>
            <div>
                Italiano
                <a href="/edit/it">EDIT</a>
                <a href="/download/it">DOWNLOAD</a>
            </div>
        </body>
    </html>
    """

    return page


@app.route('/edit/<language>')
def edit_lang(language='it'):
    page=file_manager(language)

    return page
    # return jsonify({"msg": page})

@app.route('/save/<language>', methods=['POST'])
def save(language='it'):
    # page=file_manager()
    print(request.get_data())
    # data = json.loads(request.get_data())
    # print(data)
    filename=f'./translations/{language}-b.yaml'

    with open(filename, 'r') as file:

        translation = yaml.safe_load(file)
    
    for key in request.form:
        print(key)
        items = key.split("_")
        print(f"NEW {request.form[key]}")
        item_to_replace = translation
        pointer_to_item_to_replace = None
        last_index=None
        for key_part in items:
            # if isinstance(key_part, str):
            # print("Key part:" + key_part)
            pointer_to_item_to_replace = item_to_replace
            last_index = key_part
            try:
                item_to_replace = item_to_replace[key_part]
            except Exception as e:
                print(e)
                item_to_replace = item_to_replace[int(key_part)]
        try:
            pointer_to_item_to_replace[last_index] = request.form[key]
        except Exception as e:
            print(e)
            pointer_to_item_to_replace[int(last_index)] = request.form[key]
        print(f"OLD: {item_to_replace}")
    
    with open(f"{filename}", 'w') as file:
        yaml.dump(translation, file)

    # return jsonify({"Saved": 1})
    return redirect("/edit", code=302)

@app.route('/download/<language>', methods=['GET'])
def download(language):
    source_filename=f'./translations/{language}-b.yaml'
    target_filename=f'./translations/{language}-b.json'
    with open(source_filename, 'r') as file:

        source_content = yaml.safe_load(file)

    output = json.dumps(source_content)
    target_file = open(target_filename, "w")
    target_file.write(output)
    target_file.close()
    return send_file(target_filename, as_attachment=True)
