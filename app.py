from flask import Flask
from flask import render_template 
from flask import request

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


app =Flask(__name__)



@app.route("/" , methods = ["GET" , "POST"])# this shows directory of website and bydefault get method called if no method mntined
def home():
    
    if request.method =="GET":
        return render_template("index.html")
    elif request.method == "POST":
        file = open("data.csv" ,"r")
        data=[]
        for row in file.readlines()[1:]:
            data.append(list(map(int,row.strip().split(","))))
        selcted = request.form.get("ID")
        entered = request.form["id_value"]
        if not selcted or not entered:
            return render_template("error.html")
        elif selcted =="course_id":
            try:
                
                

                #paste here if issue
                sum=0
                count=0
                maxi=0
                marksc=[]
                for row in data:
                    if row[1]==int(entered):
                        marksc.append(row[2])
                        sum= sum+row[2]
                        count+=1
                        if row[2]>maxi:
                            maxi=row[2]

                avg=sum/count
                
                #grades = df[df["Course id"] == int(entered)]["Marks"]
                plt.hist(marksc, edgecolor='black')

                # Add titles and labels
                plt.xlabel('Marks')
                plt.ylabel('frequency')
                
               
                plt.savefig("static/histogram.png")
                plt.close()
                
                return render_template("coursedetail.html",average_marks=avg, maximum_marks = maxi)
                
                
            
            except Exception as e:
              return render_template("error.html")
        elif selcted=="student_id":
            totalmarks=0
            for row in data:
                if row[0]==int(entered):
                    totalmarks= totalmarks+row[2]

            if totalmarks==0:
                return render_template("error.html")
            return render_template("studentdetail.html" , data =data , total_marks_data=totalmarks,value=int(entered))   

        

    


if __name__ == "__main__":
    app.debug = True # not for producitn as exact error is shown and can be potential reaveling danger of data
    app.run()