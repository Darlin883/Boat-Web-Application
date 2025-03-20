from flask import Flask,render_template, request
from sqlalchemy import create_engine, text, update

# __name__ is a special python variable that holds the name of the current module
# root file of the application

"""
previous practice
"""
# # hello
# @app.route('/hello')
# def servingHello():
#     return f"Hello"

# @app.route('/hello/<name>')
# def servingHelloToName(name):
#     return f"Hello, {name}"

# @app.route("/hello/<int:num>")
# def servingHelloToNum(num):
#     return f"The next number is, {num + 1}"

# # donut
# @app.route('/donuts')
# def servingDonut():
#     return "here is your donut"

# @app.route('/<name>')
# def greeting(name):
    # return render_template('user.html', user = name)
"""
previous practice
"""

app = Flask(__name__)
# connection string is in the format mysql://user:password@server/database
conn_str = "mysql://root:cset155@localhost/boatdb"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/') # home route
def hello():
    return render_template('index.html')

# -------------
# BOAT DATABASE
# -------------
@app.route('/boats')
def boats():
    boats = conn.execute(text("select * from boats")).all()
    # for boat in boats:
    #     print(boat)
    return render_template('boats.html', boats = boats)

# ---------------
# CREATE BOAT
# ---------------
@app.route('/createboat', methods = ['GET'])
def getBoat():
    return render_template('createboat.html')

@app.route('/createboat', methods = ['POST'])
def createBoat():
    # debugging checking if we are getting data
    # data = request.form
    # print(data)
    try:
        conn.execute(text("insert into boats values(:id, :name, :type, :owner_id, :rental_price)"), request.form)# research other way
        conn.commit() # to add to the database
        return render_template('createboat.html', error = None, success = "Successfull")
    except:
        return render_template('createboat.html', error = "Failed", success = None)
    
# --------------
# UPDATE BOAT
# --------------
@app.route('/updateboat', methods = ['GET'])
def getToUpdateBoat():
    return render_template('update.html')

@app.route('/updateboat', methods = ['POST'])
def updateBoat():
        result = conn.execute(text("update boats set name = :name, type = :type, owner_id = :owner_id, rental_price = :rental_price where id = :id"), request.form)
        conn.commit()
        
        if result.rowcount == 0:  # If no rows were updated, ID doesn't exist
                return render_template('update.html', error="ID does not exist", success=None)
        else:  
            return render_template('update.html', error = None, success = "Successfull update")

# ------------
# SEARCH BOAT
# ------------
@app.route('/searchboat', methods = ['GET'])
def search():
    boats = []
    return render_template('search.html', boats = boats)

@app.route('/searchboat', methods = ['POST'])
def searchBoat():
    try:
        boats = conn.execute(text("select * from boats where id = :id"), request.form).all()
        return render_template('search.html', boats = boats, error = None, success = "success")
    except:
        return render_template('search.html', boats = boats, error = "nope", success = None)
 
 
# ------------
# DELETE BOAT
# ------------   
@app.route('/deleteboat', methods = ['GET'])
def delete():
    boats = conn.execute(text("select * from boats")).all()
    return render_template('delete.html', boats=boats)

@app.route('/deleteboat', methods = ['POST'])
def deleteBoat():
    
    conn.execute(text("delete from boats where id = :id"), request.form)
    # window.relaod
    boats = conn.execute(text("select * from boats")).all()
    conn.commit()
    return render_template('delete.html',boats = boats) 

if __name__ == '__main__':
    app.run(debug=True)