from flask import Flask, request, json, jsonify
from sqlalchemy import create_engine
from sqlalchemy.sql import text

app = Flask(__name__)

conn_str = 'postgresql://postgres:123098@localhost:5432/latihan'
engine = create_engine(conn_str, echo=False)
    
@app.route('/employee/leave', methods=['GET'])
def get_employee_leaves():
    body = request.json.get
    start_d = body('start_date')
    end_d = body('end_date')
    list = []
    with engine.connect() as connection:
        query = text("select e.nik, e.name, sum(date_part('day', end_date-start_date)+1) as total_cuti from employee e join leave l on e.nik = l.employee_nik where start_date >= :start and end_date <= :end group by e.nik, e.name")
        result = connection.execute(query, start = start_d, end = end_d)
        for row in result:
            list.append({"nik":row['nik'], "nama":row['name'], "total_cuti":row['total_cuti']})
    return jsonify(list)
    
if __name__=="__main__":
    app.run(debug=True)