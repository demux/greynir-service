import json

# from app.utils import get_sentence_lemmas
from flask import current_app as app, request, Response
from reynir import Reynir
from reynir.bintokenizer import tokenize
from reynir.bindb import BIN_Meaning
from tokenizer import TOK

r = Reynir()

def json_response(data):
    return Response(json.dumps(data, ensure_ascii=False, indent=2),
                    content_type='application/json')


# @app.route('/parse/', methods=('GET', 'POST'))
# def parse_api():
#     if request.method == 'GET':
#         text = request.args.get('text')
#     else:
#         text = request.get_data(as_text=True)

#     job = r.parse(text)

#     return json_response([{
#         **s.dump(),
#         'lemmas': list(get_sentence_lemmas(s)),
#     } for s in job['sentences']])


@app.route('/tokenize/', methods=('GET', 'POST'))
def tokenize_api():
    if request.method == 'GET':
        text = request.args.get('text')
    else:
        text = request.get_data(as_text=True)

    def serialize_token_val(tok_val):
        if tok_val is None:
            return None
        for val in tok_val:
            if isinstance(val, BIN_Meaning):
                yield val._asdict()
            else:
                yield val

    return json_response([{
        'kind': TOK.descr[tok.kind],
        'txt': tok.txt,
        'val': list(serialize_token_val(tok.val)),
    } for tok in tokenize(text)])
