from flask import Flask, request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Swayam@2006'
app.config['MYSQL_DB']='dcc_assignment_4'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/question1',methods=["GET","POST"])
def question1():
    if request.method=="POST":
    
        cursor=mysql.connection.cursor()
        cursor.execute("select * from eb_purchase_details where `Bond\nNumber` like %s",(request.form["box"],))
        purchase_data=cursor.fetchall()
        cursor.close()

        cursor=mysql.connection.cursor()
        cursor.execute("select * from eb_redemption_details where `Bond\nNumber` like %s",(request.form["box"],))
        redemption_data = cursor.fetchall()
        cursor.close()
        data_a1={"purchase_data": purchase_data,"redemption_data": redemption_data}
        return render_template('question1.html', data_a1=data_a1)
    return render_template('question1.html')



@app.route('/question2',methods=["GET","POST"])
def question2():
    cursor=mysql.connection.cursor()
    cursor.execute("select distinct `Name of the Purchaser` from `eb_purchase_details`")
    data=cursor.fetchall()
    dropdown_options=[row[0] for row in data]
    cursor.close()

    if request.method=="POST":
        if 'dropdown' in request.form:  
            selected_option=request.form["dropdown"]
            cursor=mysql.connection.cursor()
            cursor.execute(f"select * from eb_purchase_details where `Name of the Purchaser` = '{selected_option}'")
            data_a2=cursor.fetchall()
            cursor.close()
            return render_template('question2.html', dropdown_options=dropdown_options,data_a2=data_a2,selected_option=selected_option)
        
    return render_template('question2.html', dropdown_options=dropdown_options)



@app.route('/question3',methods=['GET', 'POST'])
def question3():
    cursor=mysql.connection.cursor()
    cursor.execute("select distinct `Name of the Purchaser` from eb_purchase_details")
    data=cursor.fetchall()
    dropdown_options=[row[0] for row in data]
    cursor.close()

    if request.method=="POST":
        if 'dropdown' in request.form:
            selected_option=request.form["dropdown"]
            cursor=mysql.connection.cursor()  
            cursor.execute("""select substring(`Date of\nPurchase`, -4) , count(`Bond\nNumber`) , sum(cast(replace(Denominations, ',', '') AS UNSIGNED)) from eb_purchase_details where `Name of the Purchaser` = %s group by substring(`Date of\nPurchase`, -4) """, (selected_option,))

            data_a3=cursor.fetchall()
            x_values=[row[0] for row in data_a3]
            y1_values=[row[1] for row in data_a3]
            y3_values=[]
            y2_values=[row[2] for row in data_a3]
            for i in y2_values:
                y3_values.append(int(i))
            cursor.close()
            return render_template('question3.html',data_a3=data_a3,dropdown_options=dropdown_options,selected_option=selected_option,x_values=x_values,y1_values=y1_values,y3_values=y3_values)
    return render_template('question3.html',dropdown_options=dropdown_options)



@app.route('/question4',methods=['GET','POST'])
def question4():
    cursor=mysql.connection.cursor()
    cursor.execute("select distinct `Name of the Political Party` from eb_redemption_details")
    dropdown_options=[row[0] for row in cursor.fetchall()]
    cursor.close()

    if request.method=="POST":
        if 'dropdown' in request.form:
            selected_option=request.form["dropdown"]
            cursor=mysql.connection.cursor()
            cursor.execute("""select substring(`Date of\nEncashment`, -4) , count(`Bond\nNumber`) , sum(cast(replace(Denominations, ',', '') as unsigned)) from eb_redemption_details where  `Name of the Political Party` = %s group by substring(`Date of\nEncashment`, -4)""", (selected_option,))
            
            data_a4=cursor.fetchall()
            x_values=[row[0] for row in data_a4]
            y1_values=[row[1] for row in data_a4]
            y3_values=[]
            y2_values=[row[2] for row in data_a4]
            for i in y2_values:
                y3_values.append(int(i))

            cursor.close()
            return render_template('question4.html',data_a4=data_a4,dropdown_options=dropdown_options,selected_option=selected_option,x_values=x_values,y1_values=y1_values,y3_values=y3_values)

    return render_template('question4.html',dropdown_options=dropdown_options)



@app.route('/question5',methods=["GET","POST"])
def question5():
    cursor=mysql.connection.cursor()
    cursor.execute("select distinct `Name of the Political Party` from eb_redemption_details")
    dropdown_options=[row[0] for row in cursor.fetchall()]
    cursor.close()
    
    if request.method=="POST":
        if 'dropdown' in request.form:
            selected_option=request.form["dropdown"]
            cursor=mysql.connection.cursor()
            cursor.execute("""select eb_purchase_details.`Name of the purchaser`, sum(cast(replace(eb_purchase_details.`Denominations`, ',', '') as decimal)) from eb_purchase_details join eb_redemption_details on eb_purchase_details.`Bond\nNumber` = eb_redemption_details.`Bond\nNumber` where eb_redemption_details.`Name of the Political Party` = %s group by eb_purchase_details.`Name of the purchaser` """, (selected_option,))
            data_a5 = cursor.fetchall()
            data_a6 = [row[1] for row in data_a5]
            sum=0
            for i in data_a6:
                sum+=int(i)
            cursor.close()
            return render_template('question5.html',data_a5=data_a5,dropdown_options=dropdown_options,selected_option=selected_option,sum=sum)
    return render_template('question5.html', dropdown_options=dropdown_options)

@app.route('/question6', methods=["GET","POST"])
def question6():
    cursor=mysql.connection.cursor()
    cursor.execute("select distinct `Name of the Purchaser` from eb_purchase_details")
    dropdown_options=[row[0] for row in cursor.fetchall()]
    cursor.close()
    if request.method=="POST":
        if 'dropdown' in request.form:
            selected_option=request.form["dropdown"]
            cursor=mysql.connection.cursor()
            cursor.execute("""select eb_redemption_details.`Name of The Political Party`, sum(cast(replace(eb_redemption_details.`Denominations`, ',', '') as decimal)) from eb_purchase_details join eb_redemption_details ON eb_purchase_details.`Bond\nNumber` = eb_redemption_details.`Bond\nNumber` where eb_purchase_details.`Name of the Purchaser` = %s group by eb_redemption_details.`Name of The Political Party` """, (selected_option,))
            data_a7=cursor.fetchall()
            data_a8=[row[1] for row in data_a7]
            count=0
            for i in data_a8:
                count+=int(i)
            cursor.close()
            return render_template('question6.html',data_a5=data_a7,dropdown_options=dropdown_options,selected_option=selected_option,count=count)
    return render_template('question6.html',dropdown_options=dropdown_options)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)