from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

UPSTREAM_URL = "https://1.4399.vu/api/createOrder"


@app.route("/api/transform", methods=["POST"])
def transform():
    data = request.get_json(silent=True) or request.form.to_dict()
    required = ["tid", "user", "pass"]
    for k in required:
        if k not in data:
            return jsonify({"error": f"missing param {k}"}), 400

    try:
        upstream_resp = requests.post(
            UPSTREAM_URL,
            data={
                "tid": data["tid"],
                "user": data["user"],
                "pass": data["pass"],
                "input1": data.get("input1", "test"),
                "num": data.get("num", "1"),
            },
            timeout=10,
            proxies={},
        )
        upstream_resp.raise_for_status()
        upstream_json = upstream_resp.json()
    except Exception as e:
        return jsonify({"error": f"upstream failed: {e}"}), 502

    delivery_content = ""
    kmdata = upstream_json.get("kmdata")
    if isinstance(kmdata, list) and len(kmdata) > 0:
        delivery_content = kmdata[0].get("card", "")

    result = {
        "DELIVERY_CONTENT": delivery_content,
        "order_id": upstream_json.get("orderid", ""),
        "item_id": data.get("tid", ""),
        "item_title": "",
        "buyer_name": "",
        "buyer_id": "",
        "seller_name": "",
    }
    return delivery_content


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
