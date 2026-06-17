import os
import sys

index_path = '/tmp/index.html'

if not os.path.exists(index_path):
    print(f"Error: {index_path} does not exist.")
    sys.exit(1)

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

essora_script = """
<!-- Essora AI SDK Integration -->
<script src="https://unpkg.com/livekit-client/dist/livekit-client.umd.js"></script>
<script src="https://essora-backend-api-193009628373.asia-south1.run.app/essora-sdk.js"></script>
<script>
  (function() {
    function initEssora() {
      if (typeof Essora !== 'undefined') {
        try {
          Essora.init({
            serverUrl: "https://essora-backend-api-193009628373.asia-south1.run.app",
            livekitUrl: "wss://essora-ai-june-3gghj1x0.livekit.cloud",
            apiKey: "pk_d767b78a9b1a22bb50dc179f8c12dc2d",
            user: {
              id: "vendure-admin",
              email: "superadmin@vendure.io",
              name: "Vendure Superadmin"
            }
          });
          console.log("Essora SDK initialized successfully.");
        } catch(e) {
          console.error("Essora init error:", e);
        }
      } else {
        setTimeout(initEssora, 500);
      }
    }
    if (document.readyState === 'complete') {
      initEssora();
    } else {
      window.addEventListener('load', initEssora);
    }
  })();
</script>
</body>
"""

if 'essora-sdk.js' not in content:
    content = content.replace('</body>', essora_script)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected Essora SDK successfully")
else:
    print("Essora SDK already injected")
