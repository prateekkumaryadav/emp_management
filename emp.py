import logging
from flask import Flask, jsonify, request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
log = logging.getLogger("emp-api")


app = Flask(__name__)

emp = [{
 "emp-101": { "name": "Asha", "daysLeft": 5 },
 "emp-102": { "name": "Ravi", "daysLeft": 1 }
}]

leave = {}

# pending = []


@app.route('/emp', methods=['GET'])
def emp_details():
    log.info("GET /emp - returning %d books", len(emp))
    return jsonify(emp)

@app.route('/total_leaves', methods=['GET'])
def leaves_details():
    log.info("GET /total_leaves - returning %d books", len(leave))
    return jsonify(leave)

'''
Request shape
POST /leaves
{ "employeeId": "emp-101", "days": 2, "reason": "Family function" }
'''

@app.route('/leaves', methods=['POST'])
def apply_leave():
    cur_req = request.json
    log.info("POST /books body=%s", cur_req)
    # leave.append(cur_req)
    cur_req["status"] = "PENDING"
    cur_req["leaveId"] = f"lv-{len(leave)}"
    log.info("Book added id=%s", f"lv-{len(leave)}")
    leave[cur_req["leaveId"]] = cur_req
    # i+=1
    return jsonify(cur_req), 201

@app.route('/leaves/<int:lv_id>/approve', methods=['POST'])
def approval(lv_id):
    cur_req = leave[f"{lv_id}"]
    data = request.get_json(silent=True)
    data.pop("status", None)  # don't allow changing the id
    data["statues"]="Approved"  # don't allow changing the id
    
    # book.update(data)
    # log.info("Book updated id=%d", book_id)
    return jsonify(data)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5100, debug=True)