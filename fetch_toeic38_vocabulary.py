import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os
import sys

def initialize_firebase():
    """Initialize Firebase connection"""
    try:
        # Check if already initialized
        try:
            app = firebase_admin.get_app()
        except ValueError:
            # Try different locations for the Firebase config file
            config_paths = [
                'firebase_config.json',
                'scripts/firebase_config.json',
                os.path.join(os.path.dirname(__file__), 'firebase_config.json')
            ]
            
            config_path = None
            for path in config_paths:
                if os.path.exists(path):
                    config_path = path
                    break
                    
            if not config_path:
                print("Error: Firebase configuration file not found.")
                print("Please place firebase_config.json in the current directory or scripts/ folder.")
                sys.exit(1)
                
            cred = credentials.Certificate(config_path)
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        return db
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        sys.exit(1)

def fetch_toeic38_course_data(db):
    """Fetches the course data for TOEIC38"""
    try:
        course_doc = db.collection('Courses').document('toeic38').get()
        if not course_doc.exists:
            print("Error: TOEIC38 course not found in Firebase.")
            return None
            
        course_data = course_doc.to_dict()
        print(f"Course: {course_data.get('title', 'TOEIC38')}")
        return course_data
    except Exception as e:
        print(f"Error fetching course data: {e}")
        return None

def fetch_toeic38_lessons(db):
    """Fetches all lessons for TOEIC38 course"""
    try:
        lessons_ref = db.collection('Courses').document('toeic38').collection('Lessons')
        lessons = lessons_ref.get()
        
        lesson_list = []
        for lesson in lessons:
            lesson_data = lesson.to_dict()
            lesson_data['id'] = lesson.id
            lesson_list.append(lesson_data)
            
        # Sort lessons by lesson number
        lesson_list.sort(key=lambda x: x.get('lessonNumber', 0))
        
        print(f"Found {len(lesson_list)} lessons for TOEIC38 course")
        return lesson_list
    except Exception as e:
        print(f"Error fetching lessons: {e}")
        return []

def fetch_vocabulary_for_lesson(db, lesson_id):
    """Fetches vocabulary items for a specific lesson"""
    try:
        # Path 1: Courses/toeic38/Lessons/{lessonId}/Vocabulary
        vocabulary_ref = db.collection('Courses').document('toeic38').collection('Lessons').document(lesson_id).collection('Vocabulary')
        vocabulary_docs = vocabulary_ref.get()
        
        vocabulary_items = []
        for doc in vocabulary_docs:
            vocab_item = doc.to_dict()
            vocabulary_items.append(vocab_item)
            
        if vocabulary_items:
            print(f"Found {len(vocabulary_items)} vocabulary items for lesson {lesson_id} from Courses collection")
            return vocabulary_items
            
        # Path 2: Try the Lessons collection directly if no results from Courses
        vocabulary_ref = db.collection('Lessons').document(lesson_id).collection('Vocabulary')
        vocabulary_docs = vocabulary_ref.get()
        
        vocabulary_items = []
        for doc in vocabulary_docs:
            vocab_item = doc.to_dict()
            vocabulary_items.append(vocab_item)
            
        print(f"Found {len(vocabulary_items)} vocabulary items for lesson {lesson_id} from Lessons collection")
        return vocabulary_items
    except Exception as e:
        print(f"Error fetching vocabulary for lesson {lesson_id}: {e}")
        return []

def load_company_structures_vocabulary():
    """Load vocabulary related to company structures from a local JSON file if available"""
    vocab_files = ['vocabulary_data.json', 'lessons_with_vocabulary.json']
    
    all_vocabulary = []
    for file_path in vocab_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Extract vocabulary items for toeic38
                if isinstance(data, list):
                    # vocabulary_data.json format
                    for item in data:
                        if item.get('courseId') == 'toeic38':
                            all_vocabulary.append(item)
                            
                elif isinstance(data, dict) and 'toeic38' in data:
                    # lessons_with_vocabulary.json format
                    toeic38_data = data['toeic38']
                    if 'lessons' in toeic38_data:
                        for lesson_id, lesson_data in toeic38_data['lessons'].items():
                            if 'vocabulary' in lesson_data:
                                for vocab in lesson_data['vocabulary']:
                                    vocab['lessonId'] = lesson_id
                                    all_vocabulary.append(vocab)
                
                if all_vocabulary:
                    print(f"Loaded {len(all_vocabulary)} vocabulary items from {file_path}")
                    return all_vocabulary
                    
            except Exception as e:
                print(f"Error loading vocabulary from {file_path}: {e}")
    
    return all_vocabulary

def process_meeting_vocabulary():
    """Create a list of essential meeting vocabulary based on screenshots"""
    meeting_vocabulary = [
        {"english": "Schedule", "vietnamese": "Lịch trình", "phonetic": "/ˈʃɛdjuːl/"},
        {"english": "Agenda", "vietnamese": "Chương trình nghị sự", "phonetic": "/əˈdʒɛndə/"},
        {"english": "Conference Call", "vietnamese": "Cuộc gọi hội nghị", "phonetic": "/ˈkɒnfərəns kɔːl/"},
        {"english": "Minutes", "vietnamese": "Biên bản", "phonetic": "/ˈmɪnɪts/"},
        {"english": "Deadline", "vietnamese": "Hạn chót", "phonetic": "/ˈdɛdlaɪn/"},
        {"english": "Meeting Room", "vietnamese": "Phòng họp", "phonetic": "/ˈmiːtɪŋ ruːm/"},
        {"english": "Appointment", "vietnamese": "Cuộc hẹn", "phonetic": "/əˈpɔɪntmənt/"},
        {"english": "Reschedule", "vietnamese": "Sắp xếp lại lịch", "phonetic": "/riːˈʃɛdjuːl/"}
    ]
    return meeting_vocabulary

def main():
    print("Connecting to Firebase to fetch TOEIC38 vocabulary data...")
    
    # Try to initialize Firebase
    try:
        db = initialize_firebase()
    except Exception as e:
        print(f"Failed to connect to Firebase: {e}")
        # Fall back to local data if Firebase connection fails
        meeting_vocabulary = process_meeting_vocabulary()
        print("Using local meeting vocabulary data instead:")
        for item in meeting_vocabulary:
            print(f"{item['english']} - {item['vietnamese']} ({item['phonetic']})")
        return
    
    # Fetch course data
    course_data = fetch_toeic38_course_data(db)
    if not course_data:
        # Fall back to local data
        meeting_vocabulary = process_meeting_vocabulary()
        print("Using local meeting vocabulary data instead:")
        for item in meeting_vocabulary:
            print(f"{item['english']} - {item['vietnamese']} ({item['phonetic']})")
        return
    
    # Fetch lessons
    lessons = fetch_toeic38_lessons(db)
    if not lessons:
        print("No lessons found for TOEIC38 course.")
        # Try loading from local file
        vocabulary = load_company_structures_vocabulary()
        if vocabulary:
            print_vocabulary_by_lesson(vocabulary)
        else:
            meeting_vocabulary = process_meeting_vocabulary()
            print("Using local meeting vocabulary data instead:")
            for item in meeting_vocabulary:
                print(f"{item['english']} - {item['vietnamese']} ({item['phonetic']})")
        return
    
    # Fetch vocabulary for each lesson
    results = {}
    for lesson in lessons:
        lesson_id = lesson['id']
        lesson_title = lesson.get('title', f"Lesson {lesson.get('lessonNumber', '?')}")
        
        vocabulary = fetch_vocabulary_for_lesson(db, lesson_id)
        if vocabulary:
            results[lesson_id] = {
                'title': lesson_title,
                'vocabulary': vocabulary
            }
    
    if not results:
        print("No vocabulary data found in Firebase for TOEIC38 lessons.")
        # Try loading from local file
        vocabulary = load_company_structures_vocabulary()
        if vocabulary:
            print_vocabulary_by_lesson(vocabulary)
        else:
            meeting_vocabulary = process_meeting_vocabulary()
            print("\nUsing local meeting vocabulary data instead:")
            for item in meeting_vocabulary:
                print(f"{item['english']} - {item['vietnamese']} ({item['phonetic']})")
        return
    
    # Display vocabulary by lesson
    print("\n===== TOEIC38 Vocabulary by Lesson =====")
    for lesson_id, data in results.items():
        print(f"\n{data['title']} ({lesson_id}):")
        for item in data['vocabulary']:
            english = item.get('english', '')
            vietnamese = item.get('vietnamese', '')
            phonetic = item.get('phonetic', '')
            print(f"  {english} - {vietnamese} ({phonetic})")
    
    # Save vocabulary to JSON file
    output_file = "toeic38_vocabulary.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nVocabulary data saved to {output_file}")

def print_vocabulary_by_lesson(vocabulary_items):
    """Print vocabulary items grouped by lesson"""
    lessons = {}
    for item in vocabulary_items:
        lesson_id = item.get('lessonId', 'unknown')
        if lesson_id not in lessons:
            lessons[lesson_id] = []
        lessons[lesson_id].append(item)
    
    print("\n===== TOEIC38 Vocabulary by Lesson (from local data) =====")
    for lesson_id, items in lessons.items():
        print(f"\n{lesson_id}:")
        for item in items:
            english = item.get('english', '')
            vietnamese = item.get('vietnamese', '')
            phonetic = item.get('phonetic', '')
            print(f"  {english} - {vietnamese} ({phonetic})")

if __name__ == "__main__":
    main() 