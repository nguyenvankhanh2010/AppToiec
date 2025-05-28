# YouTube Video Playback Integration Guide

This guide explains how to add YouTube video playback capabilities to the English Learning App.

## Option 1: WebView Approach (Current Implementation)

The app currently uses a WebView-based approach to play YouTube videos. Here's how it works:

1. The layout includes both a standard VideoView and a WebView in the video container:
   ```xml
   <FrameLayout
       android:id="@+id/video_container"
       android:layout_width="match_parent"
       android:layout_height="280dp"
       android:layout_alignParentTop="true"
       android:background="#000000">

       <VideoView
           android:id="@+id/video_view"
           android:layout_width="match_parent"
           android:layout_height="match_parent"
           android:layout_gravity="center" />
           
       <WebView
           android:id="@+id/youtube_web_view"
           android:layout_width="match_parent"
           android:layout_height="match_parent"
           android:layout_gravity="center"
           android:visibility="gone" />
   </FrameLayout>
   ```

2. The `loadVideo()` method in VideoPlayerActivity checks if the video URL is a YouTube URL:
   ```java
   if (videoUrl != null && !videoUrl.isEmpty() && videoUrl.contains("youtube.com")) {
       // Handle YouTube video with WebView
       // ...
   } else {
       // Handle standard video with VideoView
       // ...
   }
   ```

3. For YouTube videos, the app:
   - Shows the WebView and hides the VideoView
   - Configures the WebView for video playback
   - Extracts the YouTube video ID from the URL
   - Loads HTML with an embedded YouTube iframe

4. The code handles the YouTube video ID extraction:
   ```java
   if (videoUrl.contains("youtube.com/watch?v=")) {
       videoId = videoUrl.split("youtube.com/watch\\?v=")[1];
       if (videoId.contains("&")) {
           videoId = videoId.split("&")[0];
       }
   } else if (videoUrl.contains("youtu.be/")) {
       videoId = videoUrl.split("youtu.be/")[1];
       if (videoId.contains("?")) {
           videoId = videoId.split("\\?")[0];
       }
   }
   ```

5. The HTML iframe is created and loaded into the WebView:
   ```java
   String htmlContent = "<!DOCTYPE html>" +
           "<html>" +
           "<head>" +
           "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no\">" +
           "<style>" +
           "body { margin: 0; padding: 0; background-color: #000; }" +
           ".video-container { position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; }" +
           ".video-container iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }" +
           "</style>" +
           "</head>" +
           "<body>" +
           "<div class=\"video-container\">" +
           "<iframe width=\"100%\" height=\"100%\" src=\"https://www.youtube.com/embed/" + videoId + "?rel=0&autoplay=1&playsinline=1\" frameborder=\"0\" allowfullscreen></iframe>" +
           "</div>" +
           "</body>" +
           "</html>";
   
   youtubeWebView.loadData(htmlContent, "text/html", "UTF-8");
   ```

6. The lifecycle methods (`onPause()`, `onResume()`, `onDestroy()`) handle WebView states correctly.

### Limitations of the WebView Approach

- Limited control over video playback (cannot get position, duration, etc.)
- No direct access to YouTube player controls
- No easy way to detect when video finishes playing
- Limited ability to control playback quality

## Option 2: YouTube Android Player API (Recommended)

For better integration, you can use the official YouTube Android Player API:

1. First, add the dependency to your app's `build.gradle`:
   ```gradle
   dependencies {
       implementation 'com.google.apis:google-api-services-youtube:v3-rev222-1.25.0'
       implementation 'com.google.android.youtube:youtube-android-player-api:1.2.2'
   }
   ```

2. Get a YouTube API key from the Google Developer Console:
   - Go to https://console.developers.google.com/
   - Create a new project
   - Enable the YouTube Data API v3
   - Create credentials (API Key)

3. Update the layout to include a YouTubePlayerView:
   ```xml
   <com.google.android.youtube.player.YouTubePlayerView
       android:id="@+id/youtube_player_view"
       android:layout_width="match_parent"
       android:layout_height="match_parent"
       android:visibility="gone" />
   ```

4. Modify VideoPlayerActivity to implement YouTubePlayer.OnInitializedListener:
   ```java
   public class VideoPlayerActivity extends YouTubeBaseActivity implements YouTubePlayer.OnInitializedListener {
       private static final String API_KEY = "YOUR_API_KEY";
       private YouTubePlayerView youTubePlayerView;
       private YouTubePlayer youTubePlayer;
       
       // Rest of the code...
       
       @Override
       public void onInitializationSuccess(YouTubePlayer.Provider provider, YouTubePlayer player, boolean wasRestored) {
           youTubePlayer = player;
           if (!wasRestored) {
               player.loadVideo(videoId);
               player.setPlaybackEventListener(new PlaybackEventListener());
           }
       }
       
       @Override
       public void onInitializationFailure(YouTubePlayer.Provider provider, YouTubeInitializationResult result) {
           // Handle failure
       }
   }
   ```

5. Initialize the YouTube player in `loadVideo()`:
   ```java
   if (isYoutubeUrl(videoUrl)) {
       String videoId = extractYoutubeVideoId(videoUrl);
       if (videoId != null) {
           videoView.setVisibility(View.GONE);
           youTubePlayerView.setVisibility(View.VISIBLE);
           youTubePlayerView.initialize(API_KEY, this);
       }
   }
   ```

### Benefits of YouTube API Approach

- Better integration with the YouTube platform
- Access to player state changes (playing, paused, buffering, etc.)
- Ability to control playback (seek, pause, stop)
- Better handling of fullscreen mode
- Consistent YouTube player UI

## Troubleshooting

If you're encountering issues with YouTube video playback:

1. **Video doesn't play**: 
   - Check for valid YouTube URL format
   - Ensure internet permissions are granted
   - Check that the WebView JavaScript is enabled

2. **Poor performance**:
   - Consider upgrading to the YouTube API approach
   - Ensure device has adequate resources

3. **Issues extracting video ID**:
   - YouTube URL formats may change - update regex patterns
   - Log the URL being processed for debugging

4. **Content not loading in WebView**:
   - Enable debugging: `WebView.setWebContentsDebuggingEnabled(true);`
   - Check for WebView error events
   - Try different MIME types with `loadData()` method
   
5. **Security warnings**:
   - Use HTTPS for YouTube embeds
   - Consider adding network security config

## References

- [YouTube Android Player API](https://developers.google.com/youtube/android/player)
- [WebView Documentation](https://developer.android.com/reference/android/webkit/WebView)
- [YouTube Embedded Players](https://developers.google.com/youtube/iframe_api_reference) 