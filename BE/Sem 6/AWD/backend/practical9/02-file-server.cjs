// 02-file-server.js
// File Server - Serving static files and handling file operations

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3002;
const BASE_DIR = path.resolve(__dirname, '../../');

const mimeTypes = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'text/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
  console.log(`${req.method} ${req.url}`);

  const requestedPath = decodeURIComponent(req.url.split('?')[0]);

  let filePath;
  if (requestedPath === '/') {
    filePath = path.join(
      BASE_DIR,
      'assets',
      'a-minimalist-vector-logo-design-featurin_AwG4WkmDQnCYxphzErXgmQ_1TnwNI6rRRCX3Pg6upWYKA.png'
    );
  } else {
    filePath = path.join(BASE_DIR, requestedPath.replace(/^\/+/, ''));
  }

  const extname = String(path.extname(filePath)).toLowerCase();
  const contentType = mimeTypes[extname] || 'application/octet-stream';

  fs.readFile(filePath, (error, content) => {
    if (error) {
      if (error.code === 'ENOENT') {
        res.writeHead(404, { 'Content-Type': 'text/html' });
        res.end('<h1>404 - File Not Found</h1><p>The requested file was not found.</p>', 'utf-8');
      } else {
        res.writeHead(500);
        res.end(`Server Error: ${error.code}`, 'utf-8');
      }
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    }
  });
});

server.listen(PORT, () => {
  console.log('File Server Started');
  console.log(`File server running at: http://localhost:${PORT}/`);
  console.log('\nPress Ctrl+C to stop the server\n');
});
