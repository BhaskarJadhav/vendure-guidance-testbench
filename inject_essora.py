import os
import sys

index_path = '/tmp/index.html'
local_path = os.path.join('node_modules', '@vendure', 'admin-ui-plugin', 'lib', 'admin-ui', 'browser', 'index.html')

if not os.path.exists(index_path):
    if os.path.exists(local_path):
        index_path = local_path
        print(f"Using local developer path: {index_path}")
    else:
        print(f"Error: Neither '/tmp/index.html' nor local node_modules path exists.")
        sys.exit(1)

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

essora_script = """
<!-- Essora AI SDK Integration -->
<script src="https://cdn.jsdelivr.net/npm/livekit-client@2/dist/livekit-client.umd.js"></script>
<script>
(function() {
  'use strict';
  if (window.__ESSORA_SDK_ACTIVE__ || window.__ESSORA_INJECT_LOADER__) return;
  window.__ESSORA_INJECT_LOADER__ = true;

  // Polyfill crypto.randomUUID for insecure HTTP contexts (non-HTTPS)
  try {
    if (!window.crypto) {
      window.crypto = {};
    }
    if (!window.crypto.randomUUID) {
      window.crypto.randomUUID = function() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
          var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
          return v.toString(16);
        });
      };
      console.log("Applied crypto.randomUUID polyfill for HTTP context.");
    }
  } catch (e) {
    console.error("Failed to polyfill crypto.randomUUID:", e);
  }

  // Check if developer wants to test their local SDK
  var urlParams = new URLSearchParams(window.location.search);
  var isLocal = urlParams.has('local_sdk');

  var BACKEND_URL = isLocal 
    ? 'http://localhost:8000' 
    : 'https://essora-backend-api-193009628373.asia-south1.run.app';
  var IDENTITY_URL = 'https://essora-identity-193009628373.asia-south1.run.app';
  var API_KEY = 'pk_62af599c2284eaa74b746d0b999927b7';

  fetch(BACKEND_URL + '/essora-sdk.js')
    .then(function(res) {
      if (!res.ok) throw new Error('SDK fetch failed: ' + res.status);
      return res.text();
    })
    .then(function(sdkCode) {
      var script = document.createElement('script');
      script.textContent = sdkCode;
      document.head.appendChild(script);

      setTimeout(function() {
        Essora.init({
          serverUrl: BACKEND_URL,
          identityUrl: IDENTITY_URL,
          livekitUrl: '',
          apiKey: API_KEY,
          appId: window.location.hostname,
          debug: true
        });
      }, 100);
    })
    .catch(function(err) {
      console.error('[ESSORA] Cannot load SDK:', err);
    });
})();
</script>
</body>
"""

if '<!-- Essora AI SDK Integration -->' in content:
    content = content.split('<!-- Essora AI SDK Integration -->')[0] + '</body>'

content = content.replace('</body>', essora_script)
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Injected/Updated Essora SDK successfully")
