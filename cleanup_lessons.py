import firebase_admin
from firebase_admin import credentials, firestore
import time

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
    
    # Get all courses
    courses_ref = db.collection("Courses")
    courses = courses_ref.get()
    
    deleted_count = 0
    
    for course in courses:
        # Get lessons for this course
        lessons_ref = courses_ref.document(course.id).collection("Lessons")
        
        # Find and delete duplicate lessons
        for lesson_id in duplicates:
            lesson_doc = lessons_ref.document(lesson_id)
            try:
                if lesson_doc.get().exists:
                    lesson_doc.delete()
                    print(f"Deleted lesson: {lesson_id} from course: {course.id}")
                    deleted_count += 1
            except Exception as e:
                print(f"Error checking/deleting lesson {lesson_id}: {e}")
    
    print(f"Total deleted lessons: {deleted_count}")

def move_vocabulary_to_collection(db):
    # Get all courses
    courses_ref = db.collection("Courses")
    courses = courses_ref.get()
    
    # Create a batch for efficient writes
    batch = db.batch()
    count = 0
    batch_count = 0
    
    for course in courses:
        course_id = course.id
        print(f"Processing course: {course_id}")
        
        # Get lessons for this course
        lessons_ref = courses_ref.document(course_id).collection("Lessons")
        lessons = lessons_ref.get()
        
        for lesson in lessons:
            lesson_data = lesson.to_dict()
            lesson_id = lesson.id
            
            # Get vocabulary items
            vocab_items = lesson_data.get('vocabularyItems', [])
            
            if vocab_items:
                print(f"Found {len(vocab_items)} vocabulary items in lesson: {lesson_id}")
                
                # Add vocabulary items to Vocabulary collection
                for vocab in vocab_items:
                    vocab_id = vocab.get('id', '')
                    if not vocab_id:
                        continue
                    
                    # Add course and lesson reference
                    vocab['courseId'] = course_id
                    vocab['lessonId'] = lesson_id
                    
                    # Use a unique ID for the vocabulary document
                    unique_id = f"{lesson_id}_{vocab_id}".replace("/", "_")
                    
                    # Add to Vocabulary collection
                    vocab_ref = db.collection("Vocabulary").document(unique_id)
                    batch.set(vocab_ref, vocab)
                    count += 1
                    
                    # Commit batch every 500 operations (Firestore limit)
                    if count % 500 == 0:
                        batch.commit()
                        print(f"Committed batch of 500 vocabulary items (total: {count})")
                        batch = db.batch()
                        batch_count += 1
                        time.sleep(1)  # Avoid rate limiting
    
    # Commit any remaining operations
    if count % 500 != 0:
        batch.commit()
        batch_count += 1
    
    print(f"Total vocabulary items moved: {count} in {batch_count} batches")

def main():
    print("Connecting to Firebase...")
    db = initialize_firebase()
    
    # Delete duplicate lessons
    print("\nDeleting duplicate lessons...")
    delete_duplicate_lessons(db)
    
    # Move vocabulary to separate collection
    print("\nMoving vocabulary to Vocabulary collection...")
    move_vocabulary_to_collection(db)
    
    print("\nCleanup complete!")

if __name__ == "__main__":
    main() 