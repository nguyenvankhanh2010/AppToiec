# Firestore Setup for English Learning App

This guide will help you set up Firebase Firestore for the English Learning App with proper security rules and sample data.

## Setup Steps

1. **Create a Firebase Project**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Click "Add project" and follow the setup steps

2. **Add Android App to Firebase Project**
   - In Firebase Console, click on your project
   - Click "Android" icon to add an Android app
   - Enter package name: `com.example.englishlearningapp`
   - Download `google-services.json` and place it in the app directory

3. **Set Up Firestore Database**
   - In Firebase Console, go to "Firestore Database"
   - Click "Create database"
   - Start in production mode
   - Choose a location closest to your users

4. **Import Security Rules**
   - Go to "Rules" tab in Firestore
   - Copy and paste the contents of `firestore.rules` file
   - Click "Publish"

## Database Structure

The app expects the following Firestore structure:

```
/Courses/{courseId}
  - courseId: string
  - title: string
  - description: string
  - category: string
  - duration: string
  - favoriteCount: number

/Courses/{courseId}/Lessons/{lessonId}
  - lessonId: string
  - lessonNumber: number
  - title: string
  - duration: string
  - introduction: string
  - category: string
  - videoUrl: string
  - isLocked: boolean
  - vocabulary_count: number

/Courses/{courseId}/Lessons/{lessonId}/Vocabulary/{vocabId}
  - english: string
  - vietnamese: string
  - phonetic: string
```

## Sample Data Import

To import sample vocabulary data for testing, you can use the provided scripts in the `train model python` directory:

1. Navigate to `train model python` directory:
   ```
   cd "train model python"
   ```

2. Run the Firebase uploader script:
   ```
   python firebase_uploader.py
   ```

3. Follow the prompts to import the data

## Troubleshooting

If you encounter "PERMISSION_DENIED" errors:

1. Check that your security rules match the ones provided in `firestore.rules`
2. Ensure users are authenticated before accessing data
3. For testing, you can temporarily enable public read access with the rule:
   ```
   match /{document=**} {
     allow read: if true;
   }
   ```
   
**Important:** The app includes fallback sample data in case Firestore access fails.

## Custom Vocabulary Data

To add your own vocabulary:

1. Go to Firestore Console
2. Navigate to your lesson: `Courses/{courseId}/Lessons/{lessonId}`
3. Create a `Vocabulary` subcollection
4. Add documents with fields:
   - english: The English text
   - vietnamese: The Vietnamese translation
   - phonetic: The phonetic pronunciation (IPA format)

## Need Help?

Check the app's error logs for specific Firestore access errors. Common issues include:
- Security rules configuration
- Authentication not set up correctly
- Missing collections or documents

For more details, refer to the [Firebase Documentation](https://firebase.google.com/docs/firestore). 