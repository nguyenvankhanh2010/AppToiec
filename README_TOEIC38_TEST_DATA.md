# TOEIC38 Test Data Generator and Android Integration

This package contains scripts and utilities to generate TOEIC vocabulary test data and integrate it with the English Learning App.

## Overview

The system includes:

1. **Test Data Generation** - Python script to create test questions from vocabulary data
2. **Firebase Integration** - Upload test data to Firebase for use in the Android app
3. **Android Adapters** - Java utility classes to fetch test data from Firebase or local assets
4. **Exam Activity Integration** - Instructions for integrating with the ExamActivity

## Files

- `generate_toeic38_test_data.py` - Python script to generate test data from vocabulary
- `toeic38_test_data.json` - Generated test data with questions for listening, reading, writing, and speaking
- `toeic38_firebase_test_adapter.java` - Java adapter for Firebase integration
- `toeic38_test_json_loader.java` - Java utility to load test data from JSON assets

## How To Use

### Generating Test Data

1. Make sure the `toeic38_vocabulary.json` file is available in the project root
2. Run the Python script:
   ```
   python generate_toeic38_test_data.py
   ```
3. The script will:
   - Load vocabulary data from `toeic38_vocabulary.json`
   - Generate test questions for listening, reading, writing, and speaking
   - Save data to `toeic38_test_data.json`
   - Upload data to Firebase (if Firebase is configured)

### Android Integration

#### Option 1: Using Firebase

1. Copy `toeic38_firebase_test_adapter.java` to your Android project's Utils package
2. In your activity, create an instance of the adapter and call startTest:

```java
// In your activity
import com.example.englishlearningapp.Utils.TOEIC38TestAdapter;

// Inside a method
TOEIC38TestAdapter testAdapter = new TOEIC38TestAdapter(this);

// Start different types of tests
testAdapter.startTest("listening"); // For listening test
testAdapter.startTest("reading");   // For reading test
testAdapter.startTest("writing");   // For writing test
testAdapter.startTest("speaking");  // For speaking test
```

#### Option 2: Using Local JSON

1. Copy `toeic38_test_data.json` to your Android project's assets folder
2. Copy `toeic38_test_json_loader.java` to your Android project's Utils package
3. In your activity, create an instance of the loader and call startTest:

```java
// In your activity
import com.example.englishlearningapp.Utils.TOEIC38TestJSONLoader;

// Inside a method
TOEIC38TestJSONLoader jsonLoader = new TOEIC38TestJSONLoader(this);

// Start different types of tests
jsonLoader.startTest("listening"); // For listening test
jsonLoader.startTest("reading");   // For reading test
jsonLoader.startTest("writing");   // For writing test
jsonLoader.startTest("speaking");  // For speaking test
```

## Test Data Structure

The test data is organized into four parts:

1. **part_1: Listening Practice** - Listen to English words and select correct Vietnamese meanings
2. **part_2: Reading Practice** - Read Vietnamese words and select correct English translations
3. **part_3: Writing Practice** - Complete sentences with appropriate vocabulary words
4. **part_4: Speaking Practice** - Practice pronunciation with example sentences

Each question includes:
- Question text
- Answer options
- Correct answer index
- Word being tested
- Phonetic representation
- Explanation text
- Audio URL (if applicable)
- Example text (if applicable)

## Adapting ExamActivity

The ExamActivity should already handle different question types based on the "testType" parameter. Here are some tips for ensuring compatibility:

1. Make sure ExamActivity can handle questions with the format used in the test data
2. Verify that the ExamActivity correctly displays phonetic text for reading questions
3. For speaking questions, ensure the activity can play back audio and record responses
4. For writing questions, check that example sentences are displayed correctly

### Usage Example

```java
// Example of a button click to start a test
Button listeningTestButton = findViewById(R.id.listening_test_button);
listeningTestButton.setOnClickListener(v -> {
    // Choose one of the methods below:
    
    // Method 1: Use Firebase adapter
    TOEIC38TestAdapter testAdapter = new TOEIC38TestAdapter(this);
    testAdapter.startTest("listening");
    
    // Method 2: Use local JSON loader
    // TOEIC38TestJSONLoader jsonLoader = new TOEIC38TestJSONLoader(this);
    // jsonLoader.startTest("listening");
});
```

## Troubleshooting

- If Firebase connection fails, the test data is still saved locally as `toeic38_test_data.json`
- If you encounter issues with the Firebase adapter, try using the JSON loader as a fallback
- Make sure the ExamActivity is properly registered in your AndroidManifest.xml 