// Proxy wrapper for agentcore CLI
// Patches Node.js https.globalAgent to use the corporate proxy
const https = require('https');
const http = require('http');
const net = require('net');
const tls = require('tls');

const PROXY_HOST = 's-eacea-rh-proxy.eacea.cec.eu.int';
const PROXY_PORT = 9997;

// Override https.request to tunnel through the proxy
const originalRequest = https.request;
https.request = function(options, callback) {
  if (typeof options === 'string') {
    options = new URL(options);
  }
  
  const host = options.hostname || options.host;
  const port = options.port || 443;
  
  // Create a CONNECT tunnel through the proxy
  return new Promise((resolve) => {
    const proxyReq = http.request({
      host: PROXY_HOST,
      port: PROXY_PORT,
      method: 'CONNECT',
      path: `${host}:${port}`,
    });
    
    proxyReq.on('connect', (res, socket) => {
      if (res.statusCode === 200) {
        options.socket = socket;
        options.agent = false;
        const req = originalRequest.call(https, options, callback);
        resolve(req);
      }
    });
    
    proxyReq.end();
  });
};
