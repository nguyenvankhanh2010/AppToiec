import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os
import random
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

def load_vocabulary_data():
    """Load vocabulary data from toeic38_vocabulary.json"""
    try:
        with open('toeic38_vocabulary.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Loaded vocabulary data with {len(data)} lessons")
        return data
    except Exception as e:
        print(f"Error loading vocabulary data: {e}")
        sys.exit(1)

def create_listening_questions(vocabulary_data):
    """Create listening test questions based on vocabulary"""
    listening_questions = []
    all_vocab = []
    
    # Extract all vocabulary items
    for lesson_id, lesson_data in vocabulary_data.items():
        for vocab in lesson_data['vocabulary']:
            all_vocab.append(vocab)
    
    # Shuffle to randomize questions
    random.shuffle(all_vocab)
    
    # Create listening questions (listen to audio, select the correct English word)
    for i, vocab in enumerate(all_vocab[:10]):  # Create 10 questions
        english_word = vocab['english']
        vietnamese = vocab['vietnamese']
        phonetic = vocab.get('phonetic', '')
        
        # Create wrong options by selecting random English words
        wrong_options = []
        while len(wrong_options) < 3:
            random_vocab = random.choice(all_vocab)
            if random_vocab['english'] != english_word and random_vocab['english'] not in wrong_options:
                wrong_options.append(random_vocab['english'])
        
        # Combine correct and wrong options
        options = [english_word] + wrong_options
        random.shuffle(options)
        
        # Find index of correct answer in shuffled options
        correct_answer = options.index(english_word)
        
        question = {
            'questionText': "Bạn nghe từ. Chọn từ tiếng Anh đúng với từ bạn vừa nghe.",
            'options': options,
            'correctAnswer': correct_answer,
            'audioUrl': '',  # In a real app, this would be a URL to audio file
            'explanation': f"Từ bạn nghe là '{english_word}' ({phonetic}) có nghĩa là '{vietnamese}'.",
            'word': english_word,
            'phoneticText': phonetic,
            'questionType': 'listening'
        }
        listening_questions.append(question)
    
    return listening_questions

def create_reading_questions(vocabulary_data):
    """Create reading test questions based on vocabulary"""
    reading_questions = []
    all_vocab = []
    
    # Extract all vocabulary items
    for lesson_id, lesson_data in vocabulary_data.items():
        for vocab in lesson_data['vocabulary']:
            all_vocab.append(vocab)
    
    # Shuffle to randomize questions
    random.shuffle(all_vocab)
    
    # Create reading questions (show English word, select Vietnamese meaning)
    for i, vocab in enumerate(all_vocab[:10]):  # Create 10 questions
        english_word = vocab['english']
        correct_vietnamese = vocab['vietnamese']
        phonetic = vocab.get('phonetic', '')
        
        # Create wrong options by selecting random Vietnamese translations
        wrong_options = []
        while len(wrong_options) < 3:
            random_vocab = random.choice(all_vocab)
            if random_vocab['vietnamese'] != correct_vietnamese and random_vocab['vietnamese'] not in wrong_options:
                wrong_options.append(random_vocab['vietnamese'])
        
        # Combine and shuffle options
        options = [correct_vietnamese] + wrong_options
        random.shuffle(options)
        
        # Find index of correct answer
        correct_answer = options.index(correct_vietnamese)
        
        question = {
            'questionText': f"Đâu là nghĩa của '{english_word}' ({phonetic})?",
            'options': options,
            'correctAnswer': correct_answer,
            'explanation': f"'{english_word}' ({phonetic}) có nghĩa là '{correct_vietnamese}'.",
            'word': english_word,
            'phoneticText': phonetic,
            'questionType': 'reading'
        }
        reading_questions.append(question)
    
    return reading_questions

def create_speaking_questions(vocabulary_data):
    """Create speaking test questions based on vocabulary"""
    speaking_questions = []
    all_vocab = []
    
    # Extract all vocabulary items
    for lesson_id, lesson_data in vocabulary_data.items():
        for vocab in lesson_data['vocabulary']:
            all_vocab.append(vocab)
    
    # Shuffle to randomize questions
    random.shuffle(all_vocab)
    
    # Speaking questions (repeat pronunciation and use in a sentence)
    for i, vocab in enumerate(all_vocab[:10]):  # Create 10 questions
        english_word = vocab['english']
        vietnamese = vocab['vietnamese']
        phonetic = vocab.get('phonetic', '')
        
        # Create example sentences for the words
        business_contexts = [
            f"Please {english_word.lower()} the meeting for tomorrow.",
            f"We need to {english_word.lower()} our strategy before the deadline.",
            f"The {english_word.lower()} will be held in the main conference room.",
            f"Can you {english_word.lower()} this information to the team?",
            f"Our company {english_word.lower()} requires approval from management."
        ]
        
        example_sentence = random.choice(business_contexts)
        
        # For speaking, we provide conversation responses as options
        options = [
            f"I can pronounce '{english_word}' correctly.",
            f"I need more practice with this word.",
            f"Let me try again with '{english_word}'.",
            f"I understand how to use '{english_word}' in a sentence."
        ]
        
        question = {
            'questionText': f"Hãy phát âm từ '{english_word}' ({phonetic}) và sử dụng nó trong câu sau: '{example_sentence}'",
            'options': options,
            'correctAnswer': 0,  # First option is always correct for speaking practice
            'audioUrl': '',  # In a real app, this would be a URL to audio file
            'explanation': f"'{english_word}' ({phonetic}) có nghĩa là '{vietnamese}'.",
            'word': english_word,
            'phoneticText': phonetic,
            'exampleText': example_sentence,
            'questionType': 'speaking'
        }
        speaking_questions.append(question)
    
    return speaking_questions

def create_writing_questions(vocabulary_data):
    """Create writing test questions based on vocabulary"""
    writing_questions = []
    all_vocab = []
    
    # Extract all vocabulary items
    for lesson_id, lesson_data in vocabulary_data.items():
        for vocab in lesson_data['vocabulary']:
            all_vocab.append(vocab)
    
    # Shuffle to randomize questions
    random.shuffle(all_vocab)
    
    # Writing questions (complete sentences using vocabulary)
    for i, vocab in enumerate(all_vocab[:10]):  # Create 10 questions
        english_word = vocab['english']
        vietnamese = vocab['vietnamese']
        phonetic = vocab.get('phonetic', '')
        
        # Create sentence templates with blanks
        sentence_templates = [
            f"We need to _____ a meeting with the clients next week.",
            f"Please _____ the document before sending it to the manager.",
            f"The team will _____ the new project next month.",
            f"Can you _____ this information in your report?",
            f"Our company needs to _____ new employees for the project."
        ]
        
        sentence = random.choice(sentence_templates)
        
        # For writing, options are possible words to complete the sentence
        options = [english_word]
        while len(options) < 4:
            random_vocab = random.choice(all_vocab)
            if random_vocab['english'] != english_word and random_vocab['english'] not in options:
                options.append(random_vocab['english'])
        
        random.shuffle(options)
        correct_answer = options.index(english_word)
        
        question = {
            'questionText': f"Hoàn thành câu sau bằng từ vựng phù hợp: '{sentence}'",
            'options': options,
            'correctAnswer': correct_answer,
            'explanation': f"Từ '{english_word}' ({phonetic}) có nghĩa là '{vietnamese}' và phù hợp để điền vào chỗ trống.",
            'word': english_word,
            'phoneticText': phonetic,
            'exampleText': sentence.replace("_____", english_word),
            'questionType': 'writing'
        }
        writing_questions.append(question)
    
    return writing_questions

def create_test_data(vocabulary_data):
    """Create test data structure with all question types"""
    test_data = {
        'nameTest': 'TOEIC38 Vocabulary Practice Test',
        'description': 'Luyện tập từ vựng TOEIC về Business Meetings',
        'parts': {
            'part_1': {
                'title': 'Listening Practice',
                'description': 'Listen to the word and select the correct meaning',
                'questions': create_listening_questions(vocabulary_data)
            },
            'part_2': {
                'title': 'Reading Practice',
                'description': 'Read and understand the vocabulary meaning',
                'questions': create_reading_questions(vocabulary_data)
            },
            'part_3': {
                'title': 'Writing Practice',
                'description': 'Complete sentences with appropriate vocabulary',
                'questions': create_writing_questions(vocabulary_data)
            },
            'part_4': {
                'title': 'Speaking Practice',
                'description': 'Practice pronunciation and using vocabulary in context',
                'questions': create_speaking_questions(vocabulary_data)
            }
        }
    }
    return test_data

def upload_test_data_to_firebase(db, test_data):
    """Upload test data to Firebase"""
    try:
        # Create test document reference
        test_ref = db.collection('Tests').document('toeic38_test')
        
        # Upload main test data (excluding parts)
        test_info = {
            'nameTest': test_data['nameTest'],
            'description': test_data['description'],
            'courseId': 'toeic38'
        }
        test_ref.set(test_info)
        
        # Upload each part separately
        for part_id, part_data in test_data['parts'].items():
            part_ref = test_ref.collection('Parts').document(part_id)
            
            # Add part info without questions
            part_info = {
                'title': part_data['title'],
                'description': part_data['description']
            }
            part_ref.set(part_info)
            
            # Add questions as subcollection
            for i, question in enumerate(part_data['questions']):
                question_ref = part_ref.collection('Questions').document(f'question_{i+1}')
                question_ref.set(question)
        
        print(f"Successfully uploaded test data to Firebase")
        return True
    except Exception as e:
        print(f"Error uploading test data to Firebase: {e}")
        return False

def save_test_data_locally(test_data):
    """Save test data to a local JSON file"""
    try:
        with open('toeic38_test_data.json', 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        print("Test data saved to toeic38_test_data.json")
        return True
    except Exception as e:
        print(f"Error saving test data locally: {e}")
        return False

def main():
    print("Generating test data for TOEIC38 vocabulary...")
    
    # Load vocabulary data
    vocabulary_data = load_vocabulary_data()
    
    # Create test data structure
    test_data = create_test_data(vocabulary_data)
    
    # Save test data locally
    save_test_data_locally(test_data)
    
    # Try to initialize Firebase and upload data
    try:
        db = initialize_firebase()
        upload_test_data_to_firebase(db, test_data)
    except Exception as e:
        print(f"Failed to connect to Firebase: {e}")
        print("Test data was saved locally but not uploaded to Firebase.")
        return

if __name__ == "__main__":
    main() 