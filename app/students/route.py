from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.student_service import *
from app.auth.decorators import *

students_bp = Blueprint("students", __name__)

@students_bp.route("/")
@login_required
def students_list():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    result = list_students(page=page, search=search)
    
    return render_template("students/students.html", 
                         students=result['students'],
                         total=result['total'],
                         page=result['page'],
                         total_pages=result['total_pages'],
                         search=search)

@students_bp.route("/create", methods=["GET","POST"])
@login_required
@roles_required('admin', 'teacher')  
def create_student():
    if request.method == "POST":
        student = {
            "name": request.form["name"],
            "email": request.form["email"]
        }
        
        new_student = add_student(student)
        flash(f"Étudiant {new_student['name']} créé avec succès! Mot de passe: {new_student['password']}", "success")
        
        return redirect(url_for("students.students_list"))
    
    return render_template("students/create_student.html")

@students_bp.route("/delete/<int:id>")
@login_required
@roles_required('admin')  
def delete(id):
    delete_student(id)
    flash("Student deleted", "info")
    return redirect(url_for("students.students_list"))

