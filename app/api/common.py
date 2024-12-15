from flask import Blueprint, request, current_app, jsonify
import trafilatura
import os

common_api = Blueprint("common_api", __name__)

def verify_api_key(api_key):
    valid_api_key = os.getenv('API_KEY')
    return api_key == valid_api_key

@common_api.route("/")
def entry_status():
    """
    metric api

    response success when server is up
    ---
    tags:
        -   common
    responses:
        200:
            description: server ping-pong response
            schema:
                name: ServerMetircResponse
                type: object
                properties:
                    code:
                        type: integer
                    docs:
                        type: string
                        default: http://127.0.0.1:5000/apidocs
                    service:
                        type: string
    """

    return {
        "service": current_app.config["SWAGGER"]["title"],
        "code": 200,
        "docs": f"{request.url_root}apidocs"
    }

@common_api.post("/extract")
def extract():
    # json api
    """
    extract api by trafilatura
    ---
    tags:
        -   common
    parameters:
        -   in: header
            name: X-API-Key
            required: true
            type: string
            description: API key for authentication
        -   in: body
            name: body
            required: true
            schema:
                name: ExtractRequest
                type: object
                properties:
                    url:
                        type: string
                        description: url to extract
                    raw_html:
                        type: string
                        description: raw html to extract
                    output_options:
                        type: object
                        description: options for trafilatura extraction
                        properties:
                            include_comments:
                                type: boolean
                            include_tables:
                                type: boolean
                            include_links:
                                type: boolean
                            include_formatting:
                                type: boolean
                            include_images:
                                type: boolean
                            output_format:
                                type: string
                                enum: [csv, json, html, markdown, txt, xml, xmltei]
                            with_metadata:
                                type: boolean
                            favor_precision:
                                type: boolean
                            favor_recall:
                                type: boolean
    responses:
        200:
            description: extract response
            schema:
                name: ExtractResponse
                type: object
                properties:
                    text:
                        type: string
    """
    api_key = request.headers.get('X-API-Key')
    if not verify_api_key(api_key):
        return jsonify({"error": "Invalid API key"}), 403

    input = request.get_json()
    html = input.get('raw_html', '') or trafilatura.fetch_url(input['url'])
    output_options = input.get('output_options', {})
    extract_params = {
        'include_comments': output_options.get('include_comments', True),
        'include_tables': output_options.get('include_tables', True),
        'include_links': output_options.get('include_links', False),
        'include_formatting': output_options.get('include_formatting', False),
        'include_images': output_options.get('include_images', False),
        'output_format': output_options.get('output_format', 'txt'),
        'with_metadata': output_options.get('with_metadata', False),
        'favor_precision': output_options.get('favor_precision', False),
        'favor_recall': output_options.get('favor_recall', False),
    }
    article = trafilatura.extract(html, **extract_params)
    return {"output": article}
