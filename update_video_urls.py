#!/usr/bin/env python3
import os
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def update_lesson_video_urls(target_url="https://www.youtube.com/watch?v=kFYgLjdSkXE"):
    """
    Update the videoUrl of all lessons in Firebase to point to the specified YouTube URL.
    This script will also log all updates for reference.
    """
    
    print(f"Starting to update all lesson videoUrl fields to: {target_url}")
    
    # Check for Firebase credential file
    credential_file = 'firebase_config.json'
    if not os.path.exists(credential_file):
        # Try the admin SDK credential file if the config doesn't exist
        credential_file = 'englishlearningapp-30b00-firebase-adminsdk-fbsvc-3c16f54503.json'
        if not os.path.exists(credential_file):
            # Try to find any admin SDK file
            admin_sdk_files = [f for f in os.listdir('.') if f.endswith('firebase-adminsdk') or f.endswith('.json')]
            if admin_sdk_files:
                credential_file = admin_sdk_files[0]
                print(f"Using found credential file: {credential_file}")
            else:
                print("Error: No Firebase credential file found. Please ensure you have either:")
                print("- firebase_config.json")
                print("- A Firebase Admin SDK JSON file")
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
    with open(log_file, 'w') as f:
        f.write(f"Video URL Update Log - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Target URL: {target_url}\n\n")
    
    # Fetch all courses
    try:
        courses_ref = db.collection('Courses')
        courses = courses_ref.stream()
        
        total_courses = 0
        total_lessons = 0
        updated_lessons = 0
        
        # Loop through all courses
        for course in courses:
            total_courses += 1
            course_id = course.id
            print(f"Processing course: {course_id}")
            
            # Log to file
            with open(log_file, 'a') as f:
                f.write(f"Course: {course_id}\n")
            
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
                    with open(log_file, 'a') as f:
                        f.write(f"  - Lesson: {lesson_id}\n")
                        f.write(f"    Old URL: {old_url}\n")
                        f.write(f"    New URL: {target_url}\n")
                    
                    time.sleep(0.1)  # Small delay to avoid hitting quota limits
                elif 'videoUrl' not in lesson_data:
                    print(f"  Adding videoUrl to lesson: {lesson_id}")
                    lessons_ref.document(lesson_id).update({'videoUrl': target_url})
                    updated_lessons += 1
                    
                    # Log to file
                    with open(log_file, 'a') as f:
                        f.write(f"  - Lesson: {lesson_id}\n")
                        f.write(f"    Added URL: {target_url}\n")
                    
                    time.sleep(0.1)  # Small delay to avoid hitting quota limits
                else:
                    print(f"  Lesson already has the target URL: {lesson_id}")
        
        print(f"\nUpdate complete!")
        print(f"Total courses processed: {total_courses}")
        print(f"Total lessons found: {total_lessons}")
        print(f"Lessons updated: {updated_lessons}")
        print(f"Log file created: {log_file}")
        
        # Log final statistics
        with open(log_file, 'a') as f:
            f.write(f"\nSummary:\n")
            f.write(f"Total courses processed: {total_courses}\n")
            f.write(f"Total lessons found: {total_lessons}\n")
            f.write(f"Lessons updated: {updated_lessons}\n")
        
    except Exception as e:
        print(f"Error updating lesson video URLs: {e}")
        # Log error to file
        with open(log_file, 'a') as f:
            f.write(f"\nERROR: {e}\n")

if __name__ == "__main__":
    update_lesson_video_urls(target_url="https://www.youtube.com/watch?v=kFYgLjdSkXE") 