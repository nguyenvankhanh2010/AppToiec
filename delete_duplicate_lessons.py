import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    # Initialize Firebase if not already initialized
    try:
        app = firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate("scripts/firebase_config.json")
        app = firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    return db

def delete_duplicate_lessons(db):
    # Lessons to delete (with pattern toeic_lesson_1_X)
    duplicates = [
        "toeic_lesson_1_1", 
        "toeic_lesson_1_2", 
        "toeic_lesson_1_3"
    ]
    
    # Get courses collection
    courses_ref = db.collection("Courses")
    
    # For each course, check if it has the duplicate lessons
    for course_doc in courses_ref.stream():
        course_id = course_doc.id
        print(f"Checking course: {course_id}")
        
        # Get lessons subcollection
        lessons_ref = courses_ref.document(course_id).collection("Lessons")
        
        # Try to delete each duplicate lesson
        for lesson_id in duplicates:
            try:
                lesson_doc = lessons_ref.document(lesson_id)
                snapshot = lesson_doc.get()
                
                if snapshot.exists:
                    print(f"Deleting lesson: {lesson_id} from course: {course_id}")
                    lesson_doc.delete()
                    print(f"Successfully deleted: {lesson_id}")
            except Exception as e:
                print(f"Error with lesson {lesson_id}: {str(e)}")

def main():
    print("Connecting to Firebase...")
    db = initialize_firebase()
    
    print("\nDeleting duplicate lessons...")
    delete_duplicate_lessons(db)
    
    print("\nCleanup complete!")

if __name__ == "__main__":
    main() 