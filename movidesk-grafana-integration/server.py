from requests import get
from pandas import DataFrame
from flask import Flask, make_response, jsonify, request
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

comparasion_translate = {
    '=': 'eq',
    '!=': 'ne',
    '>': 'gt',
    '<': 'lt'
}

def convert_dict_format(movidesk_response):
    df = DataFrame(movidesk_response)
    columns = list(df.columns)
    columns.reverse()
    types = [df[column].dtype.name for column in columns]
    columns = [{'text': text, 'type': dtype} for text, dtype in tuple(zip(columns, types))]
    rows = [row.tolist() for row in df.values]
    grafana_response = [{'columns': columns, 'rows': rows}]

    return grafana_response


app = Flask(__name__)


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
    return make_response(jsonify(my_dropdown_items))


@app.route('/query', methods=['GET', 'POST', 'OPTIONS'])
def query_request():
    query_data = request.get_json()
    query_type = query_data['targets'][0]['type']
    print(query_data)
    response = []

    if query_type == 'table':
        targets = query_data['targets'][0]
        params = {'token': f"{config['movidesk']['API_TOKEN']}",
                  '$select': f'{targets["target"]}',
                  '$filter': f'createdDate ge {query_data["range"]["from"]} '
                             f'and createdDate le {query_data["range"]["to"]}'}

        for filtro in query_data['adhocFilters']:
            params['$filter'] += f' and {filtro["key"]} ' \
                                 f'{comparasion_translate[filtro["operator"]]} ' \
                                 f"'{filtro['value']}'"

        response = get(config['movidesk']['API_DOMAIN'], params).json()

    elif query_type == 'timeserie':
        pass

    movidesk_response = convert_dict_format(response)
    movidesk_response[0]['type'] = query_type
    print(movidesk_response)
    return make_response(jsonify(movidesk_response))


@app.route('/annotations')
def annotation_request():
    resp = make_response([])
    return jsonify(resp)


if __name__ == "__main__":
    app.run(debug=True, port=config['movidesk']['PORT'], threaded=True)
