const http = require('http');

http.createServer((req, res) => {
    console.log(`Request Details: Method=${req.method}, URL=${req.url}`);
    
    port = req.url.split('=')[1];
    console.log(`Port: ${port}`);

    res.writeHead(302, { 'Location': 'http://127.0.0.1:' + port });
    res.end();
}).listen(8080, () => console.log('Node.js web server at 8080 is logging client info and redirecting...'));
