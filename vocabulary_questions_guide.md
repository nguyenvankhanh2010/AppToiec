# Vocabulary Questions Generator Guide

This guide explains how to generate vocabulary-based questions from Firebase data and integrate them into the English Learning App.

## Overview

The system consists of two main components:

1. **Python Script for Question Generation**: Extracts vocabulary from Firebase, generates different types of questions, and uploads the questions back to Firebase.
2. **Android Integration**: Modified `ExamActivity.java` to load these questions and display them to users.

## Question Types

The system generates five types of questions:

1. **Listening Comprehension**: Users listen to audio and select the correct English phrase that matches a Vietnamese phrase.
2. **Reading Comprehension**: Users read an English phrase and select the correct Vietnamese translation.
3. **Writing Practice**: Users complete sentences by filling in blanks with appropriate words.
4. **Speaking Practice**: Users select the correct pronunciation for English phrases.
5. **Roleplay Scenarios**: Users select appropriate responses for conversation scenarios.

## How to Generate Questions

### Method 1: Using the Full Firebase Script

1. Make sure Firebase Admin SDK is installed:
   ```bash
   pip install firebase-admin
   ```

2. Run the generator script:
   ```bash
   python scripts/generate_vocab_questions.py
   ```

3. This will:
   - Connect to Firebase
   - Extract vocabulary from Courses > Lessons > Vocabulary collections
   - Generate questions for each vocabulary item
   - Upload the questions back to Firebase under a 'Tests' collection

### Method 2: Using the Mock Data Script

For testing or demonstration purposes, you can use the mock data script:

```bash
python scripts/generate_mock_questions.py
```

This will generate example questions based on predefined vocabulary and save them to a local file called `mock_test_questions.json`.

## Firebase Data Structure

The generated questions are stored in Firebase with the following structure:

```
Tests/
  ├── {courseId}_test/
  │     ├── courseId: String
  │     ├── nameTest: String
  │     ├── description: String
  │     ├── testType: "vocabulary"
  │     ├── parts: Array<Object>
  │     │
  │     └── Parts/
  │           ├── part_1/  # Listening
  │           │    ├── partNumber: 1
  │           │    ├── partName: "Listening Comprehension"
  │           │    ├── questionCount: Number
  │           │    │
  │           │    └── Questions/
  │           │          ├── question_1/
  │           │          │    ├── questionText: String
  │           │          │    ├── options: Array<String>
  │           │          │    └── correctAnswer: Number
  │           │          ├── question_2/
  │           │          └── ...
  │           │
  │           ├── part_2/  # Reading
  │           ├── part_3/  # Writing
  │           ├── part_4/  # Speaking
  │           └── part_5/  # Roleplay
  │
  └── ...
```

## Using Questions in the App

The modified `ExamActivity.java` can load questions in two ways:

1. **From TestModel** (legacy support): Loads questions from a TestModel object passed via Intent.
2. **From Firebase** (new): Loads questions directly from Firebase based on course ID and test type.

### Launching the Exam Activity with Firebase Questions

```java
Intent intent = new Intent(context, ExamActivity.class);
intent.putExtra("courseId", "toeic1");
intent.putExtra("testType", "listening"); // Options: listening, reading, writing, speaking, roleplay
startActivity(intent);
```

### How It Works

1. The app connects to Firebase and fetches the test document for the specified course.
2. It loads questions for the specified test type (corresponding to a specific part).
3. It randomly selects 5 questions from all available questions.
4. The questions are displayed to the user with radio button options.
5. After answering all questions, the user can submit the test for scoring.

## Customization

You can customize the number of questions per test by changing the `QUESTIONS_PER_TEST` constant in `ExamActivity.java`.

## Troubleshooting

If questions don't appear:
1. Check that the correct course ID is being used
2. Verify that questions were successfully uploaded to Firebase
3. Check the Firebase security rules to ensure read access to the Tests collection
4. Look for error messages in the app logs

## Next Steps

- Implement actual audio playback for listening questions
- Add more complex question types with images or video
- Create a practice mode with hints and explanations 