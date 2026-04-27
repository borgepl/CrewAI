// Preload script to add proxy support for ALL Node.js HTTPS requests
// Monkey-patches https.Agent to always tunnel through the corporate proxy
const https = require('https');
const http = require('http');
const tls = require('tls');

const PROXY_HOST = 's-eacea-rh-proxy.eacea.cec.eu.int';
const PROXY_PORT = 9997;

const OriginalAgent = https.Agent;
const origCreateConnection = OriginalAgent.prototype.createConnection;

OriginalAgent.prototype.createConnection = function(options, callback) {
  const targetHost = options.host || options.hostname;
  const targetPort = options.port || 443;
  
  // Skip proxy for localhost
  if (targetHost === 'localhost' || targetHost === '127.0.0.1') {
    return origCreateConnection.call(this, options, callback);
  }

  const connectReq = http.request({
    host: PROXY_HOST,
    port: PROXY_PORT,
    method: 'CONNECT',
    path: `${targetHost}:${targetPort}`,
  });

  connectReq.on('connect', (res, socket) => {
    if (res.statusCode === 200) {
      const tlsSocket = tls.connect({
        ...options,
        socket: socket,
        servername: targetHost,
      });
      callback(null, tlsSocket);
    } else {
      callback(new Error(`Proxy CONNECT failed: ${res.statusCode}`));
    }
  });

  connectReq.on('error', (err) => {
    callback(err);
  });

  connectReq.end();
};
