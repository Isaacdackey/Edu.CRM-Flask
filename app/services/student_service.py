from app import db
from app.models import User, Student

def list_students(page=1, per_page=5, search=None):
    """Récupère les étudiants avec pagination et recherche"""
    query = db.session.query(User, Student).join(
        Student, User.id == Student.id
    )
    
    if search:
        query = query.filter(User.name.ilike(f'%{search}%'))
    
    offset = (page - 1) * per_page
    total = query.count()
    
    students_data = query.offset(offset).limit(per_page).all()
    
    result = []
    for user, student in students_data:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })
    
    return {
        "students": result,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page
    }

def add_student(student_data):
    """Ajoute un étudiant dans la base de données"""
    from app.models import User
    
    name_parts = student_data["name"].strip().split()
    
    user = User(
        name=student_data["name"],
        email=student_data["email"],
        password="passer",
        role="student"
    )
    db.session.add(user)
    db.session.flush()
    
    student = Student(id=user.id)
    db.session.add(student)
    db.session.commit()
    
    return {"id": user.id, "name": user.name, "email": user.email, "password": "passer"}

def get_student_by_id(student_id):
    """Récupère un étudiant par son ID"""
    student = Student.query.get(student_id)
    if student:
        user = User.query.get(student_id)
        if user:
            return {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
    return None

def delete_student(id):
    """Supprime un étudiant"""
    from app.models import CourseAssignment
    
    try:
        student = Student.query.get(id)
        if student:
            CourseAssignment.query.filter_by(student_id=id).delete()
            db.session.delete(student)
            
            user = User.query.get(id)
            if user:
                db.session.delete(user)
            
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        raise e
    
def get_students_count():
    """Retourne le nombre total d'étudiants"""
    from app.models import Student
    return Student.query.count()