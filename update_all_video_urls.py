#!/usr/bin/env python3
import os
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def update_all_video_urls(target_url="https://www.youtube.com/watch?v=kFYgLjdSkXE"):
    """
    Update all videoUrl fields in Firebase (both in Lessons and Questions)
    to point to the specified YouTube URL.
    """
    
    print(f"Starting to update all videoUrl fields to: {target_url}")
    
    # Check for specific Firebase credential files in the expected locations
    possible_files = [
        'firebase_config.json',
        'train model python/firebase_config.json',
        'train model python/englishlearningapp-30b00-firebase-adminsdk-fbsvc-3c16f54503.json'
    ]
    
    credential_file = None
    for file_path in possible_files:
        if os.path.exists(file_path):
            credential_file = file_path
            print(f"Using credential file: {credential_file}")
            break
    
    if credential_file is None:
        print("Error: No Firebase credential file found. Please place either:")
        print("- firebase_config.json in the current directory")
        print("- or the Admin SDK JSON file in the train model python directory")
        return
    
    # Initialize Firebase
    try:
        cred = credentials.Certificate(credential_file)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase connection successful!")
    except Exception as e:
        print(f"Error connecting to Firebase: {e}")
        return
    
    # Create a log file to track changes
    log_file = f"video_url_updates_{time.strftime('%Y%m%d_%H%M%S')}.log"
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"Video URL Update Log - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Target URL: {target_url}\n\n")
    
    total_updated = 0
    
    # 1. Update Lessons
    total_updated += update_lesson_videos(db, target_url, log_file)
    
    # 2. Update Questions
    total_updated += update_question_videos(db, target_url, log_file)
    
    print(f"\nUpdate complete! Total items updated: {total_updated}")
    print(f"Log file created: {log_file}")
    
    # Log final statistics
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\nFinal Summary:\n")
        f.write(f"Total items updated: {total_updated}\n")
        f.write(f"Completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

def update_lesson_videos(db, target_url, log_file):
    """Update videoUrl in all lessons"""
    print("\n===== Updating Lesson Videos =====")
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write("\n===== LESSONS =====\n")
    
    total_courses = 0
    total_lessons = 0
    updated_lessons = 0
    
    try:
        # Fetch all courses
        courses_ref = db.collection('Courses')
        courses = courses_ref.stream()
        
        # Loop through all courses
        for course in courses:
            total_courses += 1
            course_id = course.id
            course_data = course.to_dict()
            course_name = course_data.get('title', course_data.get('name', 'Unknown'))
            print(f"Processing course: {course_id} - {course_name}")
            
            # Log to file
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"Course: {course_id} - {course_name}\n")
            
            # Get all lessons for this course
            lessons_ref = db.collection('Courses').document(course_id).collection('Lessons')
            lessons = lessons_ref.stream()
            
            # Update each lesson's videoUrl
            for lesson in lessons:
                total_lessons += 1
                lesson_id = lesson.id
                lesson_data = lesson.to_dict()
                
                # Check if the videoUrl field exists and needs updating
                old_url = lesson_data.get('videoUrl', 'None')
                
                if 'videoUrl' in lesson_data and lesson_data['videoUrl'] != target_url:
                    print(f"  Updating lesson: {lesson_id}")
                    print(f"  Old URL: {old_url}")
                    lessons_ref.document(lesson_id).update({'videoUrl': target_url})
                    updated_lessons += 1
                    
                    # Log to file
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(f"  - Lesson: {lesson_id}\n")
                        f.write(f"    Old URL: {old_url}\n")
                        f.write(f"    New URL: {target_url}\n")
                    
                    time.sleep(0.1)  # Small delay to avoid hitting quota limits
                elif 'videoUrl' not in lesson_data:
                    print(f"  Adding videoUrl to lesson: {lesson_id}")
                    lessons_ref.document(lesson_id).update({'videoUrl': target_url})
                    updated_lessons += 1
                    
                    # Log to file
                    with open(log_file, 'a', encoding='utf-8') as f:
                        f.write(f"  - Lesson: {lesson_id}\n")
                        f.write(f"    Added URL: {target_url}\n")
                    
                    time.sleep(0.1)  # Small delay to avoid hitting quota limits
        
        print(f"\nLesson update complete!")
        print(f"Total courses processed: {total_courses}")
        print(f"Total lessons found: {total_lessons}")
        print(f"Lessons updated: {updated_lessons}")
        
        # Log statistics
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\nLesson Summary:\n")
            f.write(f"Total courses processed: {total_courses}\n")
            f.write(f"Total lessons found: {total_lessons}\n")
            f.write(f"Lessons updated: {updated_lessons}\n")
        
        return updated_lessons
        
    except Exception as e:
        print(f"Error updating lesson video URLs: {e}")
        # Log error to file
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\nERROR in lessons update: {e}\n")
        return 0

def update_question_videos(db, target_url, log_file):
    """Update videoUrl in all questions (tests and exam questions)"""
    print("\n===== Updating Question Videos =====")
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write("\n===== QUESTIONS =====\n")
    
    total_questions = 0
    updated_questions = 0
    
    collections_to_check = [
        'Tests',        # For main test questions 
        'Questions',    # For standalone questions
        'examQuestions' # For exam specific questions
    ]
    
    try:
        for collection_name in collections_to_check:
            print(f"\nChecking collection: {collection_name}")
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"\nCollection: {collection_name}\n")
            
            # Some questions might be directly in the collection
            questions_ref = db.collection(collection_name)
            questions = questions_ref.stream()
            
            for question in questions:
                total_questions += 1
                question_id = question.id
                question_data = question.to_dict()
                
                # Check for videoUrl in the question
                if 'videoUrl' in question_data:
                    old_url = question_data['videoUrl']
                    if old_url != target_url:
                        print(f"  Updating question: {question_id}")
                        print(f"  Old URL: {old_url}")
                        questions_ref.document(question_id).update({'videoUrl': target_url})
                        updated_questions += 1
                        
                        # Log to file
                        with open(log_file, 'a', encoding='utf-8') as f:
                            f.write(f"  - Question: {question_id}\n")
                            f.write(f"    Old URL: {old_url}\n")
                            f.write(f"    New URL: {target_url}\n")
                        
                        time.sleep(0.1)  # Small delay to avoid hitting quota limits
        
        # Now check for nested questions inside test models
        print("\nChecking for questions inside test models...")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write("\nTest Models with Questions:\n")
        
        # Get all test models
        tests_ref = db.collection('Tests')
        tests = tests_ref.stream()
        
        for test in tests:
            test_id = test.id
            test_data = test.to_dict()
            
            # Check if test has partQuestions array
            if 'partQuestions' in test_data and isinstance(test_data['partQuestions'], list):
                print(f"Processing test: {test_id} - Has partQuestions")
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f"Test: {test_id}\n")
                
                parts_updated = False
                part_questions = test_data['partQuestions']
                
                # Loop through each part (which is a list of questions)
                for part_index, part in enumerate(part_questions):
                    if isinstance(part, list):
                        # Loop through questions in this part
                        for q_index, question in enumerate(part):
                            total_questions += 1
                            if 'videoUrl' in question:
                                old_url = question['videoUrl']
                                if old_url != target_url:
                                    print(f"  Updating question in test {test_id}, part {part_index+1}, question {q_index+1}")
                                    part_questions[part_index][q_index]['videoUrl'] = target_url
                                    parts_updated = True
                                    updated_questions += 1
                                    
                                    # Log to file
                                    with open(log_file, 'a', encoding='utf-8') as f:
                                        f.write(f"  - Question in part {part_index+1}, index {q_index+1}\n")
                                        f.write(f"    Old URL: {old_url}\n")
                                        f.write(f"    New URL: {target_url}\n")
                
                # Update the test document if any questions were changed
                if parts_updated:
                    tests_ref.document(test_id).update({'partQuestions': part_questions})
                    print(f"  Updated test: {test_id}")
                    time.sleep(0.2)  # Slightly longer delay for larger updates
        
        print(f"\nQuestion update complete!")
        print(f"Total questions checked: {total_questions}")
        print(f"Questions updated: {updated_questions}")
        
        # Log statistics
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\nQuestion Summary:\n")
            f.write(f"Total questions checked: {total_questions}\n")
            f.write(f"Questions updated: {updated_questions}\n")
        
        return updated_questions
        
    except Exception as e:
        print(f"Error updating question video URLs: {e}")
        # Log error to file
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\nERROR in questions update: {e}\n")
        return 0

if __name__ == "__main__":
    update_all_video_urls() 