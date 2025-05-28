# Fixing Firebase Permission Issues

## Problem Identified
The app is experiencing Firebase permission issues when trying to access the following collections and subcollections:
1. Direct access to `Lessons/toeic_lesson_39_10`
2. Access to subcollections: `Courses/toeic39/Lessons/toeic_lesson_39_10/Vocabulary`

Error shown in logs:
```
PERMISSION_DENIED: Missing or insufficient permissions
```

Additional issues identified in model mapping:
```
No setter/field for vocabulary_count found on class com.example.englishlearningapp.Models.Lesson
No setter/field for isLocked found on class com.example.englishlearningapp.Models.Lesson
No setter/field for category found on class com.example.englishlearningapp.Models.Lesson
No setter/field for introduction found on class com.example.englishlearningapp.Models.Lesson
```

## Solution 1: Update Firebase Security Rules

Replace the current Firebase security rules with:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /Users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Direct access to Lessons collection
    match /Lessons/{lessonId} {
      allow read, write: if true;
      
      // Access to Vocabulary subcollection within a lesson
      match /Vocabulary/{vocabularyId} {
        allow read, write: if true;
      }
      
      // Access to Subtitles subcollection within a lesson
      match /Subtitles/{subtitleId} {
        allow read, write: if true;
      }
    }
    
    match /Courses/{courseId} {
      allow read, write: if true; // Allow access to courses
      
      // Access to Lessons subcollection within a course
      match /Lessons/{lessonId} {
        allow read, write: if true;
        
        // Access to Vocabulary subcollection within a lesson that's in a course
        match /Vocabulary/{vocabularyId} {
          allow read, write: if true;
        }
        
        // Access to Subtitles subcollection within a lesson that's in a course
        match /Subtitles/{subtitleId} {
          allow read, write: if true;
        }
      }
      
      match /wordGame1/{documentId} {
        allow read: if true;
        allow write: if request.auth != null;
      }
    }
  }
}
```

## Solution 2: Update Lesson Model

Updated the Lesson model in `app/src/main/java/com/example/englishlearningapp/Models/Lesson.java` to include the missing fields:

- Added `vocabulary_count` field (int)
- Added `category` field (String)
- Added `introduction` field (String)

The existing `isLocked` field was already present but may have been camelCased differently between the app and Firebase.

## Implementation Steps

1. Copy the updated Firebase security rules to your Firebase console:
   - Go to Firebase Console > Your Project > Firestore Database > Rules
   - Replace the current rules with the new ones
   - Click "Publish"

2. Build and run the app again to verify that the permissions issues are resolved.

3. If the app continues to use the sample vocabulary data, check the Firebase database structure to make sure the paths match what the app is expecting:
   - Main lessons collection: `Lessons/{lessonId}`
   - Vocabulary subcollection: `Lessons/{lessonId}/Vocabulary`
   - Courses collection: `Courses/{courseId}`
   - Course lessons subcollection: `Courses/{courseId}/Lessons/{lessonId}`
   - Course lesson vocabulary: `Courses/{courseId}/Lessons/{lessonId}/Vocabulary`

## Note on Security

The current rules allow full read/write access to most collections. This is appropriate for development and testing but should be restricted for production use.

For a production environment, you should implement more restrictive rules that:
1. Require authentication for most operations
2. Limit write access to only authorized users
3. Implement proper data validation 