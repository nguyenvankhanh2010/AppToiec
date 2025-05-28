import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
import re
import random
from datetime import datetime

# Initialize Firebase
def initialize_firebase():
    cred = credentials.Certificate("scripts/firebase_config.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

# Parse TOEIC dataset
def parse_toeic_dataset(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split content by topics
    topics = re.split(r'TOPIC \d+: |TOEIC \d+: ', content)[1:]
    topic_names = re.findall(r'(TOPIC \d+: |TOEIC \d+: )([^\n]+)', content)
    topic_names = [name[1].strip() for name in topic_names]
    
    topic_data = []
    for i, topic in enumerate(topics):
        # Extract vocabulary items
        vocab_items = []
        lines = topic.strip().split('\n')
        
        j = 0
        while j < len(lines):
            line = lines[j].strip()
            if not line:
                j += 1
                continue
            
            # Check if this line contains a vocabulary word
            if re.match(r'^[a-zA-Z]', line) and "=" not in line and ":" not in line:
                word = line.strip()
                
                # Skip empty lines
                while j+1 < len(lines) and not lines[j+1].strip():
                    j += 1
                
                # Next line should be part of speech or meaning
                j += 1
                meaning = ""
                example = ""
                
                # Collect meaning and examples
                while j < len(lines) and (not re.match(r'^[a-zA-Z]', lines[j].strip()) or "=" in lines[j] or ":" in lines[j] or lines[j].strip() == ""):
                    if lines[j].strip():
                        if "(v)" in lines[j] or "(n)" in lines[j] or "(adj)" in lines[j]:
                            meaning = lines[j].strip()
                        elif "Ex:" in lines[j]:
                            example = lines[j].replace("Ex:", "").strip()
                        elif example == "" and "(" not in lines[j] and meaning != "":
                            example = lines[j].strip()
                    j += 1
                    if j < len(lines) and re.match(r'^[a-zA-Z]', lines[j].strip()) and "=" not in lines[j] and ":" not in lines[j]:
                        break
                
                # Add vocabulary item
                if word and meaning:
                    vocab_items.append({
                        "english": word,
                        "vietnamese": meaning,
                        "example": example
                    })
                
                j -= 1  # Go back one line to not skip the next word
            j += 1
        
        topic_data.append({
            "name": topic_names[i] if i < len(topic_names) else f"TOEIC Topic {i+1}",
            "vocabulary": vocab_items
        })
    
    return topic_data

# Create lessons from vocabulary (5 words per lesson)
def create_lessons(topic_data):
    all_courses = []
    
    for topic_idx, topic in enumerate(topic_data):
        course_id = f"toeic{topic_idx+1}"
        course_name = topic['name']
        
        # Create lessons (5 words per lesson)
        lessons = []
        vocab = topic['vocabulary']
        
        for i in range(0, len(vocab), 5):
            lesson_vocab = vocab[i:i+5]
            lesson_number = i // 5 + 1
            
            lesson = {
                "lessonId": f"{course_id}_lesson_{lesson_number}",
                "lessonNumber": lesson_number,
                "title": f"{course_name} - Lesson {lesson_number}",
                "description": f"Learn 5 essential TOEIC vocabulary words for {course_name}",
                "duration": "15:00",
                "isLocked": False,
                "courseId": course_id,
                "videoUrl": f"https://www.youtube.com/watch?v=example{topic_idx+1}_{lesson_number}",
                "vocabulary": lesson_vocab,
                "vocabulary_count": len(lesson_vocab)
            }
            
            lessons.append(lesson)
        
        # Create course
        course = {
            "courseId": course_id,
            "title": f"TOEIC {topic_idx+1}: {course_name}",
            "description": f"Master essential vocabulary for {course_name} in this comprehensive TOEIC course.",
            "category": "TOEIC Vocabulary",
            "imageUrl": f"https://example.com/images/toeic_{topic_idx+1}.jpg",
            "duration": f"{len(lessons) * 15} minutes",
            "instructor": "Amanda Peterson",
            "language": "English",
            "level": "Beginner to Intermediate",
            "lastUpdated": datetime.now().strftime("%B %Y"),
            "favoriteCount": random.randint(200, 500),
            "lessons": lessons
        }
        
        all_courses.append(course)
    
    return all_courses

# Create test questions for vocabulary
def create_test_questions(courses):
    all_tests = []
    
    for course in courses:
        course_id = course["courseId"]
        test_id = f"{course_id}_test"
        
        listening_questions = []
        reading_questions = []
        speaking_questions = []
        writing_questions = []
        
        # Collect all vocabulary from all lessons
        all_vocab = []
        for lesson in course["lessons"]:
            all_vocab.extend(lesson["vocabulary"])
        
        # Create listening questions
        for vocab in all_vocab:
            english_word = vocab["english"]
            vietnamese_meaning = vocab["vietnamese"]
            
            # Multiple choice listening question
            options = [vocab["vietnamese"]]
            # Add wrong options from other vocabulary
            wrong_options = [v["vietnamese"] for v in all_vocab if v != vocab]
            random.shuffle(wrong_options)
            options.extend(wrong_options[:3])
            random.shuffle(options)
            
            question = {
                "questionId": f"listening_{english_word.replace(' ', '_')}",
                "questionText": f"Listen and choose the correct meaning for: {english_word}",
                "audioUrl": f"https://example.com/audio/{english_word.replace(' ', '_')}.mp3",
                "options": options,
                "correctAnswer": vietnamese_meaning,
                "explanation": f"The word '{english_word}' means '{vietnamese_meaning}' in Vietnamese."
            }
            
            listening_questions.append(question)
        
        # Create reading questions
        for vocab in all_vocab:
            english_word = vocab["english"]
            vietnamese_meaning = vocab["vietnamese"]
            example = vocab["example"] if vocab["example"] else f"This is an example with the word {english_word}."
            
            blank_example = example.replace(english_word, "_____")
            
            # Fill in the blank
            options = [english_word]
            wrong_options = [v["english"] for v in all_vocab if v != vocab]
            random.shuffle(wrong_options)
            options.extend(wrong_options[:3])
            random.shuffle(options)
            
            question = {
                "questionId": f"reading_{english_word.replace(' ', '_')}",
                "questionText": f"Choose the correct word to complete the sentence: {blank_example}",
                "options": options,
                "correctAnswer": english_word,
                "explanation": f"The correct word is '{english_word}', which means '{vietnamese_meaning}' in Vietnamese."
            }
            
            reading_questions.append(question)
        
        # Create speaking questions
        for vocab in all_vocab:
            english_word = vocab["english"]
            
            question = {
                "questionId": f"speaking_{english_word.replace(' ', '_')}",
                "questionText": f"Pronounce the word: {english_word}",
                "wordToSpeak": english_word,
                "audioUrlReference": f"https://example.com/audio/{english_word.replace(' ', '_')}_reference.mp3",
                "explanation": f"Practice pronouncing '{english_word}' correctly."
            }
            
            speaking_questions.append(question)
        
        # Create writing questions
        for vocab in all_vocab:
            english_word = vocab["english"]
            vietnamese_meaning = vocab["vietnamese"]
            
            question = {
                "questionId": f"writing_{english_word.replace(' ', '_')}",
                "questionText": f"Write the English word for: {vietnamese_meaning}",
                "correctAnswer": english_word,
                "explanation": f"The English word for '{vietnamese_meaning}' is '{english_word}'."
            }
            
            writing_questions.append(question)
        
        # Create complete test
        test = {
            "testId": test_id,
            "courseId": course_id,
            "title": f"Test for {course['title']}",
            "description": f"Comprehensive test covering vocabulary from {course['title']}",
            "duration": "30:00",
            "passScore": 70,
            "questions": {
                "listening": listening_questions,
                "reading": reading_questions,
                "speaking": speaking_questions,
                "writing": writing_questions
            }
        }
        
        all_tests.append(test)
    
    return all_tests

# Upload courses and tests to Firebase
def upload_to_firebase(db, courses, tests):
    # Upload courses
    for course in courses:
        course_ref = db.collection("Courses").document(course["courseId"])
        
        # Create a copy of course without lessons for the main document
        course_data = course.copy()
        lessons = course_data.pop("lessons")
        
        # Upload course document
        course_ref.set(course_data)
        print(f"Uploaded course: {course['courseId']}")
        
        # Upload lessons as subcollection
        for lesson in lessons:
            lesson_data = lesson.copy()
            vocabulary = lesson_data.pop("vocabulary")
            
            # Upload lesson document
            lesson_ref = course_ref.collection("Lessons").document(lesson["lessonId"])
            lesson_ref.set(lesson_data)
            print(f"Uploaded lesson: {lesson['lessonId']}")
            
            # Store vocabulary in the lesson document field instead of subcollection
            # This avoids the need for a subcollection inside another subcollection
            vocab_field = []
            for vocab in vocabulary:
                vocab_id = f"{vocab['english'].replace(' ', '_')}"
                vocab_item = vocab.copy()
                vocab_item["id"] = vocab_id
                vocab_field.append(vocab_item)
            
            # Update the lesson document with vocabulary array
            lesson_ref.update({
                "vocabularyItems": vocab_field
            })
            print(f"Added {len(vocabulary)} vocabulary items to lesson: {lesson['lessonId']}")
    
    # Upload tests
    for test in tests:
        test_ref = db.collection("Tests").document(test["testId"])
        
        # Store questions directly in the test document
        test_ref.set(test)
        print(f"Uploaded test: {test['testId']}")

def main():
    # Path to the dataset file
    dataset_file = "c:\\Users\\ADMIN\\Downloads\\dataset for english app.txt"
    
    # Check if file exists
    if not os.path.isfile(dataset_file):
        print(f"Dataset file not found: {dataset_file}")
        return
    
    print("Initializing Firebase...")
    db = initialize_firebase()
    
    print("Parsing TOEIC dataset...")
    topic_data = parse_toeic_dataset(dataset_file)
    print(f"Found {len(topic_data)} topics with vocabulary")
    
    print("Creating courses and lessons...")
    courses = create_lessons(topic_data)
    print(f"Created {len(courses)} courses")
    
    print("Creating test questions...")
    tests = create_test_questions(courses)
    print(f"Created {len(tests)} tests")
    
    print("Uploading to Firebase...")
    upload_to_firebase(db, courses, tests)
    
    print("Done!")

if __name__ == "__main__":
    main() 