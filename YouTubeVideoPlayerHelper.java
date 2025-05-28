package com.example.englishlearningapp.Utils;

import android.util.Log;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.VideoView;

/**
 * Helper class to manage YouTube video playback in WebView
 * This class handles YouTube URL parsing and embedding in a WebView
 */
public class YouTubeVideoPlayerHelper {
    private static final String TAG = "YouTubePlayerHelper";
    
    /**
     * Check if a URL is a YouTube URL
     * 
     * @param url The URL to check
     * @return True if it's a YouTube URL, false otherwise
     */
    public static boolean isYoutubeUrl(String url) {
        if (url == null) return false;
        return url.contains("youtube.com") || url.contains("youtu.be");
    }
    
    /**
     * Extract YouTube video ID from various YouTube URL formats
     * 
     * @param url YouTube URL
     * @return Video ID or null if extraction failed
     */
    public static String extractYoutubeVideoId(String url) {
        if (url == null) return null;
        
        try {
            if (url.contains("youtube.com/watch?v=")) {
                return url.split("youtube.com/watch\\?v=")[1].split("&")[0];
            } else if (url.contains("youtu.be/")) {
                return url.split("youtu.be/")[1].split("\\?")[0];
            } else if (url.contains("youtube.com/embed/")) {
                return url.split("youtube.com/embed/")[1].split("\\?")[0];
            }
        } catch (Exception e) {
            Log.e(TAG, "Error extracting YouTube video ID: " + e.getMessage());
        }
        
        return null;
    }
    
    /**
     * Load a YouTube video into a WebView
     * 
     * @param webView WebView to display the video
     * @param videoView VideoView to hide (will be made GONE)
     * @param youtubeUrl YouTube URL to play
     * @return True if video loaded successfully, false otherwise
     */
    public static boolean loadYoutubeVideo(WebView webView, VideoView videoView, String youtubeUrl) {
        if (webView == null || youtubeUrl == null) {
            Log.e(TAG, "WebView or URL is null");
            return false;
        }
        
        // Hide VideoView, show WebView
        if (videoView != null) {
            videoView.setVisibility(View.GONE);
        }
        
        webView.setVisibility(View.VISIBLE);
        
        // Set up WebView for YouTube
        webView.setWebViewClient(new WebViewClient());
        webView.setWebChromeClient(new WebChromeClient());
        
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setLoadWithOverviewMode(true);
        webSettings.setUseWideViewPort(true);
        
        // Extract YouTube video ID from the URL
        String videoId = extractYoutubeVideoId(youtubeUrl);
        if (videoId == null) {
            Log.e(TAG, "Could not extract YouTube video ID from: " + youtubeUrl);
            return false;
        }
        
        // Create HTML with embedded YouTube iframe
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
        
        webView.loadData(htmlContent, "text/html", "UTF-8");
        return true;
    }
} 