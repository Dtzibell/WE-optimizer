// Load current settings
chrome.storage.sync.get(['urlPattern', 'autoDownload', 'downloadPath'], (result) => {
  document.getElementById('pattern').value = result.urlPattern || 'articles';
  document.getElementById('autoDownload').checked = result.autoDownload !== false;
  document.getElementById('downloadPath').value = result.downloadPath || 'html-downloads';
  
  updatePathPreview();
  checkCurrentUrl();
});

// Update path preview
function updatePathPreview() {
  const path = document.getElementById('downloadPath').value || '(root)';
  document.getElementById('pathPreview').textContent = path;
}

document.getElementById('downloadPath').addEventListener('input', updatePathPreview);

// Save settings
document.getElementById('save').addEventListener('click', () => {
  const pattern = document.getElementById('pattern').value;
  const autoDownload = document.getElementById('autoDownload').checked;
  const downloadPath = document.getElementById('downloadPath').value.trim();
  
  try {
    new RegExp(pattern);
    
    chrome.storage.sync.set({
      urlPattern: pattern,
      autoDownload: autoDownload,
      downloadPath: downloadPath
    }, () => {
      showStatus('Settings saved! Files will be downloaded to: Downloads/' + (downloadPath || '(root)'), true);
      checkCurrentUrl();
    });
  } catch (e) {
    showStatus('Invalid regex pattern: ' + e.message, false);
  }
});

// Download current page
document.getElementById('downloadNow').addEventListener('click', () => {
  chrome.runtime.sendMessage({ action: 'downloadNow' });
  showStatus('Downloading current page...', true);
});

// Check if current URL matches pattern
function checkCurrentUrl() {
  chrome.runtime.sendMessage({ action: 'checkUrl' }, (response) => {
    if (response) {
      if (response.matches) {
        showStatus(`✓ Current URL matches pattern: ${response.url}`, true);
      } else {
        showStatus(`✗ Current URL doesn't match pattern: ${response.url}`, false);
      }
    }
  });
}

function showStatus(message, isSuccess) {
  const statusDiv = document.getElementById('status');
  statusDiv.textContent = message;
  statusDiv.className = 'status ' + (isSuccess ? 'match' : 'no-match');
  statusDiv.style.display = 'block';
}

document.getElementById('pattern').addEventListener('input', () => {
  clearTimeout(window.checkTimeout);
  window.checkTimeout = setTimeout(checkCurrentUrl, 500);
});
