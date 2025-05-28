# Fix for Firestore Permission Issues in English Learning App

This project contains fixes for the "PERMISSION_DENIED: Missing or insufficient permissions" errors in the English Learning App when trying to access vocabulary data.

## Root Cause

The error occurs due to two main issues:
1. Firestore security rules not properly configured to allow access to vocabulary data
2. Missing fields in the Lesson model class causing deserialization errors

## Implemented Fixes

1. **Updated Lesson Model**
   - Added missing fields (vocabulary_count, isLocked, category, introduction)
   - Fixed Firestore serialization/deserialization

2. **Improved Error Handling**
   - Added proper fallback to sample vocabulary data when Firebase access fails
   - Implemented better error messaging in log outputs

3. **Added Required Resources**
   - Created vector drawable for audio playback in vocabulary list
   - Added missing item layout for vocabulary list items

4. **Firestore Setup Guide**
   - Created `FIRESTORE_SETUP.md` with detailed instructions
   - Added security rules in `firestore.rules` file
   - Created a Python script for adding sample vocabulary data

## How to Fix

1. Update your Firestore security rules using the provided `firestore.rules` file
2. Follow the setup instructions in `FIRESTORE_SETUP.md`
3. Run the Python script in `train model python/add_vocabulary_data.py` to add sample vocabulary data

If you continue to experience issues, the app is now designed to gracefully fall back to sample data, so it will still function without Firestore access.

## Sample Data

The app now includes sample TOEIC vocabulary in these categories:
- Marketing Terminology
- Human Resources
- Business Communication

## Testing

To verify the fix:
1. Run the app and navigate to a course
2. Open a vocabulary lesson
3. Confirm vocabulary items display correctly
4. Test audio playback and word selection features

If Firestore access is successful, you'll see data from the database. If not, sample vocabulary data will be displayed automatically. 