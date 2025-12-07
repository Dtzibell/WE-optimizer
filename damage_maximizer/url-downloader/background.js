// Load settings from storage
let urlPattern = /market\/equipments/; // Default pattern
let autoDownload = true;
let downloadPath = 'html-downloads'; // Subfolder within Downloads

// Load saved settings
chrome.storage.sync.get(['urlPattern', 'autoDownload', 'downloadPath'], (result) => {
  if (result.urlPattern) {
    try {
      urlPattern = new RegExp(result.urlPattern);
    } catch (e) {
      console.error('Invalid pattern:', e);
    }
  }
  if (result.autoDownload !== undefined) {
    autoDownload = result.autoDownload;
  }
  if (result.downloadPath) {
    downloadPath = result.downloadPath;
  }
});

// Listen for settings changes
chrome.storage.onChanged.addListener((changes) => {
  if (changes.urlPattern) {
    try {
      urlPattern = new RegExp(changes.urlPattern.newValue);
    } catch (e) {
      console.error('Invalid pattern:', e);
    }
  }
  if (changes.autoDownload) {
    autoDownload = changes.autoDownload.newValue;
  }
  if (changes.downloadPath) {
    downloadPath = changes.downloadPath.newValue;
  }
});

// Monitor page loads
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url && autoDownload) {
    if (urlPattern.test(tab.url)) {
      console.log('Matched URL:', tab.url);
      
      setTimeout(() => {
        chrome.scripting.executeScript({
          target: { tabId: tabId },
          func: downloadPageHTML
        });
      }, 1000);
    }
  }
});

function downloadPageHTML() {
  const html = document.documentElement.outerHTML;
  const url = window.location.href;
  
  const filename = url
    .replace(/https?:\/\//, '')
    .replace(/[^\w\-\.]/g, '_')
    .substring(0, 200) + '.html';
  
  const blob = new Blob([html], { type: 'text/html' });
  const blobUrl = URL.createObjectURL(blob);
  
  chrome.runtime.sendMessage({
    action: 'download',
    url: blobUrl,
    filename: filename,
    pageUrl: url
  });
}

// Handle download requests
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'download') {
    // Construct the full path (relative to Downloads folder)
    const fullPath = downloadPath ? `${downloadPath}/${request.filename}` : request.filename;
    
    chrome.downloads.download({
      url: request.url,
      filename: fullPath,
      saveAs: false,  // This prevents the "Save As" dialog
      conflictAction: 'uniquify'  // Auto-rename if file exists
    }, (downloadId) => {
      if (downloadId) {
        console.log('Downloaded:', request.pageUrl, '->', fullPath);
        
        // Optionally hide the download from the shelf
        if (chrome.downloads.setShelfEnabled) {
          chrome.downloads.setShelfEnabled(false);
        }
      } else {
        console.error('Download failed for:', request.pageUrl);
      }
    });
  }
  
  if (request.action === 'downloadNow') {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        chrome.scripting.executeScript({
          target: { tabId: tabs[0].id },
          func: downloadPageHTML
        });
      }
    });
  }
  
  if (request.action === 'checkUrl') {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        const matches = urlPattern.test(tabs[0].url);
        sendResponse({ matches: matches, url: tabs[0].url });
      }
    });
    return true;
  }
});
