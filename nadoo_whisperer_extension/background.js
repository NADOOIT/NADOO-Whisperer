// background.js

let port = null;

function connectToNativeApp() {
  if (port === null) {
    port = chrome.runtime.connectNative('de.nadooit.nadoo_whisperer');

    port.onMessage.addListener((msg) => {
      console.log("Received message from native app:", msg);
      // Handle the message from the native app
    });

    port.onDisconnect.addListener(() => {
      console.log("Disconnected from native app");
      port = null;
    });
  }
}

chrome.runtime.onInstalled.addListener(() => {
  connectToNativeApp();
  // Create an alarm to keep the service worker awake
  chrome.alarms.create('keepAlive', { periodInMinutes: 1 });
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'keepAlive') {
    // Perform a simple fetch to keep the service worker awake
    fetch('https://www.google.com', { mode: 'no-cors' }).then(() => {
      console.log('Keep-alive fetch performed.');
    }).catch((error) => {
      console.error('Keep-alive fetch failed:', error);
    });
  }
});

// Listen for messages from the content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Message received from content script:', message);
  
  if (message.command === "start_recording") {
    connectToNativeApp(); // Ensure connection to the native app
    if (port) {
      // Forward the message to the native application
      port.postMessage(message);
      console.log('Message sent to native app:', message);
    } else {
      console.error("Failed to connect to native app.");
    }
  }
});
