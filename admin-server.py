#!/usr/bin/env python3
"""
Admin save server for activemillers.com static site.
Listens on localhost:8760. Only accessible from localhost.
Accepts POST /save-order with new image order and rewrites the HTML file in place.
"""
import http.server
import json
import os
import re
import sys
import traceback

PORT = 8760
SITE_DIR = os.path.dirname(os.path.abspath(__file__))

class AdminHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Quiet logging
        sys.stderr.write("[admin-server] %s - %s\n" % (self.client_address[0], args[0] if args else ''))

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    def do_POST(self):
        if self.path == '/save-order':
            try:
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length)
                data = json.loads(body)

                page = data.get('page', '')
                images = data.get('images', [])

                # Security: only allow .html files in this directory
                page = os.path.basename(page)
                if not page.endswith('.html'):
                    self._json_error(400, 'Only .html files allowed')
                    return

                filepath = os.path.join(SITE_DIR, page)
                if not os.path.exists(filepath):
                    self._json_error(404, 'File not found: %s' % page)
                    return

                # Read the current file
                with open(filepath, 'r', encoding='utf-8') as f:
                    html = f.read()

                # Find all content images (image-row + stacked-images)
                # We need to rebuild the image-row and stacked-images sections

                # Split images: first 2 go to image-row, rest to stacked-images
                image_row_imgs = images[:2]
                stacked_imgs = images[2:]

                # Build new image-row HTML
                if image_row_imgs:
                    row_items = []
                    for img in image_row_imgs:
                        row_items.append(
                            '  <div class="img-wrap">\n'
                            '    <img src="%s" alt="%s" loading="lazy">\n'
                            '  </div>' % (img['src'], img.get('alt', ''))
                        )
                    new_image_row = '<!-- ===== 2. TWO-IMAGE ROW ===== -->\n'
                    new_image_row += '<section class="image-row fade-in">\n'
                    new_image_row += '\n'.join(row_items) + '\n'
                    new_image_row += '</section>'
                else:
                    new_image_row = ''

                # Build new stacked-images HTML
                if stacked_imgs:
                    stack_items = []
                    for img in stacked_imgs:
                        stack_items.append(
                            '  <div class="img-wrap fade-in">\n'
                            '    <img src="%s" alt="%s" loading="lazy">\n'
                            '  </div>' % (img['src'], img.get('alt', ''))
                        )
                    new_stacked = '<!-- ===== 4. PROGRESSION PANELS ===== -->\n'
                    new_stacked += '<section class="stacked-images">\n'
                    new_stacked += '\n'.join(stack_items) + '\n'
                    new_stacked += '</section>'
                else:
                    new_stacked = ''

                # Replace image-row section
                # Pattern: <!-- ===== 2. TWO-IMAGE ROW ===== --> ... </section>
                row_pattern = r'<!-- ===== 2\. TWO-IMAGE ROW ===== -->\s*<section class="image-row[^"]*"[^>]*>.*?</section>'
                if new_image_row:
                    html = re.sub(row_pattern, new_image_row, html, count=1, flags=re.DOTALL)
                else:
                    # Remove the section entirely if no images
                    html = re.sub(row_pattern, '', html, count=1, flags=re.DOTALL)

                # Replace stacked-images section
                # Pattern: <!-- ===== 4. PROGRESSION PANELS ===== --> ... </section>
                # (some pages use different numbers/comments — be flexible)
                stack_pattern = r'<!-- ===== \d+\. PROGRESSION PANELS ===== -->\s*<section class="stacked-images"[^>]*>.*?</section>'
                if new_stacked:
                    if re.search(stack_pattern, html, flags=re.DOTALL):
                        html = re.sub(stack_pattern, new_stacked, html, count=1, flags=re.DOTALL)
                    else:
                        # Insert before outcome section
                        outcome_pattern = r'(<!-- ===== \d+\. OUTCOME SECTION ===== -->)'
                        html = re.sub(outcome_pattern, new_stacked + '\n\n' + r'\1', html, count=1, flags=re.DOTALL)
                else:
                    html = re.sub(stack_pattern, '', html, count=1, flags=re.DOTALL)

                # Write back
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html)

                self._json_ok({'ok': True, 'count': len(images), 'page': page})

            except Exception as e:
                traceback.print_exc()
                self._json_error(500, str(e))
        else:
            self._json_error(404, 'Not found')

    def do_GET(self):
        if self.path == '/health':
            self._json_ok({'ok': True, 'dir': SITE_DIR})
        else:
            self._json_error(404, 'Not found')

    def _cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _json_ok(self, data):
        self.send_response(200)
        self._cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _json_error(self, code, msg):
        self.send_response(code)
        self._cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'ok': False, 'error': msg}).encode())


if __name__ == '__main__':
    print('[admin-server] Serving %s on http://localhost:%d' % (SITE_DIR, PORT))
    print('[admin-server] Endpoints: POST /save-order  GET /health')
    server = http.server.HTTPServer(('127.0.0.1', PORT), AdminHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n[admin-server] Shutting down.')
        server.shutdown()
