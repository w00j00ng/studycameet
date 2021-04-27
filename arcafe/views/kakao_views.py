from flask import Blueprint, request, jsonify


bp = Blueprint('kakao', __name__, url_prefix='/kakao/')

@bp.route('/', methods=['POST'])
def chatbot():
    content = request.get_json()
    content = content['userRequest']['utterance']

    if content=='책구매':
        print('------책구매------')
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleImage": {
                        "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg",
                        "altText": "보물상자입니다"
                         }
                    }
                ]
            }
        }

    return jsonify(dataSend)