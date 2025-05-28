# Video URL Update Scripts

This directory contains scripts to update all video URLs in the Firebase database to point to a specific YouTube video.

## Available Scripts

### update_all_video_urls.py

This is the comprehensive script that will update video URLs in:
- All Lessons across all Courses
- All Questions in standalone collections
- All Questions nested inside Test models

### update_video_urls.py

This is a simpler script that only updates videoUrl fields in Lessons.

## How to Use

1. Make sure the Firebase Admin SDK is installed:
   ```
   pip install firebase-admin
   ```

2. Ensure your Firebase credentials are in one of these locations:
   - `firebase_config.json` in the current directory
   - `train model python/firebase_config.json`
   - `train model python/englishlearningapp-30b00-firebase-adminsdk-fbsvc-3c16f54503.json`

3. Run the script:
   ```
   python update_all_video_urls.py
   ```

4. Review the generated log file to see all changes that were made.

## Log Files

The scripts generate detailed log files with the naming pattern `video_url_updates_YYYYMMDD_HHMMSS.log` that contain:
- Which fields were updated
- Old and new URL values
- Summary statistics

## Customization

If you want to use a different video URL, you can modify the target URL in the script or customize the script by opening it in a text editor and changing the `target_url` parameter.

## Troubleshooting

- **Authentication Error**: Make sure your Firebase credentials are valid and have write access to the database
- **Rate Limiting**: The script includes delays to avoid hitting Firebase quota limits, but if you encounter rate limiting, you can increase the sleep time in the code
- **Missing Fields**: If some fields don't get updated, check if they're using a different field name or structure 