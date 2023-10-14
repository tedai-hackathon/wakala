
from flask import Flask, jsonify, make_response, request
from utils import create_chat,get_market_agent,get_vectortool
from langchain.vectorstores import Chroma

app = Flask(__name__)
# app.run(debug=True, use_reloader=False)
# app.run(host='127.0.0.1',port=8000,debug=True)

conversation = create_chat()
vector_tool = get_vectortool()

@app.route("/reset", methods = ['POST'])
def reset():
    global conversation
    global vector_tool
    conversation = create_chat()
    vector_tool = get_vectortool()
    return make_response(jsonify({"response": {"response_code": 200}}))

@app.route("/market", methods = ['POST'])
def market():
    tools = [vector_tool]
    agent = get_market_agent(tools)
    data = request.json
    data = data.get("request","")
    d = data.get("data","")
    farmer,product,quantity,message = d.get("farmer",""),d.get("product",""),d.get("quantity",""),d.get("message","")
    prompt = f"""
    Human:
    {message}

    1. Find the markets that sell {product}
    2. Of those markets, find the market with the highest price
    3. In your response, include the following data in a single sentence in prose:
    - date : the date of the price
    - market : the market with the highest price matching the product
    - price : the price of the product at the market

    """
    print(prompt)

    try:
        message = agent.run(prompt)
        return make_response(
            jsonify({"response": {"message": message, "data": data["data"], "state":3, "response_code": 200}})
                              )
    except:
        return make_response(
            jsonify({"response": {"message": "Sorry, I don't understand. Please try again.", "data": data["data"], "state":3, "response_code": 400}})
                              )
    
@app.route("/chat", methods = ['POST'])
def chat():
    if not request.is_json:
        return make_response(
            jsonify(
                {"success": False,
                 "error": "Unexpected error, request is not in JSON format"}),
            400)

    # data = request.json
    # print(conversation(data["message"]))

    try:
        data = request.json
        message = conversation(data["message"])
        # print(message)
        msg = eval(message['text'])
        # print(msg)

        return make_response(
            jsonify({"response":{
                "data": msg["data"],"message":msg["message"], "state": msg["state"], "response_code":200}}))

        # return jsonify(eval(message['text']), status=200, mimetype='application/json')
    
    except:
        return make_response(
            jsonify({"response": False, "data": "na", "state": "na", "data": "na"}),400)