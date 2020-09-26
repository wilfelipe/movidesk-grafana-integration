from requests import get
from pandas import DataFrame
import os
from flask import Flask, make_response, jsonify, request

app = Flask(__name__)


def convert_dict_format(movidesk_response):
    df = DataFrame(movidesk_response)
    columns = list(df.columns)
    types = [df[column].dtype.name for column in columns]
    columns = [{'text': text, 'type': dtype} for text, dtype in tuple(zip(columns, types))]
    rows = [row.tolist() for row in df.values]
    grafana_response = [{'columns': columns, 'rows': rows}]

    return grafana_response


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response


@app.route('/')
def test_request():
    return make_response("ok")


@app.route('/search', methods=['GET', 'POST'])
def search_request():
    my_dropdown_items = []
    query_data = request.get_json()

    if query_data.get('target') == "server_list":
        my_dropdown_items += ['here', 'are', 'some', 'things', 'for', 'the', 'dropdowns']

    elif query_data.get('target') == "server_values":
        my_dropdown_items += [{'text': 'here', 'value': 'key1'}, {'text': 'another', 'value': 'key2'}]

    return make_response(jsonify(my_dropdown_items))


@app.route('/query', methods=['GET', 'POST', 'OPTIONS'])
def query_request():
    query_data = request.get_json()
    query_type = query_data['targets'][0]['type']
    print(query_data)
    response = []

    if query_type == 'table':
        targets = query_data['targets'][0]
        params = {'token': f"{os.environ['MOVIEDESKTOKEN']}",
                  '$select': f'{targets["target"]}',
                  '$filter': 'createdDate gt 2016-09-01T00:00:00.00z'}
        url = 'https://api.movidesk.com/public/v1/tickets'
        response = get(url, params).json()

    elif query_type == 'timeserie':  # Se query igual a timeseries
        pass

    movidesk_response = convert_dict_format(response)
    movidesk_response[0]['type'] = query_type
    return make_response(jsonify(movidesk_response))


@app.route('/annotations')
def annotation_request():
    resp = make_response([])
    return jsonify(resp)


if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
