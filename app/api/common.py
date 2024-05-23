from flask import Blueprint, request, current_app
import trafilatura
common_api = Blueprint("common_api", __name__)


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
    input = request.get_json()
    html = ''
    if 'raw_html' in input:
        html = input['raw_html']
    else:
        html = trafilatura.fetch_url(input['url'])
    article = trafilatura.extract(html)
    return {"text": article}
