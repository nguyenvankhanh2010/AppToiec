import firebase_admin
from firebase_admin import credentials, firestore
import json

def initialize_firebase():
    # Initialize Firebase if not already initialized
    try:
        app = firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate("scripts/firebase_config.json")
        app = firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    return db

def display_courses(db):
    # Get all courses
    courses_ref = db.collection("Courses")
    courses = courses_ref.get()
    
    print(f"\n=== COURSES ({len(courses)}) ===")
    
    for course in courses:
        course_data = course.to_dict()
        print(f"\nCourse ID: {course_data.get('courseId')}")
        print(f"Title: {course_data.get('title')}")
        print(f"Description: {course_data.get('description')}")
        print(f"Category: {course_data.get('category')}")
        print(f"Duration: {course_data.get('duration')}")
        
        # Get lessons for this course
        lessons_ref = courses_ref.document(course.id).collection("Lessons")
        lessons = lessons_ref.get()
        
        print(f"\n  --- Lessons ({len(lessons)}) ---")
        
        for lesson in lessons:
            lesson_data = lesson.to_dict()
            print(f"\n  Lesson ID: {lesson_data.get('lessonId')}")
            print(f"  Title: {lesson_data.get('title')}")
            print(f"  Duration: {lesson_data.get('duration')}")
            print(f"  Vocabulary Count: {lesson_data.get('vocabulary_count')}")
            
            # Display first 2 vocabulary words as example
            vocab_items = lesson_data.get('vocabularyItems', [])
            if vocab_items:
                print("  Sample vocabulary:")
                for i, vocab in enumerate(vocab_items[:2]):
                    print(f"    {i+1}. {vocab.get('english')} - {vocab.get('vietnamese')}")
                    if vocab.get('example'):
                        print(f"       Example: {vocab.get('example')}")

def display_tests(db):
    # Get all tests
    tests_ref = db.collection("Tests")
    tests = tests_ref.get()
    
    print(f"\n=== TESTS ({len(tests)}) ===")
    
    for test in tests:
        test_data = test.to_dict()
        print(f"\nTest ID: {test_data.get('testId')}")
        print(f"Title: {test_data.get('title')}")
        print(f"Description: {test_data.get('description')}")
        print(f"Duration: {test_data.get('duration')}")
        print(f"Pass Score: {test_data.get('passScore')}")
        
        # Get question counts by type
        questions = test_data.get('questions', {})
        for q_type, q_list in questions.items():
            print(f"  {q_type.capitalize()} Questions: {len(q_list)}")
        
        # Display example questions
        if questions:
            print("\n  Sample questions:")
            
            # Show one listening question
            if questions.get('listening'):
                q = questions['listening'][0]
                print(f"  Listening: {q.get('questionText')}")
                print(f"    Options: {', '.join(q.get('options')[:2])}...")
                print(f"    Correct Answer: {q.get('correctAnswer')}")
            
            # Show one reading question
            if questions.get('reading'):
                q = questions['reading'][0]
                print(f"  Reading: {q.get('questionText')}")
                print(f"    Options: {', '.join(q.get('options')[:2])}...")
                print(f"    Correct Answer: {q.get('correctAnswer')}")

def main():
    print("Connecting to Firebase...")
    db = initialize_firebase()
    
    # Display courses and their lessons
    display_courses(db)
    
    # Display tests
    display_tests(db)
    
    print("\nVerification complete!")

if __name__ == "__main__":
    main() 